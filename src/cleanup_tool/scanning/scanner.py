from __future__ import annotations

import logging
import os
from pathlib import Path

from cleanup_tool.domain.models import CleanupItem
from cleanup_tool.interfaces import RuleProvider, Scanner

logger = logging.getLogger(__name__)


class CleanupScanner(Scanner):
    def __init__(self, rules: RuleProvider) -> None:
        self.rules = rules

    def scan(self) -> list[CleanupItem]:
        items: list[CleanupItem] = []
        for item in self.rules.rules():
            if self._exists(item.path):
                item.size_bytes = self._size_of(item.path)
                items.append(item)
        logger.info("Scanned %s items", len(items))
        return items

    def _size_of(self, path: Path) -> int:
        if not self._exists(path):
            return 0
        if path.is_file():
            try:
                return path.stat().st_size
            except OSError:
                return 0
        total = 0
        for root, _, files in os.walk(path, topdown=True, followlinks=False):
            for name in files:
                fp = Path(root) / name
                try:
                    if fp.is_symlink():
                        continue
                    total += fp.stat().st_size
                except OSError:
                    continue
        return total

    def _exists(self, path: Path) -> bool:
        try:
            return path.exists()
        except OSError:
            return False


class DrilldownScanner:
    def scan_children(self, path: Path, limit: int = 20) -> list[CleanupItem]:
        items: list[CleanupItem] = []
        if not path.exists() or not path.is_dir():
            return items
        for child in path.iterdir():
            try:
                size = self._size_of(child)
            except Exception:
                continue
            items.append(
                CleanupItem(
                    tier="Inspect",
                    name=child.name,
                    path=child,
                    reason="目录下一级占用分析",
                    action="Review",
                    size_bytes=size,
                    category="drilldown",
                )
            )
        items.sort(key=lambda item: item.size_bytes, reverse=True)
        return items[:limit]

    def _size_of(self, path: Path) -> int:
        if not path.exists():
            return 0
        if path.is_file():
            try:
                return path.stat().st_size
            except OSError:
                return 0
        total = 0
        for root, _, files in os.walk(path, topdown=True, followlinks=False):
            for name in files:
                fp = Path(root) / name
                try:
                    if fp.is_symlink():
                        continue
                    total += fp.stat().st_size
                except OSError:
                    continue
        return total
