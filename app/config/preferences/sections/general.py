from pathlib import Path

from pydantic import BaseModel

from config.preferences.sections.types import Language

DEFAULT_PROMPT = """
Тип: исследование
Квестодатель: Сидорович
""".strip()


class GeneralConfig(BaseModel):
    interface_language: Language = Language.EN
    show_notifications: bool = True

    should_generate_concept: bool = True
    should_generate_metadata: bool = True
    should_generate_icon: bool = True

    prompt_message: str = DEFAULT_PROMPT
    save_path: Path | None = None
