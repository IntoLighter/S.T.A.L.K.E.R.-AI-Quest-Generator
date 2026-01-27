import sys
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings
from PySide6.QtCore import QStandardPaths


def get_resource_path(relative_path: str) -> Path:
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(relative_path)


class ConstantsConfig(BaseSettings):
    window_dims: tuple[int, int] = (800, 600)

    editor_stretch: int = 1
    concept_stretch: int = 4
    metadata_stretch: int = 2

    editor_height: int = 100
    concept_height: int = editor_height * concept_stretch
    metadata_height: int = editor_height * metadata_stretch

    icon_path: Path = get_resource_path("resource/icon.ico")
    prompt_path: Path = get_resource_path("resource/prompt")

    app_version: str = "1.0"

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


constants_config = ConstantsConfig()
