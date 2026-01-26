from typing import Callable

from loguru import logger

from config.constants import constants_config
from config.preferences import ModelType, PreferencesConfig
from config.text import text_config
from generation.entity import ConfiguratorParameters, GameRecords
from generation.model.local import LocalModel
from generation.model.remote import RemoteModel
from generation.worker.configurator import ConfiguratorWorker
from generation.worker.normal import NormalWorker
from misc import get_layout_with_scroll, get_pixmap, show_parameters_error
from PIL import Image
from PySide6.QtCore import Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
)

from ui.editor.prompt import PromptEditor


class MainWidget(QWidget):
    def __init__(
        self, preferences_config: PreferencesConfig, show_status: Callable[[str], None]
    ) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.show_status = show_status

        self.layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor(preferences_config)
        self.layout.addWidget(self.prompt_editor)

        self.generate_button = QPushButton(text_config.generate_text)
        self.generate_button.clicked.connect(self.generate_quest_normal)
        self.layout.addWidget(self.generate_button)

        self.add_output_editors()

    def save_prompt(self) -> None:
        self.preferences_config.prompt_message = self.prompt_editor.prompt
        self.preferences_config.save()

    @Slot()
    def reset(self) -> None:
        self.prompt_editor.clear()
        self.prompt_editor.insertPlainText(self.preferences_config.prompt_message)

    @Slot()
    def generate_quest_normal(self) -> None:
        if not self.preferences_config.should_generate_concept:
            show_parameters_error(
                self,
                "Невозможно запустить генерацию с отключенной генерацией концепта.",
            )
            return

        logger.info("Normal generation started")

        self.worker = NormalWorker(
            self.preferences_config, self.get_model, self.prompt_editor.prompt
        )
        self.generate_quest()

    def generate_quest_configurator(self, parameters: ConfiguratorParameters) -> None:
        logger.info("Configurator generation started")

        self.worker = ConfiguratorWorker(
            self.preferences_config,
            self.get_model,
            parameters.prompt,
            parameters,
        )
        self.generate_quest()

    @property
    def get_model(self):
        type_to_value = {
            ModelType.Local: LocalModel(self.preferences_config),
            ModelType.Remote: RemoteModel(self.preferences_config),
        }

        return type_to_value[self.preferences_config.model_type]

    def generate_quest(self) -> None:
        self.set_generate_button_stop()
        for editor in self.output_editors:
            editor.clear()
        self.icon_editor.clear()

        self.worker.status_update.connect(self.show_status)
        self.worker.concept_chunk_ready.connect(self.show_concept_chunk)
        self.worker.metadata_chunk_ready.connect(self.show_metadata_chunk)
        self.worker.game_records_ready.connect(self.show_game_records)
        self.worker.icon_prompt_chunk_ready.connect(self.show_icon_prompt_chunk)
        self.worker.icon_ready.connect(self.show_icon)
        self.worker.error_occurred.connect(self.show_generation_error)
        self.worker.finished.connect(self.worker_complete)
        self.worker.start()

    @property
    def output_editors(self) -> list[QTextEdit]:
        return [
            self.concept_editor,
            self.metadata_editor,
            self.task_editor,
            self.article_editor,
            self.infoportions_editor,
            self.icon_prompt_editor,
        ]

    def set_generate_button_stop(self) -> None:
        self.generate_button.setText(text_config.stop_generate_text)
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.stop_generate)

    def stop_generate(self) -> None:
        logger.info("Generation canceled")
        self.worker.requestInterruption()
        self.set_generate_button_generate()

    def set_generate_button_generate(self) -> None:
        self.generate_button.setText(text_config.generate_text)
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.generate_quest_normal)

    @Slot(str)
    def show_concept_chunk(self, response: str) -> None:
        self.show_stream_response(self.concept_editor, response)

    @Slot(str)
    def show_metadata_chunk(self, response: str) -> None:
        self.show_stream_response(self.metadata_editor, response)

    @Slot(str)
    def show_icon_prompt_chunk(self, response: str) -> None:
        self.show_stream_response(self.icon_prompt_editor, response)

    def show_stream_response(self, editor: QTextEdit, response: str) -> None:
        user_cursor = editor.textCursor()
        vertical_scroll_pos = editor.verticalScrollBar().value()

        end_cursor = QTextCursor(editor.document())
        end_cursor.movePosition(QTextCursor.MoveOperation.End)
        end_cursor.insertText(response)

        editor.setTextCursor(user_cursor)
        editor.verticalScrollBar().setValue(vertical_scroll_pos)

    @Slot(GameRecords)
    def show_game_records(self, quest_records: GameRecords) -> None:
        editor_to_record = {
            self.task_editor: quest_records.task,
            self.article_editor: quest_records.article,
            self.infoportions_editor: quest_records.infoportions,
        }

        for editor, record in editor_to_record.items():
            editor.insertPlainText(record)
            editor.moveCursor(QTextCursor.MoveOperation.Start)

    @Slot(Image.Image)
    def show_icon(self, icon: Image.Image) -> None:
        self.icon_editor.setPixmap(get_pixmap(icon))

    @Slot(str)
    def show_generation_error(self, error: str) -> None:
        QMessageBox.warning(self, "Ошибка генерации", error)

    @Slot()
    def worker_complete(self) -> None:
        logger.info("Generation completed")
        self.set_generate_button_generate()
        self.worker.deleteLater()
        self.worker = None

    def add_output_editors(self) -> None:
        label = QLabel("Концепт")
        self.layout.addWidget(label)
        self.concept_editor = QTextEdit()
        self.concept_editor.setReadOnly(True)
        self.concept_editor.setMinimumHeight(constants_config.concept_height)
        self.layout.addWidget(self.concept_editor, constants_config.concept_stretch)

        label = QLabel("Метаданные")
        self.layout.addWidget(label)
        self.metadata_editor = QTextEdit()
        self.metadata_editor.setReadOnly(True)
        self.metadata_editor.setMinimumHeight(constants_config.metadata_height)
        self.layout.addWidget(self.metadata_editor, constants_config.metadata_stretch)

        label = QLabel("Задание")
        self.layout.addWidget(label)
        self.task_editor = QTextEdit()
        self.task_editor.setReadOnly(True)
        self.task_editor.setMinimumHeight(constants_config.editor_height)
        self.layout.addWidget(self.task_editor, constants_config.editor_stretch)

        label = QLabel("Описание")
        self.layout.addWidget(label)
        self.article_editor = QTextEdit()
        self.article_editor.setReadOnly(True)
        self.article_editor.setMinimumHeight(constants_config.editor_height)
        self.layout.addWidget(self.article_editor, constants_config.editor_stretch)

        label = QLabel("Инфопоршни")
        self.layout.addWidget(label)
        self.infoportions_editor = QTextEdit()
        self.infoportions_editor.setReadOnly(True)
        self.infoportions_editor.setMinimumHeight(constants_config.editor_height)
        self.layout.addWidget(self.infoportions_editor, constants_config.editor_stretch)

        label = QLabel("Промпт для генерации иконки")
        self.layout.addWidget(label)
        self.icon_prompt_editor = QTextEdit()
        self.icon_prompt_editor.setReadOnly(True)
        self.icon_prompt_editor.setMinimumHeight(constants_config.editor_height)
        self.layout.addWidget(self.icon_prompt_editor, constants_config.editor_stretch)

        label = QLabel("Иконка")
        self.layout.addWidget(label)
        self.icon_editor = QLabel()
        self.layout.addWidget(self.icon_editor)
