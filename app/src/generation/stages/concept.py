from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject
from util.logging import log_execution

from generation.model.text.main import TextModel
from generation.stages.streaming import stream_text


class ConceptStage(QObject):
    def __init__(
        self,
        text_model: TextModel,
        is_interrupted: Callable[[], bool],
        system_prompt: str,
        quest_prompt: str,
        emit_chunk: Callable[[str], None],
        emit_status: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.text_model = text_model
        self.is_interrupted = is_interrupted
        self.system_prompt = system_prompt
        self.quest_prompt = quest_prompt
        self.emit_chunk = emit_chunk
        self.emit_status = emit_status

    @log_execution
    def generate(self) -> str | None:
        self.emit_status(self.tr("Генерация концепта"))

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.quest_prompt},
        ]

        return stream_text(
            self.text_model, self.is_interrupted, messages, self.emit_chunk
        )
