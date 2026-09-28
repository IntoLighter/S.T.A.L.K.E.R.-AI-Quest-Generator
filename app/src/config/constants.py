from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings
from PySide6.QtCore import QStandardPaths
from util.resource import read_resource


class ConstantsConfig(BaseSettings):
    default_concept_prompt: str = read_resource(":/prompt/concept.txt")
    default_metadata_prompt: str = read_resource(":/prompt/metadata.txt")
    default_icon_prompt: str = read_resource(":/prompt/icon.txt")

    icon_path: str = ":/icon/icon.ico"

    default_icon_workflow: str = read_resource(":/workflow/icon.json")

    quest_generated_tray_message_msecs: int = 5000

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
