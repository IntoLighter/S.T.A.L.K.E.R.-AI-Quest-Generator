from collections.abc import Callable

from config.constants.main import constants_config
from utils.logging import log_execution

from generation.engines.image.main import ImageEngine
from generation.entity import IconRecords
from generation.stages.base import TextStreamingStage


class IconPromptStage(TextStreamingStage):
    pass


class IconRecordsStage:
    def __init__(
        self,
        image_engine: ImageEngine,
        emit_status: Callable[[str], None],
        emit_icon_ready: Callable[[IconRecords], None],
        status_message: str,
    ) -> None:
        self.image_engine = image_engine
        self.emit_status = emit_status
        self.emit_icon_ready = emit_icon_ready
        self.status_message = status_message

    @log_execution
    def create(self, icon_prompt: str) -> IconRecords | None:
        self.emit_status(self.status_message)
        icon = self.image_engine.generate(icon_prompt)
        icon_game = icon.resize(
            constants_config.generation.icon_game_size,
            constants_config.generation.icon_game_resampling,
        )
        icon_records = IconRecords(icon=icon, icon_game=icon_game)
        self.emit_icon_ready(icon_records)
        return icon_records
