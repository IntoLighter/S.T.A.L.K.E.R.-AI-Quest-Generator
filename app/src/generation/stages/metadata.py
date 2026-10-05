from __future__ import annotations

import json
from collections.abc import Callable

from deep_translator import GoogleTranslator
from loguru import logger
from PySide6.QtCore import QObject
from util.logging import log_execution

from generation.entity import Metadata
from generation.model.text.main import TextModel
from generation.stages.streaming import stream_text


class MetadataTextStage(QObject):
    def __init__(
        self,
        text_model: TextModel,
        is_interrupted: Callable[[], bool],
        system_prompt: str,
        emit_chunk: Callable[[str], None],
        emit_metadata_ready: Callable[[str], None],
        emit_status: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.text_model = text_model
        self.is_interrupted = is_interrupted
        self.system_prompt = system_prompt
        self.emit_chunk = emit_chunk
        self.emit_metadata_ready = emit_metadata_ready
        self.emit_status = emit_status

    @log_execution
    def generate(self, concept: str | None) -> str | None:
        self.emit_status(self.tr("Генерация метаданных"))

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": concept},
        ]

        metadata = stream_text(
            self.text_model,
            self.is_interrupted,
            messages,
            self.emit_chunk,
            schema=Metadata,
        )

        if metadata is None:
            return None

        formatted = self._format(metadata)

        if formatted is None:
            return metadata

        self.emit_metadata_ready(formatted)
        return formatted

    @staticmethod
    def _format(raw: str) -> str | None:
        try:
            parsed = json.loads(raw)
            return json.dumps(parsed, ensure_ascii=False, indent=2)
        except Exception:
            logger.debug("Failed to format metadata JSON, keeping raw text")
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


class TitleStage(QObject):
    def __init__(
        self,
        handle_exception: Callable[[Exception, str, str | None], None],
    ) -> None:
        super().__init__()
        self.handle_exception = handle_exception

    @log_execution
    def translate(self, title: str) -> str:
        try:
            title_english = GoogleTranslator(source="ru", target="en").translate(title)
        except Exception as e:
            self.handle_exception(
                e, self.tr("Ошибка гугл переводчика. Название не будет переведено.")
            )
            title_english = title

        return title_english.lower().replace(" ", "_")
