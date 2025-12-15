from PySide6.QtCore import Slot

from config.preferences import PreferencesConfig, ModelType
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QLabel,
)

from config.text import text_config
from ui.preferences.tab import Tab


class ModelTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config

        self.layout = QVBoxLayout(self)

        self.text_model_label = QLabel("Модель текста")
        self.layout.addWidget(self.text_model_label)

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

        self.local_model_parameters = QWidget()
        self.layout.addWidget(self.local_model_parameters)
        column = QVBoxLayout(self.local_model_parameters)
        row = QHBoxLayout()
        column.addLayout(row)
        self.local_model_editor = QLineEdit(self.preferences_config.local_model)
        row.addWidget(self.local_model_editor)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_local_model)
        row.addWidget(reset_button)

        self.remote_model_parameters = QWidget()
        self.layout.addWidget(self.remote_model_parameters)
        column = QVBoxLayout(self.remote_model_parameters)
        row = QHBoxLayout()
        column.addLayout(row)
        self.remote_model_editor = QLineEdit(self.preferences_config.remote_model)
        row.addWidget(self.remote_model_editor)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_remote_model)
        row.addWidget(reset_button)

        self.group.buttonToggled.connect(self.update_parameters)
        self.update_parameters()

        self.layout.addStretch()

    @Slot()
    def reset_local_model(self):
        self.local_model_editor.setText(text_config.default_local_model)

    @Slot()
    def reset_remote_model(self):
        self.remote_model_editor.setText(text_config.default_remote_model)

    @Slot()
    def update_parameters(self):
        button_to_parameters = {
            self.local_model_button: self.local_model_parameters,
            self.remote_model_button: self.remote_model_parameters,
        }

        current_parameters = button_to_parameters[self.group.checkedButton()]
        other_parameters = next(v for v in button_to_parameters.values() if v != current_parameters)
        current_parameters.show()
        other_parameters.hide()

    def save(self) -> None:
        button_to_type = {
            self.local_model_button: ModelType.Local,
            self.remote_model_button: ModelType.Remote
        }
        self.preferences_config.model_type = button_to_type[self.group.checkedButton()]

        self.preferences_config.local_model = self.local_model_editor.text()
        self.preferences_config.remote_model = self.remote_model_editor.text()

