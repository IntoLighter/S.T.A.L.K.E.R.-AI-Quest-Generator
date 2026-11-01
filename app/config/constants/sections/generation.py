from openai.types.shared import ReasoningEffort
from PIL import Image
from pydantic import BaseModel


class GenerationConfig(BaseModel):
    text_reasoning_effort: ReasoningEffort = "none"

    icon_download_timeout: float = 60

    icon_game_size: tuple[int, int] = (83, 47)
    icon_game_resampling: Image.Resampling = Image.Resampling.LANCZOS

    generation_encoding: str = "utf-8"
    game_encoding: str = "cp1251"

    quest_id_max_length: int = 50
    quest_id_fallback: str = "quest"

    quest_dir_name_max_length: int = 100
