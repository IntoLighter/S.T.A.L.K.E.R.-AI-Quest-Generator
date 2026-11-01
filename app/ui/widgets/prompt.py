from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from generation.parameters import parameters
from PySide6.QtCore import QEvent, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from utils.translation import ui


class PromptEditor(QWidget):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.add_parameters_editor()
        self.add_prompt_editor()
        self.retranslate_ui()

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self) -> None:
        self.add_parameter_button.setText(ui("Add"))
        self.prompt_label.setText(ui("Prompt"))

    def add_parameters_editor(self) -> None:
        row = QHBoxLayout()
        self.main_layout.addLayout(row)

        self.parameter_names_combo = QComboBox()
        self.parameter_names_combo.addItems(list(parameters))
        self.parameter_names_combo.currentTextChanged.connect(
            self.update_parameter_values_combo
        )
        row.addWidget(self.parameter_names_combo, stretch=1)

        self.parameter_values_combo = QComboBox()
        self.parameter_values_combo.addItems(
            parameters[self.parameter_names_combo.currentText()]
        )
        row.addWidget(self.parameter_values_combo, stretch=1)

        self.add_parameter_button = QPushButton()
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
        self.prompt_editor.appendPlainText(f"{name}: {value}")

    def add_prompt_editor(self) -> None:
        self.prompt_label = QLabel()
        self.main_layout.addWidget(self.prompt_label)
        self.prompt_editor = QPlainTextEdit()
        self.prompt_editor.setPlainText(self.preferences_config.general.prompt_message)
        self.prompt_editor.setMinimumHeight(constants_config.ui.editor_height)
        self.main_layout.addWidget(
            self.prompt_editor, constants_config.ui.editor_stretch
        )

    @property
    def prompt(self) -> str:
        return self.prompt_editor.toPlainText()

    @prompt.setter
    def prompt(self, value: str) -> None:
        self.prompt_editor.setPlainText(value)
