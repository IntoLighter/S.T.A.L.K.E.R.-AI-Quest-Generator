import traceback

import openai
from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from loguru import logger
from PySide6.QtCore import QObject, Signal, Slot
from util.error import (
    ErrorInfo,
)
from util.logging import log_execution

from generation.engine.soc import SoCObjectFactory
from generation.entity import GameRecords, GenerationResult, IconRecords
from generation.errors import ImageGenerationError
from generation.model.image.main import ImageModel
from generation.model.text.main import TextModel
from generation.services.saving import QuestSaver
from generation.stages.concept import ConceptStage
from generation.stages.icon import IconPromptStage, IconRecordsStage
from generation.stages.metadata import (
    MetadataParseStage,
    MetadataTextStage,
    TitleStage,
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
            quest_prompt=prompt,
            emit_chunk=self.concept_chunk_ready.emit,
            emit_status=self.status_update.emit,
        )
        self.metadata_text_stage = MetadataTextStage(
            text_model=text_model,
            is_interrupted=self._is_interrupted,
            system_prompt=preferences_config.prompt.metadata.value,
            emit_chunk=self.metadata_chunk_ready.emit,
            emit_metadata_ready=self.metadata_ready.emit,
            emit_status=self.status_update.emit,
        )
        self.metadata_parse_stage = MetadataParseStage(
            handle_exception=self.handle_exception,
        )
        self.title_stage = TitleStage(
            handle_exception=self.handle_exception,
        )
        self.icon_prompt_stage = IconPromptStage(
            text_model=text_model,
            is_interrupted=self._is_interrupted,
            system_prompt=preferences_config.prompt.icon.value,
            emit_chunk=self.icon_prompt_chunk_ready.emit,
            emit_status=self.status_update.emit,
        )
        self.icon_records_stage = IconRecordsStage(
            image_model=self.image_model,
            emit_status=self.status_update.emit,
            emit_icon_ready=self.icon_ready.emit,
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

        try:
            result.metadata_text = self.build_metadata_text(result.concept)

            if self._is_interrupted():
                return result

            if result.metadata_text is not None:
                result.metadata = self.metadata_parse_stage.parse(result.metadata_text)

            if result.metadata:
                title_english = self.title_stage.translate(result.metadata.title)
                result.game_records = SoCObjectFactory.create_game_records(
                    result.metadata, title_english
                )
                self.game_records_ready.emit(result.game_records)
        except Exception as e:
            self.handle_stage_exception(e)

        try:
            result.icon_prompt = self.build_icon_prompt(result.concept)

            if self._is_interrupted():
                return result

            if result.icon_prompt and self.should_generate_icons:
                result.icon_records = self.icon_records_stage.generate(
                    result.icon_prompt
                )
        except Exception as e:
            self.handle_stage_exception(e)

        return result

    def build_concept(self) -> str | None:
        raise NotImplementedError

    def build_metadata_text(self, concept: str | None) -> str | None:
        raise NotImplementedError

    def build_icon_prompt(self, concept: str | None) -> str | None:
        raise NotImplementedError

    @property
    def should_generate_icons(self) -> bool:
        raise NotImplementedError

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

    @log_execution
    def save_on_disk(self, result: GenerationResult) -> None:
        self.status_update.emit(self.tr("Сохранение данных"))

        save_path = self.preferences_config.general.save_path

        if not save_path:
            return

        saver = QuestSaver(
            save_path=save_path,
            quest_prompt=self.quest_prompt,
            on_error=self.handle_unknown_exception,
        )
        saver.save(result)
