import json
import re
from collections.abc import Callable

from config.constants.main import constants_config
from PySide6.QtCore import QObject

from generation.entity import Metadata
from generation.models.text.main import TextModel
from generation.stages.base import TextGenerationStage, TextStreamingStage

ID_PATTERN = re.compile(r"[a-z](?:[a-z0-9_]*[a-z0-9])?")

# fmt: off
TRANSLITERATION = str.maketrans(
    {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
)
# fmt: on


class MetadataTextStage(TextStreamingStage):
    def __init__(
        self,
        text_model: TextModel,
        is_interrupted: Callable[[], bool],
        system_prompt: str,
        emit_chunk: Callable[[str], None],
        emit_metadata_ready: Callable[[str], None],
        emit_status: Callable[[str], None],
        handle_exception: Callable[[Exception, str, str | None], None],
        status_message: str,
    ) -> None:
        super().__init__(
            text_model,
            is_interrupted,
            system_prompt,
            emit_chunk,
            emit_status,
            status_message,
        )
        self.emit_metadata_ready = emit_metadata_ready
        self.handle_exception = handle_exception

    def create(self, concept: str) -> str | None:
        metadata = super().create(concept, schema=Metadata)

        if metadata is None:
            return None

        formatted = self._format(metadata)

        if formatted is None:
            return metadata

        self.emit_metadata_ready(formatted)
        return formatted

    def _format(self, metadata: str) -> str | None:
        try:
            parsed = json.loads(metadata)
            return json.dumps(parsed, ensure_ascii=False, indent=2)
        except Exception as e:
            self.handle_exception(e, self.tr("Ошибка форматирования метаданных."))
            return None


class MetadataParseStage(QObject):
    def __init__(
        self,
        handle_exception: Callable[[Exception, str, str | None], None],
    ) -> None:
        super().__init__()
        self.handle_exception = handle_exception

    def parse(self, metadata_text: str) -> Metadata | None:
        try:
            return Metadata.model_validate_json(metadata_text)
        except Exception as e:
            self.handle_exception(
                e,
                self.tr("Невалидный json метаданных.")
                + self.tr("Попробуйте исправить json через соотвествующие сайты ")
                + self.tr("и прогоните его через конфигуратор."),
            )
        return None


class IdStage(TextGenerationStage):
    def __init__(
        self,
        text_model: TextModel,
        system_prompt: str,
        emit_status: Callable[[str], None],
        handle_exception: Callable[[Exception, str, str | None], None],
        status_message: str,
    ) -> None:
        super().__init__(
            text_model=text_model,
            system_prompt=system_prompt,
            emit_status=emit_status,
            status_message=status_message,
        )
        self.handle_exception = handle_exception

    def create(self, title: str) -> str:
        try:
            quest_id = super().create(title).strip()
            if not self._is_valid(quest_id):
                raise ValueError(f"Invalid quest ID: {quest_id!r}")
            return quest_id
        except Exception as e:
            self.handle_exception(
                e, self.tr("Ошибка генерации ID квеста. Используется fallback.")
            )
            return self._create_fallback(title)

    def _is_valid(self, quest_id: str) -> bool:
        return (
            len(quest_id) <= constants_config.generation.quest_id_max_length
            and ID_PATTERN.fullmatch(quest_id) is not None
        )

    def _create_fallback(self, title: str) -> str:
        max_length = constants_config.generation.quest_id_max_length
        fallback = constants_config.generation.quest_id_fallback

        transliterated = title.lower().translate(TRANSLITERATION)
        quest_id = re.sub(r"[^a-z0-9]+", "_", transliterated).strip("_")
        quest_id = quest_id[:max_length].rstrip("_")

        if not quest_id:
            return fallback

        if not quest_id[0].isalpha():
            quest_id = f"{fallback}_{quest_id}"[:max_length].rstrip("_")

        return quest_id
