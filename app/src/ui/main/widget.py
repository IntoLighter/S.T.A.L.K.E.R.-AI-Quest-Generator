from __future__ import annotations

from config.preferences import ModelType, PreferencesConfig
from generation.entity import ConfiguratorParameters
from generation.model.local import LocalModel
from generation.model.main import Model
from generation.model.remote import RemoteModel
from generation.worker.configurator import ConfiguratorWorker
from generation.worker.normal import NormalWorker
from loguru import logger
from util.misc import (
    ErrorInfo,
    get_layout_with_scroll,
    show_parameters_error,
    show_settings_error,
)
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QTabWidget,
    QWidget,
)

from ui.editor.prompt import PromptEditor
from ui.exception.main import ExceptionDialog
from ui.main.tab.base import Tab
from ui.main.tab.concept import ConceptTab
from ui.main.tab.icon import IconTab
from ui.main.tab.metadata import MetadataTab


class MainWidget(QWidget):
    status_update_signal = Signal(str)
    generation_completed = Signal()

    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config

        self.layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor(preferences_config)
        self.layout.addWidget(self.prompt_editor)

        self.generate_button = QPushButton(self.tr("Сгенерировать квест"))
        self.generate_button.clicked.connect(self.generate_quest_normal)
        self.layout.addWidget(self.generate_button)

        self.add_tabs()

    @Slot()
    def generate_quest_normal(self) -> None:
        if not self.preferences_config.current_model:
            show_settings_error(
                self,
                self.tr(
                    "Невозможно запустить генерацию. Текстовая модель не задана."
                ),
            )
            return

        if not self.preferences_config.should_generate_concept:
            show_parameters_error(
                self,
                self.tr(
                    "Невозможно запустить генерацию. Отключенна генерация концепта."
                ),
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
        for tab in self.tabs:
            tab.clear()

        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        for tab in self.tabs:
            tab.bind_worker(self.worker)
        self.worker.status_update.connect(self.status_update_signal)
        self.worker.error_occurred.connect(self.show_generation_error)
        self.worker.unknown_error_occurred.connect(self.show_generation_unknown_error)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.thread_complete)

        self.worker_thread.start()

    def set_generate_button_stop(self) -> None:
        self.generate_button.setText(self.tr("Остановить генерацию квеста"))
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.stop_generate)

    def stop_generate(self) -> None:
        logger.info("Generation canceled")
        self.worker.is_interruption_requested = True
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

        self.worker = None
        self.worker_thread = None

    def add_tabs(self) -> None:
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.concept_tab = ConceptTab()
        self.tab_widget.addTab(self.concept_tab, self.tr("Концепт"))

        self.metadata_tab = MetadataTab()
        self.tab_widget.addTab(self.metadata_tab, self.tr("Метаданные"))

        self.icon_tab = IconTab()
        self.tab_widget.addTab(self.icon_tab, self.tr("Иконка"))

    @property
    def tabs(self) -> list[Tab]:
        return [self.tab_widget.widget(i) for i in range(self.tab_widget.count())]
