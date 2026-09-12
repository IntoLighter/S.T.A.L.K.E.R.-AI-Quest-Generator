from config.constants import constants_config
from config.preferences import PreferencesConfig
from generation.model.main import Model


class RemoteModel(Model):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.remote_model,
            base_url=constants_config.remote_model_base_url,
            api_key=constants_config.remote_model_api_key,
        )
