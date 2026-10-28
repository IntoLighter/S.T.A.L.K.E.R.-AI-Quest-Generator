from __future__ import annotations

from config.preferences.main import PreferencesConfig
from config.preferences.sections.types import ModelType
from generation.entity import ConfiguratorParameters
from generation.models.text.local import LocalTextModel
from generation.models.text.main import TextModel
from generation.models.text.remote import RemoteTextModel
from generation.workers.base import BaseWorker
from generation.workers.configurator import ConfiguratorWorker
from generation.workers.normal import NormalWorker
from loguru import logger
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QTabWidget,
    QWidget,
)
from utils.error import (
    ErrorInfo,
)

from ui.utils.layout import get_layout_with_scroll
from ui.utils.message import show_generation_start_error
from ui.widgets.prompt import PromptEditor
from ui.windows.exception.main import ExceptionDialog
from ui.windows.main.tab.base import Tab
from ui.windows.main.tab.concept import ConceptTab
from ui.windows.main.tab.icon import IconTab
from ui.windows.main.tab.metadata import MetadataTab


class MainWidget(QWidget):
    status_update_signal = Signal(str)
    generation_completed = Signal()

    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config

        self.main_layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor(preferences_config)
        self.main_layout.addWidget(self.prompt_editor)

        self.generate_button = QPushButton(self.tr("Сгенерировать квест"))
        self.generate_button.clicked.connect(self.generate_quest_normal)
        self.main_layout.addWidget(self.generate_button)

        self.add_tabs()

    @Slot()
    def generate_quest_normal(self) -> None:
        if not self.preferences_config.model.current_text_model:
            show_generation_start_error(
                self,
                self.tr("Невозможно запустить генерацию. Текстовая модель не задана."),
            )
            return

        if not self.preferences_config.general.should_generate_concept:
            show_generation_start_error(
                self,
                self.tr(
                    "Невозможно запустить генерацию. Отключенна генерация концепта."
                ),
            )
            return

        logger.info("Normal generation started")

        worker = NormalWorker(
            preferences_config=self.preferences_config,
            text_model=self.model,
            prompt=self.prompt_editor.prompt,
        )
        self.generate_quest(worker)

    def generate_quest_configurator(self, parameters: ConfiguratorParameters) -> None:
        logger.info("Configurator generation started")

        worker = ConfiguratorWorker(
            preferences_config=self.preferences_config,
            text_model=self.model,
            prompt=parameters.prompt,
            parameters=parameters,
        )
        self.generate_quest(worker)

    @property
    def model(self) -> TextModel:
        type_to_value = {
            ModelType.Local: LocalTextModel(preferences_config=self.preferences_config),
            ModelType.Remote: RemoteTextModel(
                preferences_config=self.preferences_config
            ),
        }

        return type_to_value[self.preferences_config.model.text_model_type]

    def generate_quest(self, worker: BaseWorker) -> None:
        self.set_generate_button_stop(worker)
        for tab in self.tabs:
            tab.clear()

        worker_thread = QThread(self)
        worker.moveToThread(worker_thread)

        for tab in self.tabs:
            tab.bind_worker(worker)
        worker.status_update.connect(self.status_update_signal)
        worker.error_occurred.connect(self.show_generation_error)
        worker.unknown_error_occurred.connect(self.show_generation_unknown_error)

        worker_thread.started.connect(worker.run)
        worker.finished.connect(worker_thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker_thread.finished.connect(worker_thread.deleteLater)
        worker_thread.finished.connect(self.thread_complete)

        worker_thread.start()

    def set_generate_button_stop(self, worker: BaseWorker) -> None:
        self.generate_button.setText(self.tr("Остановить генерацию квеста"))
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(lambda: self.stop_generate(worker))

    def stop_generate(self, worker: BaseWorker) -> None:
        worker.request_interruption()
        self.set_generate_button_generate()

    def set_generate_button_generate(self) -> None:
        self.generate_button.setText(self.tr("Сгенерировать квест"))
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.generate_quest_normal)

    @Slot(ErrorInfo)
    def show_generation_error(self, error_result: ErrorInfo) -> None:
        dialog = QMessageBox(
            QMessageBox.Icon.Warning,
            self.tr("Ошибка"),
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

    def add_tabs(self) -> None:
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.concept_tab = ConceptTab()
        self.tab_widget.addTab(self.concept_tab, self.tr("Концепт"))

        self.metadata_tab = MetadataTab()
        self.tab_widget.addTab(self.metadata_tab, self.tr("Метаданные"))

        self.icon_tab = IconTab()
        self.tab_widget.addTab(self.icon_tab, self.tr("Иконка"))

    @property
    def tabs(self) -> list[Tab]:
        return [
            tab
            for i in range(self.tab_widget.count())
            if isinstance(tab := self.tab_widget.widget(i), Tab)
        ]
