from __future__ import annotations

import json
import logging
import os
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from cleanup_tool.domain.models import CleanupItem
from cleanup_tool.exceptions import CleanupRuntimeError
from cleanup_tool.orchestrator import CleanupOrchestrator
from cleanup_tool.reporting.html_reporter import HtmlReporter

logger = logging.getLogger(__name__)


class CleanupWebServer:
    def __init__(self, orchestrator: CleanupOrchestrator, reporter: HtmlReporter, items: list[CleanupItem]) -> None:
        self.orchestrator = orchestrator
        self.reporter = reporter
        self.items = items
        self._server: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._html_path: Path | None = None
        self._token = secrets.token_urlsafe(16)

    def start(self) -> str:
        self._refresh_report()
        self._server = HTTPServer(("127.0.0.1", 0), self._make_handler())
        port = self._server.server_port
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        url = f"http://127.0.0.1:{port}/"
        webbrowser.open(url)
        return url

    def close(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
        if self._thread:
            self._thread.join(timeout=2)

    def wait(self) -> None:
        try:
            if self._thread:
                self._thread.join()
        except KeyboardInterrupt:
            self.close()

    def _make_handler(self):
        server = self

        class Handler(BaseHTTPRequestHandler):
            server_version = "CleanupToolHTTP/1.0"

            def _send(self, content: str, content_type: str = "text/html; charset=utf-8", status: int = 200) -> bool:
                payload = content.encode("utf-8")
                try:
                    self.send_response(status)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(len(payload)))
                    self.end_headers()
                    self.wfile.write(payload)
                    return True
                except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                    logger.debug("Client disconnected before response could be sent")
                    return False

            def do_GET(self):  # noqa: N802
                if not server._is_authorized(self):
                    self._send(json.dumps({"ok": False, "message": "Unauthorized"}, ensure_ascii=False), "application/json; charset=utf-8", 403)
                    return
                path = urlparse(self.path).path
                if path == "/":
                    if server._html_path and server._html_path.exists():
                        self._send(server._html_path.read_text(encoding="utf-8"))
                    else:
                        self._send("<h1>Report missing</h1>", status=404)
                    return
                if path == "/api/status":
                    summary = server.orchestrator.summarize(server.items)
                    payload = {
                        "ok": True,
                        "green_bytes": summary.green_bytes,
                        "yellow_bytes": summary.yellow_bytes,
                        "red_bytes": summary.red_bytes,
                    }
                    self._send(json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")
                    return
                if path == "/favicon.ico":
                    self._send("", "image/x-icon", 204)
                    return
                self._send("<h1>Not Found</h1>", status=404)

            def do_POST(self):  # noqa: N802
                if not server._is_authorized(self):
                    self._send(json.dumps({"ok": False, "message": "Unauthorized"}, ensure_ascii=False), "application/json; charset=utf-8", 403)
                    return
                path = urlparse(self.path).path
                if path != "/api/action":
                    self._send(json.dumps({"ok": False, "message": "Not found"}, ensure_ascii=False), "application/json; charset=utf-8", 404)
                    return
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length).decode("utf-8") if length else "{}"
                payload = json.loads(raw)
                action = payload.get("action", "")
                target_path = payload.get("path", "")
                try:
                    result = server.handle_action(action, target_path)
                    self._send(json.dumps(result, ensure_ascii=False), "application/json; charset=utf-8")
                except Exception as exc:
                    logger.exception("Action handler failed: %s", action)
                    self._send(json.dumps({"ok": False, "message": str(exc)}, ensure_ascii=False), "application/json; charset=utf-8", 500)

            def log_message(self, format, *args):  # noqa: A003
                return

        return Handler

    def handle_action(self, action: str, target_path: str) -> dict[str, object]:
        if action == "clean-all-green":
            green = [item for item in self.items if item.tier == "Green"]
            self.orchestrator.apply(green)
            self._refresh_items()
            return {"ok": True, "message": "All green items removed"}
        if action in {"clean", "open"} and target_path:
            item = self._find_item(target_path)
            if not item:
                return {"ok": False, "message": "Item not found"}
            if not item.path.exists():
                self._refresh_items()
                return {"ok": True, "message": "Item already removed"}
            if action == "open":
                self._open_path(item.path)
                return {"ok": True, "message": "Path opened"}
            self.orchestrator.apply([item])
            self._refresh_items()
            return {"ok": True, "message": "Item removed"}
        return {"ok": False, "message": "Unsupported action"}

    def _find_item(self, path: str) -> CleanupItem | None:
        for item in self.items:
            if str(item.path) == path:
                return item
        return None

    def _refresh_items(self) -> None:
        self.items = self.orchestrator.scan()
        self._refresh_report()

    def _refresh_report(self) -> None:
        summary = self.orchestrator.summarize(self.items)
        system = self.orchestrator.system_info_service.read(self.orchestrator.drive)
        self._html_path = self.reporter.write_html(system, summary, self.items, self._token)

    def _open_path(self, path: Path) -> None:
        resolved = path.resolve()
        allowed = [item.path.resolve() for item in self.items]
        if resolved not in allowed:
            raise CleanupRuntimeError("Path is not in the scanned item list")
        if os.name == "nt":
            os.startfile(str(resolved))
            return
        webbrowser.open(resolved.as_uri())

    def _is_authorized(self, handler: BaseHTTPRequestHandler) -> bool:
        host = handler.headers.get("Host", "")
        origin = handler.headers.get("Origin", "")
        token = handler.headers.get("X-Cleanup-Token", "")
        if token != self._token:
            return False
        if not host.startswith("127.0.0.1:"):
            return False
        if origin and not origin.startswith("http://127.0.0.1:"):
            return False
        return True
