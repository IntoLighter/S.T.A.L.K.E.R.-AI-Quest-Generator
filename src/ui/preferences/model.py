from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
)

from config.constants import constants_config
from config.preferences import ModelType, PreferencesConfig
from generation.model.local import LocalModel
from generation.model.remote import RemoteModel
from misc import get_layout_with_scroll
from ui.editor.system_custom_text_editor import SystemCustomTextEditor
from ui.preferences.tab import Tab


class ModelTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        label = QLabel("Текст")
        self.layout.addWidget(label)

        self.group = QButtonGroup(self)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.local_model_button = QRadioButton("Локальная")
        self.remote_model_button = QRadioButton("Удаленная")
        self.group.addButton(self.local_model_button)
        self.group.addButton(self.remote_model_button)
        type_to_button = {
            ModelType.Local: self.local_model_button,
            ModelType.Remote: self.remote_model_button,
        }
        type_to_button[preferences_config.model_type].setChecked(True)
        row.addWidget(self.local_model_button)
        row.addWidget(self.remote_model_button)

        self.local_model_dropdown = QComboBox()
        model = LocalModel(preferences_config)
        self.local_model_dropdown.addItems(model.get_models())
        index = self.local_model_dropdown.findText(preferences_config.local_model)
        self.local_model_dropdown.setCurrentIndex(index)
        self.layout.addWidget(self.local_model_dropdown)

        self.remote_model_dropdown = QComboBox()
        model = RemoteModel(preferences_config)
        self.remote_model_dropdown.addItems(model.get_models())
        index = self.remote_model_dropdown.findText(preferences_config.remote_model)
        self.remote_model_dropdown.setCurrentIndex(index)
        self.layout.addWidget(self.remote_model_dropdown)

        self.group.buttonToggled.connect(self.update_text_model_dropdown)
        self.update_text_model_dropdown()

        self.icon_workflow_editor = SystemCustomTextEditor(
            label="Workflow иконки",
            source=self.preferences_config.icon_workflow_source,
            system_content=constants_config.default_icon_workflow,
            custom_content=self.preferences_config.custom_icon_workflow,
            height=constants_config.icon_workflow_height,
            stretch=constants_config.icon_workflow_stretch,
        )
        self.layout.addWidget(self.icon_workflow_editor)

    @Slot()
    def update_text_model_dropdown(self) -> None:
        button_to_dropdown = {
            self.local_model_button: self.local_model_dropdown,
            self.remote_model_button: self.remote_model_dropdown,
        }

        current_dropdown = button_to_dropdown[self.group.checkedButton()]
        other_dropdown = next(
            v for v in button_to_dropdown.values() if v != current_dropdown
        )
        current_dropdown.show()
        other_dropdown.hide()

    def save(self) -> None:
        button_to_type = {
            self.local_model_button: ModelType.Local,
            self.remote_model_button: ModelType.Remote,
        }
        self.preferences_config.model_type = button_to_type[self.group.checkedButton()]

        self.preferences_config.local_model = self.local_model_dropdown.currentText()
        self.preferences_config.remote_model = self.remote_model_dropdown.currentText()

        self.preferences_config.icon_workflow_source = self.icon_workflow_editor.source
        self.preferences_config.custom_icon_workflow = (
            self.icon_workflow_editor.custom_content
        )
