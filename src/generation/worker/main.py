import json
from deep_translator import GoogleTranslator
from loguru import logger
from PIL import Image
from PySide6.QtCore import QThread, Signal
import asyncio
from io import BytesIO
from comfykit import ComfyKit
import openai
import requests

from config.constants import get_resource_path
from config.preferences import PreferencesConfig
from generation.engine.soc import SoCObjectFactory
from generation.entity import GameRecords, GenerationResult, IconRecords, Metadata
from generation.model.main import Model
from misc import (
    AppError,
    get_unique_counter_name_path,
    get_unique_name_path,
    log_execution,
)


class Worker(QThread):
    concept_chunk_ready = Signal(str)
    metadata_chunk_ready = Signal(str)
    game_records_ready = Signal(GameRecords)
    icon_prompt_chunk_ready = Signal(str)
    icon_ready = Signal(Image.Image)
    status_update = Signal(str)
    error_occurred = Signal(str)

    def __init__(
        self, preferences_config: PreferencesConfig, text_model: Model, prompt: str
    ) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.text_model = text_model
        self.quest_prompt = prompt

    def run(self) -> None:
        try:
            result = self.perform_work()
            self.save_on_disk(result)
        except Exception as e:
            self.handle_exception(e, "Возникла непредвиденная ошибка.")
        finally:
            self.status_update.emit("")

    def perform_work(self) -> GenerationResult:
        return GenerationResult()

    def handle_exception_perform_work(self, e: Exception) -> None:
        match e:
            case openai.APIConnectionError():
                self.handle_exception(
                    e,
                    "Ошибка подключения. Проверьте запущена ли программа генерации текста.",
                )
            case openai.APIError():
                self.handle_exception(
                    e, "Ошибка генерации текста. Проверьте вывод программы генерации."
                )
            case AppError():
                self.handle_exception(e, str(e))
            case _:
                self.handle_exception(e, "Возникла непредвиденная ошибка.")

    def handle_exception(self, e: Exception, msg: str) -> None:
        logger.exception(e)
        self.error_occurred.emit(msg)

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

        for token in self.text_model.generate(
            messages,
            temperature=self.preferences_config.concept_temperature,
            top_p=self.preferences_config.concept_top_p,
        ):
            if self.isInterruptionRequested():
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

        for token in self.text_model.generate(
            messages,
            response_format={"type": "json_object"},
            temperature=0,
        ):
            if self.isInterruptionRequested():
                return

            metadata += token
            self.metadata_chunk_ready.emit(token)

        return metadata

    def create_metadata(self, metadata_text: str) -> Metadata | None:
        try:
            return Metadata(**(json.loads(metadata_text)))
        except json.JSONDecodeError as e:
            self.handle_exception(
                e,
                "Невалидный json метаданных. Попробуйте исправить json через соотвествующие сайты и прогоните его через конфигуратор.",
            )

    @log_execution
    def create_title_english(self, title: str) -> str:
        try:
            title_english = GoogleTranslator(source="ru", target="en").translate(title)
        except Exception as e:
            self.handle_exception(
                e, "Неизвестная ошибка перевода названия. Название не будет переведено."
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

        for token in self.text_model.generate(messages, temperature=0):
            if self.isInterruptionRequested():
                return

            icon_prompt += token
            self.icon_prompt_chunk_ready.emit(token)

        return icon_prompt

    @log_execution
    def create_icon_records(self, icon_prompt: str) -> IconRecords | None:
        self.status_update.emit("Генерация иконки")

        kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")
        result = asyncio.run(
            kit.execute_json(
                json.loads(self.preferences_config.icon_workflow),
                {"prompt": icon_prompt},
            )
        )

        if result.status == "error":
            raise AppError(f"Возникла ошибка генерации изображения: {result.msg}.")

        response = requests.get(result.images[0])
        response.raise_for_status()
        icon = Image.open(BytesIO(response.content))

        icon_soc = SoCObjectFactory.create_icon(icon)
        icon_records = IconRecords(icon, icon_soc)
        self.icon_ready.emit(icon_soc)

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

        quest_prompt_path = quest_path / "prompt.txt"
        quest_prompt_path.write_text(self.quest_prompt, encoding="cp1251")

        if result.concept:
            concept_path = quest_path / "concept.txt"
            concept_path.write_text(result.concept, encoding="cp1251")

        if result.metadata_text:
            metadata_path = quest_path / "metadata.json"
            metadata_path.write_text(result.metadata_text, encoding="cp1251")

        if result.game_records:
            task_path = quest_path / "task.xml"
            task_path.write_text(result.game_records.task, encoding="cp1251")

            article_path = quest_path / "article.xml"
            article_path.write_text(result.game_records.article, encoding="cp1251")

            infoportions_path = quest_path / "infoportions.xml"
            infoportions_path.write_text(
                result.game_records.infoportions, encoding="cp1251"
            )

        if result.icon_prompt:
            icon_prompt_path = quest_path / "icon_prompt.txt"
            icon_prompt_path.write_text(result.icon_prompt, encoding="cp1251")

        if result.icon_records:
            icon_path = quest_path / "icon.png"
            result.icon_records.icon.save(icon_path)

            icon_soc_path = quest_path / "icon_soc.png"
            result.icon_records.icon_soc.save(icon_soc_path)
