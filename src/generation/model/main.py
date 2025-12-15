from typing import Mapping, Union

import httpx
import openai
from httpx import Timeout
from openai import DEFAULT_MAX_RETRIES, NOT_GIVEN, NotGiven


class Model(openai.OpenAI):
    def __init__(
        self,
        model: str,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        webhook_secret: str | None = None,
        base_url: str | httpx.URL | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        super().__init__(
            api_key=api_key,
            organization=organization,
            project=project,
            webhook_secret=webhook_secret,
            base_url=base_url,
            websocket_base_url=websocket_base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )

        self.model = model

    def generate(self, messages, **kwargs):
        stream = self.chat.completions.create(
            model=self.model, messages=messages, stream=True, **kwargs
        )
        for response in stream:
            yield response.choices[0].delta.content or ""
