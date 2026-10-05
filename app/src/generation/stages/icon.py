from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject
from util.logging import log_execution

from generation.engine.soc import SoCObjectFactory
from generation.entity import IconRecords
from generation.model.image.main import ImageModel
from generation.model.text.main import TextModel
from generation.stages.streaming import stream_text


class IconPromptStage(QObject):
    def __init__(
        self,
        text_model: TextModel,
        is_interrupted: Callable[[], bool],
        system_prompt: str,
        emit_chunk: Callable[[str], None],
        emit_status: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.text_model = text_model
        self.is_interrupted = is_interrupted
        self.system_prompt = system_prompt
        self.emit_chunk = emit_chunk
        self.emit_status = emit_status

    @log_execution
    def generate(self, concept: str | None) -> str | None:
        self.emit_status(self.tr("Генерация промпта иконки"))

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": concept},
        ]

        return stream_text(
            self.text_model, self.is_interrupted, messages, self.emit_chunk
        )


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
