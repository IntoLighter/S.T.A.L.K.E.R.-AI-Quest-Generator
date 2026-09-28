from pathlib import Path

from config.constants.main import constants_config
from config.preferences import PreferencesConfig


class PreferencesRepository:
    def load(self) -> PreferencesConfig:
        if not self.path.exists():
            return PreferencesConfig()

        return PreferencesConfig.model_validate_json(
            self.path.read_text(encoding="utf-8")
        )

    def save(self, preferences: PreferencesConfig) -> None:
        self.path.write_text(preferences.model_dump_json(indent=2), encoding="utf-8")

    @property
    def path(self) -> Path:
        return constants_config.paths.preferences_path


preferences_repository = PreferencesRepository()
