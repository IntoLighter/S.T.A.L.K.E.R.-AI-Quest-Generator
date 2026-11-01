from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from config.preferences.sections.types import ModelType
from generation.engines.text.factory import create_text_engine
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
)
from utils.translation import ui

from ui.utils.layout import get_layout_with_scroll
from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import Tab


class ModelTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.main_layout = get_layout_with_scroll(self)

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
        engine = create_text_engine(ModelType.Local, preferences_config)
        self.local_model_dropdown.addItems(engine.get_models())
        index = self.local_model_dropdown.findText(
            preferences_config.model.text_model_local
        )
        self.local_model_dropdown.setCurrentIndex(index)
        self.main_layout.addWidget(self.local_model_dropdown)

        self.remote_model_dropdown = QComboBox()
        engine = create_text_engine(ModelType.Remote, preferences_config)
        self.remote_model_dropdown.addItems(engine.get_models())
        index = self.remote_model_dropdown.findText(
            preferences_config.model.text_model_remote
        )
        self.remote_model_dropdown.setCurrentIndex(index)
        self.main_layout.addWidget(self.remote_model_dropdown)

        self.group.buttonToggled.connect(self.update_text_model_dropdown)
        self.update_text_model_dropdown()

        self.icon_workflow_editor = TextOptionEditor(
            label=ui("Icon workflow"),
            option=self.preferences_config.model.icon_workflow,
            size=constants_config.ui.icon_workflow_editor_size,
        )
        self.main_layout.addWidget(self.icon_workflow_editor)

    @Slot()
    def update_text_model_dropdown(self) -> None:
        is_local = self.local_model_button.isChecked()
        self.local_model_dropdown.setVisible(is_local)
        self.remote_model_dropdown.setVisible(not is_local)

    def save(self) -> None:
        self.preferences_config.model.text_model_type = (
            ModelType.Local if self.local_model_button.isChecked() else ModelType.Remote
        )

        self.preferences_config.model.text_model_local = (
            self.local_model_dropdown.currentText()
        )
        self.preferences_config.model.text_model_remote = (
            self.remote_model_dropdown.currentText()
        )
