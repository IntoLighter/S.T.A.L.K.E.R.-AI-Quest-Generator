from config.constants.main import constants_config
from config.preferences.sections.types import Language

GENERATION_LANGUAGE_NAMES = {
    Language.EN: "English",
    Language.RU: "Russian",
}


def add_generation_language(system_prompt: str, language: Language) -> str:
    instruction = constants_config.resources.generation_language_prompt.format(
        language=GENERATION_LANGUAGE_NAMES[language]
    )
    return f"{system_prompt.rstrip()}\n\n{instruction.strip()}"
