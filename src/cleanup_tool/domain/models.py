from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class CleanupItem:
    tier: str
    name: str
    path: Path
    reason: str
    action: str
    size_bytes: int = 0
    category: str = "other"
    kill_processes: tuple[str, ...] = ()
    note: str = ""


@dataclass(slots=True)
class CleanupSummary:
    green_bytes: int
    yellow_bytes: int
    red_bytes: int = 0
