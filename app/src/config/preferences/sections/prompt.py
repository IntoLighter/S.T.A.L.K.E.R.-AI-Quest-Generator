from typing import Self

from pydantic import BaseModel, Field, model_validator

from config.constants.main import constants_config
from config.preferences.sections.types import ValueSource


class TextOption(BaseModel):
    source: ValueSource = ValueSource.SYSTEM
    system: str = Field(default="", exclude=True)
    custom: str = ""

    @property
    def value(self) -> str:
        if self.source == ValueSource.SYSTEM:
            return self.system

        return self.custom


PROMPT_SYSTEM_BY_OPTION: dict[str, str] = {
    "concept": constants_config.resources.default_concept_prompt,
    "metadata": constants_config.resources.default_metadata_prompt,
    "icon": constants_config.resources.default_icon_prompt,
}


class PromptConfig(BaseModel):
    concept: TextOption = Field(default_factory=TextOption)
    metadata: TextOption = Field(default_factory=TextOption)
    icon: TextOption = Field(default_factory=TextOption)

    @model_validator(mode="after")
    def fill_systems(self) -> Self:
        for name, system in PROMPT_SYSTEM_BY_OPTION.items():
            getattr(self, name).system = system
        return self
