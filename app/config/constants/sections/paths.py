from pathlib import Path

from pydantic import BaseModel, computed_field
from PySide6.QtCore import QStandardPaths


class PathsConfig(BaseModel):
    @computed_field
    def config_path(self) -> Path:
        path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    @computed_field
    def preferences_path(self) -> Path:
        return self.config_path / "preferences.json"

    @computed_field
    def local_data_path(self) -> Path:
        path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppLocalDataLocation
            )
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    @computed_field
    def log_path(self) -> Path:
        path: Path = self.local_data_path / "logs" / "app.log"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
