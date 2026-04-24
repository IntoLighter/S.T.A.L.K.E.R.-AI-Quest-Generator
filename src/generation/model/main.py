from typing import Iterator
import openai
from openai.types.chat import ChatCompletionMessageParam


class Model(openai.OpenAI):
    def __init__(self, model: str, base_url: str, api_key: str) -> None:
        super().__init__(api_key=api_key, base_url=base_url)
        self.model = model

    def generate(
        self, messages: list[ChatCompletionMessageParam], **kwargs
    ) -> Iterator[str]:
        stream = self.chat.completions.create(
            model=self.model, messages=messages, stream=True, **kwargs
        )
        for response in stream:
            yield response.choices[0].delta.content or ""

    def get_models(self) -> list[str]:
        return [model.id for model in self.models.list().data]
