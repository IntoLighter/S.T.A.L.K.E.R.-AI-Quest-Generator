from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig

from generation.models.text.main import TextModel


class RemoteTextModel(TextModel):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.model.text_model_remote,
            base_url=constants_config.endpoints.remote_model_base_url,
            api_key=constants_config.endpoints.remote_model_api_key,
        )
