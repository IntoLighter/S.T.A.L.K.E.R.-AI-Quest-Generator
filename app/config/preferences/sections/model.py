from pydantic import BaseModel

from config.constants.main import constants_config
from config.preferences.sections.types import ModelType, TextOption
from config.utils.mixins import CodeDefaultSectionMixin


class ModelConfig(CodeDefaultSectionMixin, BaseModel):
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

    icon_workflow: TextOption = TextOption(
        system=constants_config.resources.default_icon_workflow
    )
