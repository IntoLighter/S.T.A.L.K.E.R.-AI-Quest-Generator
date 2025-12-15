from config.preferences import PreferencesConfig

from generation.model.main import Model


class LocalModel(Model):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.local_model,
            base_url="http://127.0.0.1:11434/v1",
            api_key="",
        )
