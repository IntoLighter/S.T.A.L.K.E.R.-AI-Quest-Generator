from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from config.preferences.sections.types import ModelType
from generation.engines.text.factory import create_text_engine
from PySide6.QtCore import QObject, Qt, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QRadioButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from utils.translation import ui

from ui.utils.layout import get_layout_with_scroll
from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import PreferencesTab


class ModelsLoader(QObject):
    loaded = Signal(list, list)

    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.local_engine = create_text_engine(ModelType.Local, preferences_config)
        self.remote_engine = create_text_engine(ModelType.Remote, preferences_config)

    def start(self) -> None:
        QThreadPool.globalInstance().start(self.run)

    def run(self) -> None:
        self.loaded.emit(
            self.local_engine.get_models(), self.remote_engine.get_models()
        )


class ModelTab(PreferencesTab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.is_models_loaded = False

        self.stack = QStackedWidget()
        QVBoxLayout(self).addWidget(self.stack)

        self.loader = self.create_loader()
        self.stack.addWidget(self.loader)

        self.content = QWidget()
        self.main_layout = get_layout_with_scroll(self.content)
        self.stack.addWidget(self.content)

        label = QLabel(ui("Text"))
        self.main_layout.addWidget(label)

        self.group = QButtonGroup(self)
        row = QHBoxLayout()
        self.main_layout.addLayout(row)
        self.local_model_button = QRadioButton(ui("Local"))
        self.remote_model_button = QRadioButton(ui("Remote"))
        self.group.addButton(self.local_model_button)
        self.group.addButton(self.remote_model_button)
        type_to_button = {
            ModelType.Local: self.local_model_button,
            ModelType.Remote: self.remote_model_button,
        }
        type_to_button[preferences_config.model.text_model_type].setChecked(True)
        row.addWidget(self.local_model_button)
        row.addWidget(self.remote_model_button)

        self.local_model_dropdown = QComboBox()
        self.main_layout.addWidget(self.local_model_dropdown)

        self.remote_model_dropdown = QComboBox()
        self.main_layout.addWidget(self.remote_model_dropdown)

        self.group.buttonToggled.connect(self.update_text_model_dropdown)
        self.update_text_model_dropdown()

        self.icon_workflow_editor = TextOptionEditor(
            label=ui("Icon workflow"),
            option=self.preferences_config.model.icon_workflow,
            size=constants_config.ui.icon_workflow_editor_size,
        )
        self.main_layout.addWidget(self.icon_workflow_editor)

        self.stack.setCurrentWidget(self.loader)
        self.models_loader = ModelsLoader(preferences_config)
        self.models_loader.loaded.connect(self.on_models_loaded)
        self.models_loader.start()

    @staticmethod
    def create_loader() -> QWidget:
        loader = QWidget()
        layout = QVBoxLayout(loader)
        layout.addStretch()

        label = QLabel(ui("Loading models..."))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(font.pointSize() * 2)
        label.setFont(font)
        layout.addWidget(label)

        progress = QProgressBar()
        progress.setRange(0, 0)
        progress.setTextVisible(False)
        progress.setFixedWidth(constants_config.ui.loader_width)
        layout.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        return loader

    @Slot(list, list)
    def on_models_loaded(
        self, local_models: list[str], remote_models: list[str]
    ) -> None:
        self.fill_dropdown(
            self.local_model_dropdown,
            local_models,
            self.preferences_config.model.text_model_local,
        )
        self.fill_dropdown(
            self.remote_model_dropdown,
            remote_models,
            self.preferences_config.model.text_model_remote,
        )
        self.is_models_loaded = True
        self.stack.setCurrentWidget(self.content)

    @staticmethod
    def fill_dropdown(dropdown: QComboBox, models: list[str], current: str) -> None:
        dropdown.addItems(models)
        dropdown.setCurrentIndex(dropdown.findText(current))

    @Slot()
    def update_text_model_dropdown(self) -> None:
        is_local = self.local_model_button.isChecked()
        self.local_model_dropdown.setVisible(is_local)
        self.remote_model_dropdown.setVisible(not is_local)

    def save(self) -> None:
        self.preferences_config.model.text_model_type = (
            ModelType.Local if self.local_model_button.isChecked() else ModelType.Remote
        )

        if not self.is_models_loaded:
            return

        self.preferences_config.model.text_model_local = (
            self.local_model_dropdown.currentText()
        )
        self.preferences_config.model.text_model_remote = (
            self.remote_model_dropdown.currentText()
        )
