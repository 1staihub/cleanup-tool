from __future__ import annotations

from pathlib import Path

from cleanup_tool.domain.models import CleanupItem, CleanupSummary
from cleanup_tool.system import SystemInfo, SystemInfoService


class HtmlReporter:
    def __init__(self, report_path: Path, template_path: Path | None = None) -> None:
        self.report_path = report_path
        self.template_path = template_path or Path(__file__).resolve().parents[1].joinpath("templates", "interactive_report.html")
        self.size = SystemInfoService.human_size

    def write_html(self, system: SystemInfo, summary: CleanupSummary, items: list[CleanupItem], token: str) -> Path:
        top5 = sorted(items, key=lambda item: item.size_bytes, reverse=True)[:5]
        template = self.template_path.read_text(encoding="utf-8")
        html = (
            template.replace("{{SYSTEM_OS}}", system.os_name)
            .replace("{{SYSTEM_USER}}", system.user)
            .replace("{{SYSTEM_DRIVE}}", system.drive_name)
            .replace("{{GREEN_SIZE}}", self.size(summary.green_bytes))
            .replace("{{YELLOW_SIZE}}", self.size(summary.yellow_bytes))
            .replace("{{RED_SIZE}}", self.size(summary.red_bytes))
            .replace("{{TOP1_NAME}}", top5[0].name if top5 else "无")
            .replace("{{TOP5_HTML}}", self._top5_html(top5))
            .replace("{{GREEN_ITEMS}}", self._render_items(items, "Green"))
            .replace("{{YELLOW_ITEMS}}", self._render_items(items, "Yellow"))
            .replace("{{RED_ITEMS}}", self._render_items(items, "Red"))
            .replace("{{CLEANUP_TOKEN}}", token)
        )
        html_path = self.report_path.with_suffix(".html")
        html_path.write_text(html, encoding="utf-8")
        return html_path

    def _top5_html(self, top5: list[CleanupItem]) -> str:
        return "".join(
            f"<li><b>{item.name}</b> <span>{self.size(item.size_bytes)}</span> <small>{item.reason}</small></li>"
            for item in top5
        )

    def _render_items(self, items: list[CleanupItem], tier: str) -> str:
        scoped = sorted((item for item in items if item.tier == tier), key=lambda x: x.size_bytes, reverse=True)
        if not scoped:
            return "<div class='empty'>无</div>"
        blocks = []
        for item in scoped:
            clean_button = ""
            if item.tier == "Green":
                clean_button = f'<button class="btn-clean" data-action="clean" data-path="{item.path}">清理</button>'
            open_button = f'<button class="btn-open" data-action="open" data-path="{item.path}">打开路径</button>'
            blocks.append(
                f"""
                <details class="card">
                  <summary>{item.name} <span>{self.size(item.size_bytes)}</span></summary>
                  <div class="body">
                    <p><b>路径</b>：<code>{item.path}</code></p>
                    <p><b>说明</b>：{item.reason}</p>
                    <p><b>处理</b>：{item.action}</p>
                    <div class="actions">
                      {clean_button}
                      {open_button}
                    </div>
                  </div>
                </details>
                """
            )
        return "\n".join(blocks)
