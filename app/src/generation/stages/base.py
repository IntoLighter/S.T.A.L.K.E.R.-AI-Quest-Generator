from __future__ import annotations

from collections.abc import Callable

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel
from PySide6.QtCore import QObject

from generation.model.text.main import TextModel


class TextStage(QObject):
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

    def stream(
        self,
        user_content: str | None,
        schema: type[BaseModel] | None = None,
    ) -> str | None:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]

        text = ""

        for token in self.text_model.generate(messages, schema=schema):
            if self.is_interrupted():
                return None

            text += token
            self.emit_chunk(token)

        return text
