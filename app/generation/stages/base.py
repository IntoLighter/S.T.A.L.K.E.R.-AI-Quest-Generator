from collections.abc import Callable

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel
from utils.logging import log_execution

from generation.engines.text.main import TextEngine


class TextStage:
    schema: type[BaseModel] | None = None

    def __init__(
        self,
        text_engine: TextEngine,
        system_prompt: str,
        emit_status: Callable[[str], None],
        status_message: str,
    ) -> None:
        self.text_engine = text_engine
        self.system_prompt = system_prompt
        self.emit_status = emit_status
        self.status_message = status_message

    def _build_messages(self, user_content: str) -> list[ChatCompletionMessageParam]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]


class TextStreamingStage(TextStage):
    def __init__(
        self,
        text_engine: TextEngine,
        system_prompt: str,
        emit_chunk: Callable[[str], None],
        emit_status: Callable[[str], None],
        status_message: str,
    ) -> None:
        super().__init__(text_engine, system_prompt, emit_status, status_message)
        self.emit_chunk = emit_chunk

    @log_execution
    def create(self, user_content: str, /) -> str:
        self.emit_status(self.status_message)

        text = ""

        for token in self.text_engine.stream(
            self._build_messages(user_content), schema=self.schema
        ):
            text += token
            self.emit_chunk(token)

        return text


class TextGenerationStage(TextStage):
    @log_execution
    def create(self, user_content: str, /) -> str:
        self.emit_status(self.status_message)

        return self.text_engine.generate(
            self._build_messages(user_content), schema=self.schema
        )
