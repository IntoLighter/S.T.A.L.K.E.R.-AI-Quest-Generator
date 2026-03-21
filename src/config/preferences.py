from enum import Enum, auto
from pathlib import Path
from typing import Self

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import constants_config
from config.text import text_config


class ModelType(Enum):
    Local = auto()
    Remote = auto()


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
    local_model: str = text_config.default_local_model
    remote_model: str = text_config.default_remote_model

    @property
    def current_model(self) -> str:
        type_to_value = {
            ModelType.Local: self.local_model,
            ModelType.Remote: self.remote_model,
        }

        return type_to_value[self.model_type]

    concept_temperature: float = constants_config.default_concept_temperature
    concept_top_p: float = constants_config.default_concept_top_p

    icon_workflow_value: str = Field(
        default=constants_config.default_icon_workflow, alias="icon_workflow"
    )

    @property
    def icon_workflow(self) -> str:
        if __debug__:
            return constants_config.default_icon_workflow
        else:
            return self.icon_workflow_value

    @icon_workflow.setter
    def icon_workflow(self, value: str) -> None:
        self.icon_workflow_value = value

    concept_prompt_value: str = Field(
        default=constants_config.default_concept_prompt, alias="concept_prompt"
    )
    metadata_prompt_value: str = Field(
        default=constants_config.default_metadata_prompt, alias="metadata_prompt"
    )
    icon_prompt_value: str = Field(
        default=constants_config.default_icon_prompt, alias="icon_prompt"
    )

    @property
    def concept_prompt(self) -> str:
        if __debug__:
            return constants_config.default_concept_prompt
        else:
            return self.concept_prompt_value

    @concept_prompt.setter
    def concept_prompt(self, value: str) -> None:
        self.concept_prompt_value = value

    @property
    def metadata_prompt(self) -> str:
        if __debug__:
            return constants_config.default_metadata_prompt
        else:
            return self.metadata_prompt_value

    @metadata_prompt.setter
    def metadata_prompt(self, value: str) -> None:
        self.metadata_prompt_value = value

    @property
    def icon_prompt(self) -> str:
        if __debug__:
            return constants_config.default_icon_prompt
        else:
            return self.icon_prompt_value

    @icon_prompt.setter
    def icon_prompt(self, value: str) -> None:
        self.icon_prompt_value = value

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
