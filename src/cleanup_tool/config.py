from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    root_dir: Path
    report_path: Path
    system_drive: Path | None = None

    @property
    def data_dir(self) -> Path:
        return self.root_dir / "Data"
