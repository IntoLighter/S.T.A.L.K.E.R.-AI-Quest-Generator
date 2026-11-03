from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig

from generation.engines.image.main import ImageEngine


def create_image_engine(preferences_config: PreferencesConfig) -> ImageEngine:
    return ImageEngine(
        workflow=preferences_config.model.icon_workflow.value,
        comfyui_url=constants_config.endpoints.comfyui_base_url,
    )
