from __future__ import annotations

from cleanup_tool.domain.models import CleanupItem, CleanupSummary


class SummaryService:
    def summarize(self, items: list[CleanupItem]) -> CleanupSummary:
        green = sum(item.size_bytes for item in items if item.tier == "Green")
        yellow = sum(item.size_bytes for item in items if item.tier == "Yellow")
        red = sum(item.size_bytes for item in items if item.tier == "Red")
        return CleanupSummary(green_bytes=green, yellow_bytes=yellow, red_bytes=red)
