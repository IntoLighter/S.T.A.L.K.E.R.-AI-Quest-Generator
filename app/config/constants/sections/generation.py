from PIL import Image
from pydantic import BaseModel


class GenerationConfig(BaseModel):
    icon_game_size: tuple[int, int] = (83, 47)
    icon_game_resampling: Image.Resampling = Image.Resampling.LANCZOS
