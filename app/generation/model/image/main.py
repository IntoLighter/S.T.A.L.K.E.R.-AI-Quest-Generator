import asyncio
import json
from io import BytesIO

import requests
from comfykit import ComfyKit
from config.preferences.main import PreferencesConfig
from PIL import Image

from generation.errors import ImageGenerationError


class ImageModel:
    def __init__(self, preferences_config: PreferencesConfig, comfyui_url: str) -> None:
        self.preferences_config = preferences_config
        self.comfyui_url = comfyui_url
        self.kit = ComfyKit(comfyui_url=self.comfyui_url)

    def generate(self, prompt: str) -> Image.Image:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.kit.execute_json(
                    json.loads(self.preferences_config.model.icon_workflow.value),
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
