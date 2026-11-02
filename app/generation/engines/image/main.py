import asyncio
import json
import random
from io import BytesIO

import requests
from comfykit import ComfyKit
from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PIL import Image

from generation.errors import ImageGenerationError


class ImageEngine:
    def __init__(self, preferences_config: PreferencesConfig, comfyui_url: str) -> None:
        self.preferences_config = preferences_config
        self.comfyui_url = comfyui_url
        self.kit = ComfyKit(comfyui_url=self.comfyui_url)

    def generate(self, prompt: str) -> Image.Image:
        try:
            workflow = json.loads(self.preferences_config.model.icon_workflow.value)
        except json.JSONDecodeError as e:
            msg = f"Invalid icon workflow JSON: {e}"
            raise ImageGenerationError(msg) from e

        seed = random.randrange(constants_config.generation.icon_seed_limit)
        result = asyncio.run(
            self.kit.execute_json(workflow, {"prompt": prompt, "seed": seed})
        )

        if result.status == "error":
            raise ImageGenerationError(result.msg)

        if not result.images:
            msg = "ComfyUI returned no images"
            raise ImageGenerationError(msg)

        try:
            response = requests.get(
                result.images[0],
                timeout=constants_config.generation.icon_download_timeout,
            )
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except (requests.RequestException, OSError) as e:
            msg = f"Failed to download icon: {e}"
            raise ImageGenerationError(msg) from e
