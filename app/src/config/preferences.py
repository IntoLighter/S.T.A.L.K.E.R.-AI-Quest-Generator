import enum
from enum import Enum, auto
from pathlib import Path
from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import constants_config
from config.text import text_config


class ModelType(Enum):
    Local = auto()
    Remote = auto()


class ValueSource(enum.StrEnum):
    SYSTEM = "system"
    CUSTOM = "custom"


class PreferencesConfig(BaseSettings):
    model_config = SettingsConfigDict(
        protected_namespaces=("settings_",),
        extra="ignore",
        validate_by_name=True,
    )

    should_generate_concept: bool = True
    should_generate_metadata: bool = True
    should_generate_icon: bool = True

    prompt_message: str = text_config.default_prompt
    save_path: Path | None = None

    model_type: ModelType = ModelType.Local
    local_model: str = ""
    remote_model: str = ""

    @property
    def current_model(self) -> str:
        type_to_value = {
            ModelType.Local: self.local_model,
            ModelType.Remote: self.remote_model,
        }

        return type_to_value[self.model_type]

    icon_workflow_source: ValueSource = ValueSource.SYSTEM
    custom_icon_workflow: str = constants_config.default_icon_workflow

    @property
    def icon_workflow(self) -> str:
        if self.icon_workflow_source == ValueSource.SYSTEM:
            return constants_config.default_icon_workflow
        else:
            return self.custom_icon_workflow

    concept_prompt_source: ValueSource = ValueSource.SYSTEM
    custom_concept_prompt: str = constants_config.default_concept_prompt

    @property
    def concept_prompt(self) -> str:
        if self.concept_prompt_source == ValueSource.SYSTEM:
            return constants_config.default_concept_prompt
        else:
            return self.custom_concept_prompt

    metadata_prompt_source: ValueSource = ValueSource.SYSTEM
    custom_metadata_prompt: str = constants_config.default_metadata_prompt

    @property
    def metadata_prompt(self) -> str:
        if self.metadata_prompt_source == ValueSource.SYSTEM:
            return constants_config.default_metadata_prompt
        else:
            return self.custom_metadata_prompt

    icon_prompt_source: ValueSource = ValueSource.SYSTEM
    custom_icon_prompt: str = constants_config.default_icon_prompt

    @property
    def icon_prompt(self) -> str:
        if self.icon_prompt_source == ValueSource.SYSTEM:
            return constants_config.default_icon_prompt
        else:
            return self.custom_icon_prompt

    configurator_concept: str = ""
    configurator_metadata: str = ""
    configurator_icon_prompt: str = ""

    @classmethod
    def load(cls) -> Self:
        if constants_config.preferences_path.exists():
            try:
                instance = cls.model_validate_json(
                    constants_config.preferences_path.read_text(encoding="utf-8")
                )
            except:
                if not __debug__:
                    constants_config.preferences_path.unlink()
                raise
        else:
            instance = cls()

        return instance

    def save(self) -> None:
        constants_config.preferences_path.write_text(
            self.model_dump_json(indent=2), encoding="utf-8"
        )
