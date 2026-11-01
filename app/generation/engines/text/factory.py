from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from config.preferences.sections.types import ModelType

from generation.engines.text.main import TextEngine


def create_text_engine(
    model_type: ModelType, preferences_config: PreferencesConfig
) -> TextEngine:
    endpoints = constants_config.endpoints

    match model_type:
        case ModelType.Local:
            return TextEngine(
                model=preferences_config.model.text_model_local,
                base_url=endpoints.local_model_base_url,
                api_key=endpoints.local_model_api_key,
            )
        case ModelType.Remote:
            return TextEngine(
                model=preferences_config.model.text_model_remote,
                base_url=endpoints.remote_model_base_url,
                api_key=endpoints.remote_model_api_key,
            )
