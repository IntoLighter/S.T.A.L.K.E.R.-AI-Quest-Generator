from collections.abc import Callable

from config.constants.main import constants_config
from PySide6.QtCore import QObject
from utils.logging import log_execution

from generation.entity import IconRecords
from generation.models.image.main import ImageModel
from generation.stages.base import TextStreamingStage


class IconPromptStage(TextStreamingStage):
    pass


class IconRecordsStage(QObject):
    def __init__(
        self,
        image_model: ImageModel,
        emit_status: Callable[[str], None],
        emit_icon_ready: Callable[[IconRecords], None],
        status_message: str,
    ) -> None:
        super().__init__()
        self.image_model = image_model
        self.emit_status = emit_status
        self.emit_icon_ready = emit_icon_ready
        self.status_message = status_message

    @log_execution
    def create(self, icon_prompt: str) -> IconRecords | None:
        self.emit_status(self.status_message)
        icon = self.image_model.generate(icon_prompt)
        icon_game = icon.resize(
            constants_config.generation.icon_game_size,
            constants_config.generation.icon_game_resampling,
        )
        icon_records = IconRecords(icon=icon, icon_game=icon_game)
        self.emit_icon_ready(icon_records)
        return icon_records
