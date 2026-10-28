from functools import cached_property
from pathlib import Path

from pydantic import BaseModel
from PySide6.QtCore import QStandardPaths


class PathsConfig(BaseModel):
    @cached_property
    def config_path(self) -> Path:
        path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    @cached_property
    def preferences_path(self) -> Path:
        return self.config_path / "preferences.json"

    @cached_property
    def local_data_path(self) -> Path:
        path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppLocalDataLocation
            )
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    @cached_property
    def log_path(self) -> Path:
        path: Path = self.local_data_path / "logs" / "app.log"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
