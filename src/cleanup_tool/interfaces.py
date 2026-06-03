from __future__ import annotations

from pathlib import Path
from typing import Protocol

from cleanup_tool.domain.models import CleanupItem
from cleanup_tool.domain.models import CleanupSummary
from cleanup_tool.system import SystemInfo


class RuleProvider(Protocol):
    def rules(self) -> list[CleanupItem]:
        ...


class Scanner(Protocol):
    def scan(self) -> list[CleanupItem]:
        ...


class Reporter(Protocol):
    def write_markdown(self, system: SystemInfo, summary: CleanupSummary, items: list[CleanupItem]) -> Path:
        ...

    def write_html(self, system: SystemInfo, summary: CleanupSummary, items: list[CleanupItem]) -> Path:
        ...


class Cleaner(Protocol):
    def apply(self, items: list[CleanupItem]) -> None:
        ...
