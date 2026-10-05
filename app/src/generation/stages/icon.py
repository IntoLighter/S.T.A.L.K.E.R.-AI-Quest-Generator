from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject
from util.logging import log_execution

from generation.engine.soc import SoCObjectFactory
from generation.entity import IconRecords
from generation.model.image.main import ImageModel
from generation.stages.base import TextStage


class IconPromptStage(TextStage):
    @log_execution
    def generate(self, concept: str | None) -> str | None:
        self.emit_status(self.tr("Генерация промпта иконки"))
        return self.stream(concept)


class IconRecordsStage(QObject):
    def __init__(
        self,
        image_model: ImageModel,
        emit_status: Callable[[str], None],
        emit_icon_ready: Callable[[IconRecords], None],
    ) -> None:
        super().__init__()
        self.image_model = image_model
        self.emit_status = emit_status
        self.emit_icon_ready = emit_icon_ready

    @log_execution
    def generate(self, icon_prompt: str) -> IconRecords | None:
        self.emit_status(self.tr("Генерация иконки"))
        icon = self.image_model.generate(icon_prompt)
        icon_soc = SoCObjectFactory.create_icon(icon)
        icon_records = IconRecords(icon=icon, icon_soc=icon_soc)
        self.emit_icon_ready(icon_records)
        return icon_records
