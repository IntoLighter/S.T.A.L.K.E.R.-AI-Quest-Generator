import traceback

import openai
from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from loguru import logger
from PySide6.QtCore import QObject, Signal, Slot
from utils.error import ErrorInfo
from utils.logging import log_execution

from generation.entity import GenerationResult, IconRecords, QuestData
from generation.errors import ImageGenerationError, MetadataParseError
from generation.models.image.main import ImageModel
from generation.models.text.main import TextModel
from generation.services.quest_builder import QuestBuilder
from generation.services.saving import QuestSaver
from generation.stages.concept import ConceptStage
from generation.stages.icon import IconPromptStage, IconRecordsStage
from generation.stages.metadata import (
    IdStage,
    MetadataParseStage,
    MetadataTextStage,
)


class BaseWorker(QObject):
    concept_chunk_ready = Signal(str)
    metadata_chunk_ready = Signal(str)
    metadata_ready = Signal(str)
    quest_data_ready = Signal(QuestData)
    icon_prompt_chunk_ready = Signal(str)
    icon_ready = Signal(IconRecords)
    status_update = Signal(str)
    error_occurred = Signal(ErrorInfo)
    unknown_error_occurred = Signal(str)
    finished = Signal()

    def __init__(
        self, preferences_config: PreferencesConfig, text_model: TextModel, prompt: str
    ) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.text_model = text_model
        self.image_model = ImageModel(
            preferences_config,
            comfyui_url=constants_config.endpoints.comfyui_base_url,
        )
        self.quest_prompt = prompt
        self._is_interruption_requested = False

        self.concept_stage = ConceptStage(
            text_model=text_model,
            is_interrupted=self._is_interrupted,
            system_prompt=preferences_config.prompt.concept.value,
            emit_chunk=self.concept_chunk_ready.emit,
            emit_status=self.status_update.emit,
            status_message=self.tr("Генерация концепта"),
        )
        self.metadata_text_stage = MetadataTextStage(
            text_model=text_model,
            is_interrupted=self._is_interrupted,
            system_prompt=preferences_config.prompt.metadata.value,
            emit_chunk=self.metadata_chunk_ready.emit,
            emit_metadata_ready=self.metadata_ready.emit,
            emit_status=self.status_update.emit,
            status_message=self.tr("Генерация метаданных"),
        )
        self.metadata_parse_stage = MetadataParseStage()
        self.id_stage = IdStage(
            text_model=text_model,
            system_prompt=preferences_config.prompt.id.value,
            emit_status=self.status_update.emit,
            status_message=self.tr("Генерация ID квеста"),
        )
        self.icon_prompt_stage = IconPromptStage(
            text_model=text_model,
            is_interrupted=self._is_interrupted,
            system_prompt=preferences_config.prompt.icon.value,
            emit_chunk=self.icon_prompt_chunk_ready.emit,
            emit_status=self.status_update.emit,
            status_message=self.tr("Генерация промпта иконки"),
        )
        self.icon_records_stage = IconRecordsStage(
            image_model=self.image_model,
            emit_status=self.status_update.emit,
            emit_icon_ready=self.icon_ready.emit,
            status_message=self.tr("Генерация иконки"),
        )

    def request_interruption(self) -> None:
        logger.info("Generation canceled")
        self._is_interruption_requested = True

    def _is_interrupted(self) -> bool:
        return self._is_interruption_requested

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
        result = GenerationResult()

        try:
            result.concept = self.build_concept()
        except Exception as e:
            self.handle_stage_exception(e)
            return result

        if self._is_interrupted():
            return result

        concept = result.concept or ""

        try:
            result.metadata_text = self.build_metadata_text(concept)

            if self._is_interrupted():
                return result

            if result.metadata_text is not None:
                result.metadata = self.metadata_parse_stage.parse(result.metadata_text)

            if result.metadata:
                quest_id = self.create_quest_id(result.metadata.title)
                result.quest_data = QuestBuilder.create_quest_data(
                    result.metadata, quest_id
                )
                self.quest_data_ready.emit(result.quest_data)
        except Exception as e:
            self.handle_stage_exception(e)

        try:
            result.icon_prompt = self.build_icon_prompt(concept)

            if self._is_interrupted():
                return result

            result.icon_records = self.build_icon_records(result.icon_prompt or "")
        except Exception as e:
            self.handle_stage_exception(e)

        return result

    def build_concept(self) -> str | None:
        raise NotImplementedError

    def build_metadata_text(self, concept: str) -> str | None:
        raise NotImplementedError

    def build_icon_prompt(self, concept: str) -> str | None:
        raise NotImplementedError

    def build_icon_records(self, icon_prompt: str) -> IconRecords | None:
        raise NotImplementedError

    def create_quest_id(self, title: str) -> str:
        try:
            return self.id_stage.create(title)
        except Exception as e:
            self.handle_exception(
                e, self.tr("Ошибка генерации ID квеста. Используется fallback.")
            )
            return self.id_stage.create_fallback(title)

    def handle_stage_exception(self, e: Exception) -> None:
        match e:
            case openai.APIConnectionError():
                self.handle_exception(
                    e,
                    self.tr("Ошибка подключения.")
                    + self.tr("Проверьте запущена ли программа генерации текста."),
                )
            case openai.APIError():
                self.handle_exception(
                    e,
                    self.tr(
                        "Ошибка генерации текста. Проверьте вывод программы генерации."
                    ),
                )
            case MetadataParseError():
                self.handle_exception(
                    e,
                    self.tr("Невалидный json метаданных.")
                    + self.tr("Попробуйте исправить json через соотвествующие сайты ")
                    + self.tr("и прогоните его через конфигуратор."),
                )
            case ImageGenerationError():
                self.handle_exception(
                    e, self.tr("Возникла ошибка генерации изображения."), str(e)
                )
            case _:
                self.handle_unknown_exception(e)

    def handle_exception(
        self, e: Exception, msg: str, details: str | None = None
    ) -> None:
        if not details:
            details = traceback.format_exc()
        logger.exception(e)
        self.error_occurred.emit(ErrorInfo(msg=msg, details=details))

    def handle_unknown_exception(self, e: Exception) -> None:
        logger.exception(e)
        self.unknown_error_occurred.emit(traceback.format_exc())

    def handle_save_errors(self, errors: list[Exception]) -> None:
        msg = self.tr("Ошибки при сохранении файлов")
        details = "\n\n".join(f"{e.__class__.__name__}\n{e}" for e in errors)
        self.error_occurred.emit(ErrorInfo(msg=msg, details=details))

    @log_execution
    def save_on_disk(self, result: GenerationResult) -> None:
        save_path = self.preferences_config.general.save_path

        if not save_path:
            return

        self.status_update.emit(self.tr("Сохранение данных"))

        saver = QuestSaver(
            save_path=save_path,
            quest_prompt=self.quest_prompt,
        )
        errors = saver.save(result)

        if errors:
            self.handle_save_errors(errors)
