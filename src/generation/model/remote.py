from config.preferences import PreferencesConfig

from generation.model.main import Model


class RemoteModel(Model):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__(
            model=preferences_config.remote_model,
            base_url="http://127.0.0.1:8000/v1",
            api_key="VerysecretKey",
        )
