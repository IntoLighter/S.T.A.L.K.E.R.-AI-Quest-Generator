from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
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

        self.add_prompt_editor()
        self.retranslate_ui()

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self) -> None:
        self.prompt_label.setText(ui("Prompt"))

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
