from pydantic import BaseModel

from config.constants.main import constants_config
from config.preferences.sections.types import TextOption
from config.utils.mixins import CodeDefaultSectionMixin


class PromptConfig(CodeDefaultSectionMixin, BaseModel):
    concept: TextOption = TextOption(
        system=constants_config.resources.default_concept_prompt
    )
    metadata: TextOption = TextOption(
        system=constants_config.resources.default_metadata_prompt
    )
    id: TextOption = TextOption(system=constants_config.resources.default_id_prompt)
    icon: TextOption = TextOption(system=constants_config.resources.default_icon_prompt)
