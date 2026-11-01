from __future__ import annotations

from typing import TYPE_CHECKING

from config.preferences.sections.types import ModelType
from generation.models.text.local import LocalTextModel
from generation.models.text.remote import RemoteTextModel
from generation.workers.configurator import ConfiguratorWorker
from generation.workers.normal import NormalWorker
from loguru import logger
from PySide6.QtCore import QEvent, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QTabWidget,
    QWidget,
)
from utils.error import (
    ErrorInfo,
)
from utils.translation import err, ui

from ui.utils.layout import get_layout_with_scroll
from ui.utils.message import show_generation_start_error
from ui.widgets.prompt import PromptEditor
from ui.windows.exception.main import ExceptionDialog
from ui.windows.main.tab.base import Tab
from ui.windows.main.tab.concept import ConceptTab
from ui.windows.main.tab.icon import IconTab
from ui.windows.main.tab.metadata import MetadataTab

if TYPE_CHECKING:
    from config.preferences.main import PreferencesConfig
    from generation.entity import ConfiguratorParameters
    from generation.models.text.main import TextModel
    from generation.workers.base import BaseWorker


class MainWidget(QWidget):
    status_update_signal = Signal(str)
    generation_completed = Signal()

    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.is_generating = False

        self.main_layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor()
        self.main_layout.addWidget(self.prompt_editor)

        self.generate_button = QPushButton()
        self.generate_button.clicked.connect(self.generate_quest_normal)
        self.main_layout.addWidget(self.generate_button)

        self.add_tabs()
        self.retranslate_ui()

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self) -> None:
        self.update_generate_button_text()
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.concept_tab), ui("Concept")
        )
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.metadata_tab), ui("Metadata")
        )
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.icon_tab), ui("Icon"))

    def update_generate_button_text(self) -> None:
        if self.is_generating:
            self.generate_button.setText(ui("Stop quest generation"))
        else:
            self.generate_button.setText(ui("Generate quest"))

    @Slot()
    def generate_quest_normal(self) -> None:
        if not self.preferences_config.model.current_text_model:
            show_generation_start_error(
                self,
                err("generation_text_model_not_set"),
            )
            return

        if not self.preferences_config.general.should_generate_concept:
            show_generation_start_error(
                self,
                err("generation_concept_disabled"),
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
        self.is_generating = True
        self.update_generate_button_text()
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(lambda: self.stop_generate(worker))

    def stop_generate(self, worker: BaseWorker) -> None:
        worker.request_interruption()
        self.set_generate_button_generate()

    def set_generate_button_generate(self) -> None:
        self.is_generating = False
        self.update_generate_button_text()
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.generate_quest_normal)

    @Slot(ErrorInfo)
    def show_generation_error(self, error_result: ErrorInfo) -> None:
        dialog = QMessageBox(
            QMessageBox.Icon.Warning,
            ui("Error"),
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
        self.tab_widget.addTab(self.concept_tab, "")

        self.metadata_tab = MetadataTab()
        self.tab_widget.addTab(self.metadata_tab, "")

        self.icon_tab = IconTab()
        self.tab_widget.addTab(self.icon_tab, "")

    @property
    def tabs(self) -> list[Tab]:
        return [
            tab
            for i in range(self.tab_widget.count())
            if isinstance(tab := self.tab_widget.widget(i), Tab)
        ]
