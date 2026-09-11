from __future__ import annotations

from loguru import logger
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QWidget,
)

from config.constants import constants_config
from config.preferences import ModelType, PreferencesConfig
from config.text import text_config
from generation.entity import ConfiguratorParameters, GameRecords, IconRecords
from generation.model.local import LocalModel
from generation.model.main import Model
from generation.model.remote import RemoteModel
from generation.worker.configurator import ConfiguratorWorker
from generation.worker.normal import NormalWorker
from misc import (
    ErrorInfo,
    get_layout_with_scroll,
    get_pixmap,
    show_parameters_error,
    show_settings_error,
)
from ui.editor.prompt import PromptEditor
from ui.exception.main import ExceptionDialog


class MainWidget(QWidget):
    status_update_signal = Signal(str)
    generation_completed = Signal()

    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config

        self.layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor(preferences_config)
        self.layout.addWidget(self.prompt_editor)

        self.generate_button = QPushButton(text_config.generate_text)
        self.generate_button.clicked.connect(self.generate_quest_normal)
        self.layout.addWidget(self.generate_button)

        self.add_output_editors()

    @Slot()
    def generate_quest_normal(self) -> None:
        if not self.preferences_config.current_model:
            show_settings_error(
                self, "Невозможно запустить генерацию. Текстовая модель не задана."
            )
            return

        if not self.preferences_config.should_generate_concept:
            show_parameters_error(
                self,
                "Невозможно запустить генерацию. Отключенна генерация концепта.",
            )
            return

        logger.info("Normal generation started")

        self.worker = NormalWorker(
            preferences_config=self.preferences_config,
            text_model=self.model,
            prompt=self.prompt_editor.prompt,
        )
        self.generate_quest()

    def generate_quest_configurator(self, parameters: ConfiguratorParameters) -> None:
        logger.info("Configurator generation started")

        self.worker = ConfiguratorWorker(
            preferences_config=self.preferences_config,
            text_model=self.model,
            prompt=parameters.prompt,
            parameters=parameters,
        )
        self.generate_quest()

    @property
    def model(self) -> Model:
        type_to_value = {
            ModelType.Local: LocalModel(preferences_config=self.preferences_config),
            ModelType.Remote: RemoteModel(preferences_config=self.preferences_config),
        }

        return type_to_value[self.preferences_config.model_type]

    def generate_quest(self) -> None:
        self.set_generate_button_stop()
        for editor in self.output_editors:
            editor.clear()

        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker.status_update.connect(self.status_update_signal)
        self.worker.concept_chunk_ready.connect(self.show_concept_chunk)
        self.worker.metadata_chunk_ready.connect(self.show_metadata_chunk)
        self.worker.metadata_ready.connect(self.update_metadata)
        self.worker.game_records_ready.connect(self.show_game_records)
        self.worker.icon_prompt_chunk_ready.connect(self.show_icon_prompt_chunk)
        self.worker.icon_ready.connect(self.show_icon)
        self.worker.error_occurred.connect(self.show_generation_error)
        self.worker.unknown_error_occurred.connect(self.show_generation_unknown_error)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.thread_complete)

        self.worker_thread.start()

    @property
    def output_editors(self) -> list[QPlainTextEdit | QLabel]:
        return [
            self.concept_editor,
            self.metadata_editor,
            self.task_editor,
            self.article_editor,
            self.infoportions_editor,
            self.icon_prompt_editor,
            self.icon_soc_editor,
            self.icon_editor,
        ]

    def set_generate_button_stop(self) -> None:
        self.generate_button.setText(text_config.stop_generate_text)
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.stop_generate)

    def stop_generate(self) -> None:
        logger.info("Generation canceled")
        self.worker.is_interruption_requested = True
        self.set_generate_button_generate()

    def set_generate_button_generate(self) -> None:
        self.generate_button.setText(text_config.generate_text)
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.generate_quest_normal)

    @Slot(str)
    def show_concept_chunk(self, chunk: str) -> None:
        self.show_stream_chunk(self.concept_editor, chunk)

    @Slot(str)
    def show_metadata_chunk(self, chunk: str) -> None:
        self.show_stream_chunk(self.metadata_editor, chunk)

    @Slot(str)
    def update_metadata(self, metadata: str) -> None:
        self.metadata_editor.setPlainText(metadata)

    @Slot(str)
    def show_icon_prompt_chunk(self, chunk: str) -> None:
        self.show_stream_chunk(self.icon_prompt_editor, chunk)

    def show_stream_chunk(self, editor: QPlainTextEdit, chunk: str) -> None:
        user_cursor = editor.textCursor()
        vertical_scroll_pos = editor.verticalScrollBar().value()

        end_cursor = QTextCursor(editor.document())
        end_cursor.movePosition(QTextCursor.MoveOperation.End)
        end_cursor.insertText(chunk)

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
            editor.setPlainText(record)

    @Slot(IconRecords)
    def show_icon(self, icon_records: IconRecords) -> None:
        self.icon_editor.setPixmap(get_pixmap(icon_records.icon))
        self.icon_soc_editor.setPixmap(get_pixmap(icon_records.icon_soc))

    @Slot(ErrorInfo)
    def show_generation_error(self, error_result: ErrorInfo) -> None:
        dialog = QMessageBox(
            QMessageBox.Icon.Warning,
            "Ошибка",
            error_result.msg,
            parent=self,
            detailedText=error_result.details,
        )
        dialog.show()

    @Slot(str)
    def show_generation_unknown_error(self, stacktrace: str) -> None:
        dialog = ExceptionDialog(stacktrace=stacktrace, parent=self)
        dialog.show()

    @Slot()
    def thread_complete(self) -> None:
        logger.info("Generation completed")
        self.set_generate_button_generate()
        self.generation_completed.emit()

        self.worker = None
        self.worker_thread = None

    def add_output_editors(self) -> None:
        self.concept_editor = self.create_plain_text_editor(
            "Концепт",
            constants_config.concept_height,
            constants_config.concept_stretch,
        )

        self.metadata_editor = self.create_plain_text_editor(
            "Метаданные",
            constants_config.metadata_height,
            constants_config.metadata_stretch,
        )
        self.task_editor = self.create_plain_text_editor(
            "Задание",
            constants_config.editor_height,
            constants_config.editor_stretch,
        )
        self.article_editor = self.create_plain_text_editor(
            "Описание",
            constants_config.editor_height,
            constants_config.editor_stretch,
        )
        self.infoportions_editor = self.create_plain_text_editor(
            "Инфопоршни",
            constants_config.editor_height,
            constants_config.editor_stretch,
        )

        self.icon_prompt_editor = self.create_plain_text_editor(
            "Промпт иконки",
            constants_config.icon_prompt_height,
            constants_config.icon_prompt_stretch,
        )
        self.icon_soc_editor = self.create_label_editor("Иконка (SoC)")
        self.icon_editor = self.create_label_editor("Иконка (оригинал)")

    def create_plain_text_editor(
        self, title: str, height: int, stretch: int
    ) -> QPlainTextEdit:
        label = QLabel(title)
        self.layout.addWidget(label)

        editor = QPlainTextEdit()
        editor.setReadOnly(True)
        editor.setMinimumHeight(height)
        self.layout.addWidget(editor, stretch)

        return editor

    def create_label_editor(self, title: str) -> QLabel:
        label = QLabel(title)
        self.layout.addWidget(label)

        editor = QLabel()
        self.layout.addWidget(editor)

        return editor
