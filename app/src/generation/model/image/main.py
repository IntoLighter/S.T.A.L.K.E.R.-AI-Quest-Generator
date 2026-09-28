import asyncio
import json
from io import BytesIO

import requests
from comfykit import ComfyKit
from config.endpoints import endpoints_config
from config.preferences import PreferencesConfig
from PIL import Image

from generation.errors import ImageGenerationError


class ImageModel:
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        self.kit = ComfyKit(comfyui_url=endpoints_config.comfy_ui_base_url)
        self.preferences_config = preferences_config

    def generate(self, prompt: str) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.kit.execute_json(
                    json.loads(self.preferences_config.icon_workflow.value),
                    {"prompt": prompt},
                )
            )
        finally:
            loop.close()

        if result.status == "error":
            raise ImageGenerationError(result.msg)

        response = requests.get(result.images[0])
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        return image
