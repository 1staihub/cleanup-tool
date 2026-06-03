from __future__ import annotations

import logging
import shutil
from pathlib import Path

from cleanup_tool.domain.models import CleanupItem
from cleanup_tool.exceptions import ApplyError
from cleanup_tool.interfaces import Cleaner

logger = logging.getLogger(__name__)


class CleanupCleaner(Cleaner):
    def apply(self, items: list[CleanupItem]) -> None:
        for item in items:
            if item.tier != "Green":
                continue
            if not self._exists(item.path):
                continue
            logger.info("Removing %s", item.path)
            self._remove_path(item.path)

    def _exists(self, path: Path) -> bool:
        try:
            return path.exists()
        except OSError:
            return False

    def _remove_path(self, path: Path) -> None:
        try:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
        except Exception as exc:
            raise ApplyError(f"Failed to remove {path}: {exc}") from exc
