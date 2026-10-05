from config.constants.main import constants_config
from config.preferences.sections.types import TextOption, ValueSource
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


class TextOptionEditor(QWidget):
    def __init__(
        self,
        label: str,
        option: TextOption,
        height: int = constants_config.ui.editor_height,
        stretch: int = constants_config.ui.editor_stretch,
    ) -> None:
        super().__init__()
        self.option = option

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        label_widget = QLabel(label)
        self.layout.addWidget(label_widget)

        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.group = QButtonGroup(self)

        self.system_button = QRadioButton(self.tr("Системный"))
        self.group.addButton(self.system_button)
        row.addWidget(self.system_button)

        self.custom_button = QRadioButton(self.tr("Собственный"))
        self.group.addButton(self.custom_button)
        row.addWidget(self.custom_button)

        self.editor = QPlainTextEdit()
        mode_to_content = {
            ValueSource.SYSTEM: self.option.system,
            ValueSource.CUSTOM: self.option.custom,
        }
        self.editor.setPlainText(mode_to_content[self.option.source])
        self.editor.setMinimumHeight(height)
        self.editor.setReadOnly(self.option.source == ValueSource.SYSTEM)
        self.editor.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.editor, stretch)

        self.group.buttonToggled.connect(self.on_source_changed)
        source_to_button = {
            ValueSource.SYSTEM: self.system_button,
            ValueSource.CUSTOM: self.custom_button,
        }
        source_to_button[self.option.source].setChecked(True)

    @Slot()
    def on_text_changed(self) -> None:
        if self.option.source == ValueSource.CUSTOM:
            self.option.custom = self.editor.toPlainText()

    @Slot()
    def on_source_changed(self) -> None:
        if self.system_button.isChecked():
            self.option.source = ValueSource.SYSTEM
            self.editor.setPlainText(self.option.system)
            self.editor.setReadOnly(True)
        elif self.custom_button.isChecked():
            self.option.source = ValueSource.CUSTOM
            self.editor.setPlainText(self.option.custom)
            self.editor.setReadOnly(False)
