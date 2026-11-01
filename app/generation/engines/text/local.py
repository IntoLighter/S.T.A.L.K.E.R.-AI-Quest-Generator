from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig

from generation.engines.text.main import TextEngine


class LocalTextEngine(TextEngine):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.model.text_model_local,
            base_url=constants_config.endpoints.local_model_base_url,
            api_key=constants_config.endpoints.local_model_api_key,
        )
