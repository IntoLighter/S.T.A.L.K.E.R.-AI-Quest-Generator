from dataclasses import dataclass

from PIL import Image
from pydantic import BaseModel, Field


class Objective(BaseModel):
    title: str = Field(alias="название")
    description: str = Field(alias="описание")


class Metadata(BaseModel):
    title: str = Field(alias="название")
    description: str = Field(alias="описание")
    objectives: list[Objective] = Field(alias="задачи")


@dataclass
class GameRecords:
    task: str
    article: str
    infoportions: str


@dataclass
class IconRecords:
    icon: Image.Image
    icon_soc: Image.Image


@dataclass
class GenerationResult:
    concept: str | None = None
    metadata_text: str | None = None
    metadata: Metadata | None = None
    game_records: GameRecords | None = None
    icon_prompt: str | None = None
    icon_records: IconRecords | None = None


@dataclass
class ConfiguratorParameters:
    should_generate_concept: bool
    should_generate_metadata: bool
    should_generate_icon: bool

    prompt: str
    concept: str
    metadata: str
    icon_prompt: str
