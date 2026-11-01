from pathlib import Path

from pydantic import BaseModel

from config.preferences.sections.types import Language


class GeneralConfig(BaseModel):
    interface_language: Language = Language.EN
    generation_language: Language = Language.EN
    show_notifications: bool = True

    should_generate_concept: bool = True
    should_generate_metadata: bool = True
    should_generate_icon: bool = True

    save_path: Path | None = None
