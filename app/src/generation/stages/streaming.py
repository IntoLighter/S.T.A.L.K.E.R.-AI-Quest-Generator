from collections.abc import Callable

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from generation.model.text.main import TextModel


def stream_text(
    text_model: TextModel,
    is_interrupted: Callable[[], bool],
    messages: list[ChatCompletionMessageParam],
    emit_chunk: Callable[[str], None],
    schema: type[BaseModel] | None = None,
) -> str | None:
    text = ""

    for token in text_model.generate(messages, schema=schema):
        if is_interrupted():
            return None

        text += token
        emit_chunk(token)

    return text
