from config.constants import constants_config
from config.preferences import PreferencesConfig
from misc import get_layout_with_scroll, get_prompt_from_file
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
)

from ui.preferences.tab import Tab


class PromptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig):
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        label = QLabel("Концепт")
        self.layout.addWidget(label)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.concept_editor = QTextEdit()
        self.concept_editor.setPlainText(self.preferences_config.concept_prompt)
        self.concept_editor.setMinimumHeight(constants_config.concept_height)
        row.addWidget(self.concept_editor, constants_config.concept_stretch)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_concept)
        row.addWidget(reset_button)

        label = QLabel("Метаданные")
        self.layout.addWidget(label)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.metadata_editor = QTextEdit()
        self.metadata_editor.setPlainText(self.preferences_config.metadata_prompt)
        self.metadata_editor.setMinimumHeight(constants_config.metadata_height)
        row.addWidget(self.metadata_editor, constants_config.metadata_stretch)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_metadata)
        row.addWidget(reset_button)

        label = QLabel("Иконка")
        self.layout.addWidget(label)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.icon_editor = QTextEdit()
        self.icon_editor.setPlainText(self.preferences_config.icon_prompt)
        self.icon_editor.setMinimumHeight(constants_config.editor_height)
        row.addWidget(self.icon_editor, constants_config.editor_stretch)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_icon)
        row.addWidget(reset_button)

    @Slot()
    def reset_concept(self) -> None:
        self.concept_editor.setPlainText(get_prompt_from_file("concept.txt"))

    @Slot()
    def reset_metadata(self) -> None:
        self.metadata_editor.setPlainText(get_prompt_from_file("metadata.txt"))

    @Slot()
    def reset_icon(self) -> None:
        self.icon_editor.setPlainText(get_prompt_from_file("icon.txt"))

    def save(self) -> None:
        self.preferences_config.concept_prompt = self.concept_editor.toPlainText()
        self.preferences_config.metadata_prompt = self.metadata_editor.toPlainText()
        self.preferences_config.icon_prompt = self.icon_editor.toPlainText()
