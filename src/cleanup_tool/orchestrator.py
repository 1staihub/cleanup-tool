from __future__ import annotations

from pathlib import Path

from cleanup_tool.interfaces import Cleaner, Scanner
from cleanup_tool.domain.models import CleanupItem, CleanupSummary
from cleanup_tool.system import SummaryService, SystemInfoService


class CleanupOrchestrator:
    def __init__(self, scanner: Scanner, cleaner: Cleaner, drive: Path) -> None:
        self.scanner = scanner
        self.cleaner = cleaner
        self.drive = drive
        self.system_info_service = SystemInfoService()
        self.summary_service = SummaryService()

    def scan(self) -> list[CleanupItem]:
        return self.scanner.scan()

    def summarize(self, items: list[CleanupItem]) -> CleanupSummary:
        return self.summary_service.summarize(items)

    def apply(self, items: list[CleanupItem]) -> None:
        self.cleaner.apply(items)
