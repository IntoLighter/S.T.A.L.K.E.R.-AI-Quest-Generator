from typing import Iterator

from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class Model:
    def __init__(self, model: str, base_url: str, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def generate(
        self, messages: list[ChatCompletionMessageParam], retries: int = 2, **kwargs
    ) -> Iterator[str]:
        stream = self.client.with_options(max_retries=retries).chat.completions.create(
            model=self.model, messages=messages, stream=True, **kwargs
        )
        for response in stream:
            yield response.choices[0].delta.content or ""

    def get_models(self, retries: int = 0) -> list[str]:
        # TODO: Move to service
        try:
            return [
                model.id
                for model in self.client.with_options(max_retries=retries)
                .models.list()
                .data
            ]
        except Exception as e:
            logger.exception(e)
            return []
