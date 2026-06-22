import asyncio
import json
import traceback
from contextlib import suppress
from io import BytesIO

import openai
import requests
from comfykit import ComfyKit
from deep_translator import GoogleTranslator
from loguru import logger
from PIL import Image
from PySide6.QtCore import QObject, Signal, Slot

from config.preferences import PreferencesConfig
from generation.engine.soc import SoCObjectFactory
from generation.entity import GameRecords, GenerationResult, IconRecords, Metadata
from generation.model.main import Model
from misc import (
    ErrorInfo,
    IconGenerationError,
    get_unique_counter_name_path,
    get_unique_name_path,
    log_execution,
)


class Worker(QObject):
    concept_chunk_ready = Signal(str)
    metadata_chunk_ready = Signal(str)
    metadata_ready = Signal(str)
    game_records_ready = Signal(GameRecords)
    icon_prompt_chunk_ready = Signal(str)
    icon_ready = Signal(IconRecords)
    status_update = Signal(str)
    error_occurred = Signal(ErrorInfo)
    unknown_error_occurred = Signal(str)
    finished = Signal()

    def __init__(
        self, preferences_config: PreferencesConfig, text_model: Model, prompt: str
    ) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.text_model = text_model
        self.quest_prompt = prompt
        self.is_interruption_requested = False

    @Slot()
    def run(self) -> None:
        try:
            result = self.perform_work()
            self.save_on_disk(result)
        except Exception as e:
            self.handle_unknown_exception(e)
        finally:
            self.status_update.emit("")
            self.finished.emit()

    def perform_work(self) -> GenerationResult:
        return GenerationResult()

    def handle_exception_perform_work(self, e: Exception) -> None:
        match e:
            case openai.APIConnectionError():
                self.handle_exception(
                    e,
                    "Ошибка подключения."
                    + "Проверьте запущена ли программа генерации текста.",
                )
            case openai.APIError():
                self.handle_exception(
                    e, "Ошибка генерации текста. Проверьте вывод программы генерации."
                )
            case IconGenerationError():
                self.handle_exception(
                    e, "Возникла ошибка генерации изображения.", str(e)
                )
            case _:
                self.handle_unknown_exception(e)

    def handle_exception(
        self, e: Exception, msg: str, details: str | None = None
    ) -> None:
        if not details:
            details = traceback.format_exc()
        logger.exception(e)
        self.error_occurred.emit(ErrorInfo(msg, details))

    def handle_unknown_exception(self, e: Exception) -> None:
        logger.exception(e)
        self.unknown_error_occurred.emit(traceback.format_exc())

    @log_execution
    def create_concept(self) -> str | None:
        self.status_update.emit("Генерация концепта")

        messages = [
            {
                "role": "system",
                "content": self.preferences_config.concept_prompt,
            },
            {
                "role": "user",
                "content": self.quest_prompt,
            },
        ]

        concept = ""

        for token in self.text_model.generate(messages):
            if self.is_interruption_requested:
                return

            concept += token
            self.concept_chunk_ready.emit(token)

        return concept

    @log_execution
    def create_metadata_text(self, concept: str) -> str | None:
        self.status_update.emit("Генерация метаданных")

        messages = [
            {
                "role": "system",
                "content": self.preferences_config.metadata_prompt,
            },
            {"role": "user", "content": concept},
        ]

        metadata = ""

        for token in self.text_model.generate(messages, schema=Metadata):
            if self.is_interruption_requested:
                return

            metadata += token
            self.metadata_chunk_ready.emit(token)

        with suppress(Exception):
            parsed = json.loads(metadata)
            formatted = json.dumps(parsed, ensure_ascii=False, indent=2)
            metadata = formatted
            self.metadata_ready.emit(metadata)

        return metadata

    def create_metadata(self, metadata_text: str) -> Metadata | None:
        try:
            return Metadata.model_validate_json(metadata_text)
        except Exception as e:
            self.handle_exception(
                e,
                "Невалидный json метаданных."
                + "Попробуйте исправить json через соотвествующие сайты "
                + "и прогоните его через конфигуратор.",
            )

    @log_execution
    def create_title_english(self, title: str) -> str:
        try:
            title_english = GoogleTranslator(source="ru", target="en").translate(title)
        except Exception as e:
            self.handle_exception(
                e, "Ошибка гугл переводчика. Название не будет переведено."
            )
            title_english = title

        title_english = title_english.lower()
        title_english = title_english.replace(" ", "_")
        return title_english

    @log_execution
    def create_icon_prompt(self, concept: str) -> str | None:
        self.status_update.emit("Генерация промпта иконки")

        messages = [
            {
                "role": "system",
                "content": self.preferences_config.icon_prompt,
            },
            {
                "role": "user",
                "content": concept,
            },
        ]

        icon_prompt = ""

        for token in self.text_model.generate(messages):
            if self.is_interruption_requested:
                return

            icon_prompt += token
            self.icon_prompt_chunk_ready.emit(token)

        return icon_prompt

    @log_execution
    def create_icon_records(self, icon_prompt: str) -> IconRecords | None:
        self.status_update.emit("Генерация иконки")

        kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                kit.execute_json(
                    json.loads(self.preferences_config.icon_workflow),
                    {"prompt": icon_prompt},
                )
            )
        finally:
            loop.close()

        if result.status == "error":
            raise IconGenerationError(result.msg)

        response = requests.get(result.images[0])
        response.raise_for_status()
        icon = Image.open(BytesIO(response.content))

        icon_soc = SoCObjectFactory.create_icon(icon)
        icon_records = IconRecords(icon, icon_soc)
        self.icon_ready.emit(icon_records)

        return icon_records

    @log_execution
    def save_on_disk(self, result: GenerationResult) -> None:
        self.status_update.emit("Сохранение данных")

        if not self.preferences_config.save_path:
            return

        if result.metadata:
            quest_path = get_unique_name_path(
                self.preferences_config.save_path / result.metadata.title
            )
        else:
            quest_path = get_unique_counter_name_path(self.preferences_config.save_path)

        quest_path.mkdir(parents=True)

        generation_path = quest_path / "generation"
        generation_path.mkdir(parents=True)

        resource_path = quest_path / "resource"
        resource_path.mkdir(parents=True)

        try:
            quest_prompt_path = quest_path / "prompt.txt"
            quest_prompt_path.write_text(self.quest_prompt, encoding="utf-8")
        except Exception as e:
            self.handle_unknown_exception(e)

        if result.concept:
            try:
                concept_path = generation_path / "concept.txt"
                concept_path.write_text(result.concept, encoding="utf-8")
            except Exception as e:
                self.handle_unknown_exception(e)

        if result.metadata_text:
            try:
                metadata_path = generation_path / "metadata.json"
                metadata_path.write_text(result.metadata_text, encoding="utf-8")
            except Exception as e:
                self.handle_unknown_exception(e)

        if result.game_records:
            try:
                task_path = resource_path / "task.xml"
                task_path.write_text(result.game_records.task, encoding="cp1251")
            except Exception as e:
                self.handle_unknown_exception(e)

            try:
                article_path = resource_path / "storyline_info.xml"
                article_path.write_text(result.game_records.article, encoding="cp1251")
            except Exception as e:
                self.handle_unknown_exception(e)

            try:
                infoportions_path = resource_path / "info.xml"
                infoportions_path.write_text(
                    result.game_records.infoportions, encoding="cp1251"
                )
            except Exception as e:
                self.handle_unknown_exception(e)

        if result.icon_prompt:
            try:
                icon_prompt_path = generation_path / "icon_prompt.txt"
                icon_prompt_path.write_text(result.icon_prompt, encoding="utf-8")
            except Exception as e:
                self.handle_unknown_exception(e)

        if result.icon_records:
            try:
                icon_path = generation_path / "icon.png"
                result.icon_records.icon.save(icon_path)
            except Exception as e:
                self.handle_unknown_exception(e)

            try:
                icon_soc_path = resource_path / "icon.png"
                result.icon_records.icon_soc.save(icon_soc_path)
            except Exception as e:
                self.handle_unknown_exception(e)
