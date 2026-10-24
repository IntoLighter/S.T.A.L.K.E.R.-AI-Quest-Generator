import json
from collections.abc import Callable

from PySide6.QtCore import QObject

from generation.entity import Metadata
from generation.models.text.main import TextModel
from generation.stages.base import TextGenerationStage, TextStreamingStage


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
            return super().create(title).strip()
        except Exception as e:
            self.handle_exception(
                e, self.tr("Ошибка генерации ID квеста. Используется fallback.")
            )
            return title.lower().replace(" ", "_").replace("'", "").replace('"', "")
