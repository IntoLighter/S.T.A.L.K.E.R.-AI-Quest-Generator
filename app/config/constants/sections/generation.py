from openai.types.shared import ReasoningEffort
from PIL import Image, ImageFilter
from pydantic import BaseModel, ConfigDict


class GenerationConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    text_reasoning_effort: ReasoningEffort = "none"
    text_models_list_timeout: float = 5

    icon_download_timeout: float = 60
    icon_seed_limit: int = 2**63

    icon_game_size: tuple[int, int] = (83, 47)
    icon_game_resampling: Image.Resampling = Image.Resampling.LANCZOS
    icon_game_sharpen: ImageFilter.UnsharpMask = ImageFilter.UnsharpMask(
        radius=1, percent=60, threshold=2
    )

    generation_encoding: str = "utf-8"
    game_encoding: str = "cp1251"

    quest_id_max_length: int = 50
    quest_id_fallback: str = "quest"

    quest_dir_name_max_length: int = 100
