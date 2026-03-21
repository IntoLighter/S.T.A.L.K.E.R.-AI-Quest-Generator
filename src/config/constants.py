from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings
from PySide6.QtCore import QStandardPaths

from misc import get_resource_file_content, get_resource_path


class ConstantsConfig(BaseSettings):
    window_dims: tuple[int, int] = (800, 600)

    editor_stretch: int = 1
    concept_stretch: int = 4
    metadata_stretch: int = 2

    editor_height: int = 100
    concept_height: int = editor_height * concept_stretch
    metadata_height: int = editor_height * metadata_stretch

    icon_workflow_stretch: int = 4
    icon_workflow_height: int = editor_height * icon_workflow_stretch

    prompt_path: Path = get_resource_path("prompt")
    default_concept_prompt: str = get_resource_file_content(prompt_path / "concept.txt")
    default_metadata_prompt: str = get_resource_file_content(prompt_path / "metadata.txt")
    default_icon_prompt: str = get_resource_file_content(prompt_path / "icon.txt")

    icon_path: Path = get_resource_path("icon.ico")

    icon_workflow_path: Path = get_resource_path("generation/icon.json")
    default_icon_workflow: str = get_resource_file_content(icon_workflow_path)

    default_concept_temperature: float = 0.7
    default_concept_top_p: float = 0.9

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
