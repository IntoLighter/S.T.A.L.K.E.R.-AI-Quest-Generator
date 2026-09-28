from pathlib import Path

from config.paths import paths_config
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
        return paths_config.preferences_path


preferences_repository = PreferencesRepository()
