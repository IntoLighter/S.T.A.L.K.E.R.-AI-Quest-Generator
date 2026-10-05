import enum

from pydantic import BaseModel, Field

from config.utils.mixins import CodeDefaultOptionMixin


class ModelType(enum.StrEnum):
    Local = "local"
    Remote = "remote"


class ValueSource(enum.StrEnum):
    SYSTEM = "system"
    CUSTOM = "custom"


class TextOption(CodeDefaultOptionMixin, BaseModel):
    source: ValueSource = ValueSource.SYSTEM
    system: str = Field(exclude=True)
    custom: str = ""

    @property
    def value(self) -> str:
        return self.system if self.source is ValueSource.SYSTEM else self.custom
