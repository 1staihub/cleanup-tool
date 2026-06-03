from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cleanup_tool.app import build_application
from cleanup_tool.exceptions import CleanupToolError
from cleanup_tool.logging_utils import setup_logging
from cleanup_tool.scanning import DrilldownScanner
from cleanup_tool.web import CleanupWebServer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cleanup-tool")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default="C:\\", help="System drive root")
    common.add_argument("--report", default="cleanup-report.md", help="Report output path")
    common.add_argument("--verbose", action="store_true", help="Enable debug logging")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scan", help="Scan system junk only", parents=[common])
    subparsers.add_parser("report", help="Scan and write report", parents=[common])
    subparsers.add_parser("html", help="Scan and write HTML report", parents=[common])
    drilldown_parser = subparsers.add_parser("drilldown", help="Inspect one directory level", parents=[common])
    drilldown_parser.add_argument("--path", required=True, help="Target directory to inspect")
    drilldown_parser.add_argument("--limit", type=int, default=20, help="Max children to show")

    apply_parser = subparsers.add_parser("apply", help="Apply safe cleanup", parents=[common])
    apply_parser.add_argument("--yes", action="store_true", help="Confirm cleanup")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging(verbose=args.verbose)

    root_dir = Path(args.root).resolve()
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = Path.cwd() / report_path

    if args.command == "drilldown":
        target = Path(args.path).resolve()
        scanner = DrilldownScanner()
        items = scanner.scan_children(target, limit=args.limit)
        print(f"Drilldown: {target}")
        for index, item in enumerate(items, start=1):
            print(f"{index}. {item.name} | {item.size_bytes} bytes | {item.path}")
        return 0

    service, markdown_reporter, html_reporter = build_application(root_dir, report_path)
    items = service.scan()

    if args.command == "scan":
        summary = service.summarize(items)
        print(f"Scanned items: {len(items)}")
        print(f"Safe-to-clean size: {summary.green_bytes}")
        print(f"Review-first size: {summary.yellow_bytes}")
        try:
            server = CleanupWebServer(service, html_reporter, items)
            url = server.start()
            print(f"Interactive report: {url}")
            print("Press Ctrl+C to stop the local server.")
            server.wait()
        except CleanupToolError as exc:
            print(str(exc))
            return 1
        except Exception as exc:
            print(str(exc))
            return 1
        return 0

    if args.command == "report":
        try:
            summary = service.summarize(items)
            system = service.system_info_service.read(root_dir)
            report = markdown_reporter.write_markdown(system, summary, items)
        except CleanupToolError as exc:
            print(str(exc))
            return 1
        print(f"Report generated: {report}")
        return 0

    if args.command == "html":
        try:
            summary = service.summarize(items)
            system = service.system_info_service.read(root_dir)
            report = html_reporter.write_html(system, summary, items)
        except CleanupToolError as exc:
            print(str(exc))
            return 1
        print(f"HTML report generated: {report}")
        return 0

    if args.command == "apply":
        if not args.yes:
            print("Refusing to apply cleanup without --yes")
            return 2
        try:
            service.apply(items)
            summary = service.summarize(items)
            system = service.system_info_service.read(root_dir)
            report = markdown_reporter.write_markdown(system, summary, items)
        except CleanupToolError as exc:
            print(str(exc))
            return 1
        print(f"Cleanup finished. Report: {report}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
