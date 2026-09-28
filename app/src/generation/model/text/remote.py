from config.endpoints import endpoints_config
from config.preferences import PreferencesConfig

from generation.model.text.main import TextModel


class RemoteTextModel(TextModel):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.remote_model,
            base_url=endpoints_config.remote_model_base_url,
            api_key=endpoints_config.remote_model_api_key,
        )
