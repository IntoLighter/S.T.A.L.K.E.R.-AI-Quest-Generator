from config.constants import constants_config
from config.preferences import PreferencesConfig
from generation.model.text.main import TextModel


class LocalTextModel(TextModel):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.local_model,
            base_url=constants_config.local_model_base_url,
            api_key=constants_config.local_model_api_key,
        )
