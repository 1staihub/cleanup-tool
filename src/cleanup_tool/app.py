from __future__ import annotations

from pathlib import Path

from cleanup_tool.cleaning.cleaner import CleanupCleaner
from cleanup_tool.orchestrator import CleanupOrchestrator
from cleanup_tool.reporting.html_reporter import HtmlReporter
from cleanup_tool.reporting.markdown_reporter import MarkdownReporter
from cleanup_tool.rules.windows import WindowsCleanupRules
from cleanup_tool.scanning.scanner import CleanupScanner


def build_application(root_dir: Path, report_path: Path) -> tuple[CleanupOrchestrator, MarkdownReporter, HtmlReporter]:
    rules = WindowsCleanupRules.from_root(root_dir)
    scanner = CleanupScanner(rules)
    cleaner = CleanupCleaner()
    orchestrator = CleanupOrchestrator(scanner, cleaner, root_dir)
    markdown_reporter = MarkdownReporter(report_path)
    html_reporter = HtmlReporter(report_path)
    return orchestrator, markdown_reporter, html_reporter
