from dataclasses import dataclass

from PIL import Image
from pydantic import BaseModel


class Objective(BaseModel):
    title: str
    description: str


class Metadata(BaseModel):
    title: str
    description: str
    objectives: list[Objective]


@dataclass
class QuestData:
    task: str
    article: str
    infoportions: str


@dataclass
class IconRecords:
    icon: Image.Image
    icon_game: Image.Image


@dataclass
class GenerationResult:
    concept: str | None = None
    metadata_text: str | None = None
    metadata: Metadata | None = None
    quest_data: QuestData | None = None
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
