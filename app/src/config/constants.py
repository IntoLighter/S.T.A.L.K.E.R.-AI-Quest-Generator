from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings
from PySide6.QtCore import QStandardPaths
from util.misc import read_resource


class ConstantsConfig(BaseSettings):
    window_size: tuple[int, int] = (1280, 720)
    dialog_size: tuple[int, int] = (1024, 576)

    local_model_base_url: str = "http://127.0.0.1:11434/v1"
    local_model_api_key: str = "Key"
    remote_model_base_url: str = "http://127.0.0.1:8000/v1"
    remote_model_api_key: str = "VerysecretKey"
    comfy_ui_base_url: str = "http://127.0.0.1:8188"

    editor_stretch: int = 1
    concept_stretch: int = 4
    metadata_stretch: int = 2
    icon_prompt_stretch: int = 2

    editor_height: int = 100
    concept_height: int = editor_height * concept_stretch
    metadata_height: int = editor_height * metadata_stretch
    icon_prompt_height: int = editor_height * icon_prompt_stretch

    icon_workflow_stretch: int = 4
    icon_workflow_height: int = editor_height * icon_workflow_stretch

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
