import enum
from enum import Enum, auto
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.resources import resources_config

DEFAULT_PROMPT = """
Тип: исследование
Квестодатель: Сидорович
""".strip()


class ModelType(Enum):
    Local = auto()
    Remote = auto()


class ValueSource(enum.StrEnum):
    SYSTEM = "system"
    CUSTOM = "custom"


class TextOption(BaseModel):
    source: ValueSource = ValueSource.SYSTEM
    system: str = Field(default="", exclude=True)
    custom: str = ""

    @property
    def value(self) -> str:
        if self.source == ValueSource.SYSTEM:
            return self.system

        return self.custom


SYSTEM_BY_OPTION: dict[str, str] = {
    "icon_workflow": resources_config.default_icon_workflow,
    "concept_prompt": resources_config.default_concept_prompt,
    "metadata_prompt": resources_config.default_metadata_prompt,
    "icon_prompt": resources_config.default_icon_prompt,
}


class PreferencesConfig(BaseSettings):
    model_config = SettingsConfigDict(
        protected_namespaces=("settings_",),
        extra="ignore",
        validate_by_name=True,
    )

    show_notifications: bool = True

    should_generate_concept: bool = True
    should_generate_metadata: bool = True
    should_generate_icon: bool = True

    prompt_message: str = DEFAULT_PROMPT
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

    icon_workflow: TextOption = Field(default_factory=TextOption)
    concept_prompt: TextOption = Field(default_factory=TextOption)
    metadata_prompt: TextOption = Field(default_factory=TextOption)
    icon_prompt: TextOption = Field(default_factory=TextOption)

    @model_validator(mode="after")
    def fill_systems(self) -> Self:
        for name, system in SYSTEM_BY_OPTION.items():
            getattr(self, name).system = system

        return self

    configurator_concept: str = ""
    configurator_metadata: str = ""
    configurator_icon_prompt: str = ""
