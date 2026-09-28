from enum import Enum, auto
from typing import Self

from pydantic import BaseModel, Field, model_validator

from config.constants.main import constants_config
from config.preferences.sections.prompt import TextOption


class ModelType(Enum):
    Local = auto()
    Remote = auto()


class ModelConfig(BaseModel):
    text_model_type: ModelType = ModelType.Local
    text_model_local: str = ""
    text_model_remote: str = ""

    @property
    def current_text_model(self) -> str:
        type_to_value = {
            ModelType.Local: self.text_model_local,
            ModelType.Remote: self.text_model_remote,
        }
        return type_to_value[self.text_model_type]

    icon_workflow: TextOption = Field(default_factory=TextOption)

    @model_validator(mode="after")
    def fill_systems(self) -> Self:
        self.icon_workflow.system = constants_config.resources.default_icon_workflow
        return self
