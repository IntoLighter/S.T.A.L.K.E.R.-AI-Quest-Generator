from pathlib import Path

from config.preferences.main import PreferencesConfig


class PreferencesRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> PreferencesConfig:
        if not self._path.exists():
            return PreferencesConfig()

        return PreferencesConfig.model_validate_json(
            self._path.read_text(encoding="utf-8")
        )

    def save(self, preferences: PreferencesConfig) -> None:
        self._path.write_text(preferences.model_dump_json(indent=2), encoding="utf-8")


preferences_repository = PreferencesRepository(Path("preferences.json"))
