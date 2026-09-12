from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from config.constants import constants_config
from config.preferences import ValueSource


class SystemCustomTextEditor(QWidget):
    def __init__(
        self,
        label: str,
        source: ValueSource,
        system_content: str,
        custom_content: str,
        height: int = constants_config.editor_height,
        stretch: int = constants_config.editor_stretch,
    ) -> None:
        super().__init__()
        self.source = source
        self.system_content = system_content
        self.custom_content = custom_content

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        label_widget = QLabel(label)
        self.layout.addWidget(label_widget)

        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.group = QButtonGroup(self)

        self.system_button = QRadioButton("Системный")
        self.group.addButton(self.system_button)
        row.addWidget(self.system_button)

        self.custom_button = QRadioButton("Собственный")
        self.group.addButton(self.custom_button)
        row.addWidget(self.custom_button)

        self.editor = QPlainTextEdit()
        mode_to_content = {
            ValueSource.SYSTEM: self.system_content,
            ValueSource.CUSTOM: self.custom_content,
        }
        self.editor.setPlainText(mode_to_content[self.source])
        self.editor.setMinimumHeight(height)
        self.editor.setReadOnly(self.source == ValueSource.SYSTEM)
        self.editor.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.editor, stretch)

        self.group.buttonToggled.connect(self.on_source_changed)
        source_to_button = {
            ValueSource.SYSTEM: self.system_button,
            ValueSource.CUSTOM: self.custom_button,
        }
        source_to_button[self.source].setChecked(True)

    @Slot()
    def on_text_changed(self) -> None:
        if self.source == ValueSource.CUSTOM:
            self.custom_content = self.editor.toPlainText()

    @Slot()
    def on_source_changed(self) -> None:
        if self.system_button.isChecked():
            self.source = ValueSource.SYSTEM
            self.editor.setPlainText(self.system_content)
            self.editor.setReadOnly(True)
        elif self.custom_button.isChecked():
            self.source = ValueSource.CUSTOM
            self.editor.setPlainText(self.custom_content)
            self.editor.setReadOnly(False)
