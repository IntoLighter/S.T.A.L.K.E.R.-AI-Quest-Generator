from collections.abc import Callable

from PIL import Image
from PySide6.QtCore import QObject
from utils.logging import log_execution

from generation.entity import IconRecords
from generation.models.image.main import ImageModel
from generation.stages.base import TextStreamingStage

ICON_SOC_SIZE = (83, 47)


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
        icon_soc = icon.resize(ICON_SOC_SIZE, Image.Resampling.LANCZOS)
        icon_records = IconRecords(icon=icon, icon_soc=icon_soc)
        self.emit_icon_ready(icon_records)
        return icon_records
