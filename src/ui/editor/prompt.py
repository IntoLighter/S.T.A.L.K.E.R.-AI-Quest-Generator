
from config.constants import constants_config
from config.parameters import parameters
from config.preferences import PreferencesConfig
from config.text import text_config
from PySide6.QtCore import Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class PromptEditor(QWidget):
    def __init__(self, preferences_config: PreferencesConfig):
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = QVBoxLayout(self)

        self.add_parameters_editor()
        self.add_prompt_editor()

    def add_parameters_editor(self) -> None:
        row = QHBoxLayout()
        self.layout.addLayout(row)

        self.parameter_names_combo = QComboBox()
        self.parameter_names_combo.addItems([name for name in parameters.keys()])
        self.parameter_names_combo.currentTextChanged.connect(
            self.update_parameter_values_combo
        )
        row.addWidget(self.parameter_names_combo, stretch=1)

        self.parameter_values_combo = QComboBox()
        self.parameter_values_combo.addItems(
            parameters[self.parameter_names_combo.currentText()]
        )
        row.addWidget(self.parameter_values_combo, stretch=1)

        self.add_parameter_button = QPushButton(text_config.add_parameter_text)
        self.add_parameter_button.clicked.connect(self.add_parameter)
        row.addWidget(self.add_parameter_button)

    @Slot()
    def update_parameter_values_combo(self) -> None:
        self.parameter_values_combo.clear()
        self.parameter_values_combo.addItems(
            parameters[self.parameter_names_combo.currentText()]
        )

    @Slot()
    def add_parameter(self) -> None:
        name = self.parameter_names_combo.currentText()
        value = self.parameter_values_combo.currentText()
        self.prompt_editor.append(f"{name}: {value}")

    def add_prompt_editor(self) -> None:
        label = QLabel("Промпт")
        self.layout.addWidget(label)
        self.prompt_editor = QTextEdit()
        self.prompt_editor.setMinimumHeight(constants_config.editor_height)
        self.prompt_editor.insertPlainText(self.preferences_config.prompt_message)
        self.prompt_editor.moveCursor(QTextCursor.MoveOperation.Start)
        self.layout.addWidget(self.prompt_editor, constants_config.editor_stretch)

    @property
    def prompt(self) -> str:
        return self.prompt_editor.toPlainText()
