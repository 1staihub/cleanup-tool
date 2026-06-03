from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SystemInfo:
    os_name: str
    user: str
    drive_name: str
    disk_total: str
    disk_used: str
    disk_free: str


class SystemInfoService:
    @staticmethod
    def human_size(num: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(num)
        for unit in units:
            if value < 1024 or unit == "TB":
                return f"{value:.2f} {unit}" if unit != "B" else f"{int(value)} B"
            value /= 1024
        return f"{value:.2f} TB"

    def read(self, drive: Path) -> SystemInfo:
        try:
            total, used, free = shutil.disk_usage(str(drive))
            total_h = self.human_size(total)
            used_h = self.human_size(used)
            free_h = self.human_size(free)
        except OSError:
            total_h = used_h = free_h = "?"
        return SystemInfo(
            os_name=f"Windows {os.environ.get('OS', '').strip() or sys.platform}",
            user=os.environ.get("USERNAME", ""),
            drive_name=str(drive),
            disk_total=total_h,
            disk_used=used_h,
            disk_free=free_h,
        )
