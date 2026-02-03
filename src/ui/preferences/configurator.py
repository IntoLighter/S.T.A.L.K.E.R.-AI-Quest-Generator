from config.constants import constants_config
from config.preferences import PreferencesConfig
from misc import get_layout_with_scroll
from PySide6.QtWidgets import (
    QLabel,
    QTextEdit,
)

from ui.preferences.tab import Tab


class ConfiguratorTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        label = QLabel("Концепт")
        self.layout.addWidget(label)
        self.concept_editor = QTextEdit()
        self.concept_editor.setPlainText(self.preferences_config.configurator_concept)
        self.concept_editor.setMinimumHeight(constants_config.concept_height)
        self.layout.addWidget(self.concept_editor, constants_config.concept_stretch)

        label = QLabel("Метаданные")
        self.layout.addWidget(label)
        self.metadata_editor = QTextEdit()
        self.metadata_editor.setPlainText(self.preferences_config.configurator_metadata)
        self.metadata_editor.setMinimumHeight(constants_config.metadata_height)
        self.layout.addWidget(self.metadata_editor, constants_config.metadata_stretch)

        label = QLabel("Промпт иконки")
        self.layout.addWidget(label)
        self.icon_prompt_editor = QTextEdit()
        self.icon_prompt_editor.setPlainText(
            self.preferences_config.configurator_icon_prompt
        )
        self.icon_prompt_editor.setMinimumHeight(constants_config.editor_height)
        self.layout.addWidget(self.icon_prompt_editor, constants_config.editor_stretch)

    def save(self) -> None:
        self.preferences_config.configurator_concept = self.concept_editor.toPlainText()
        self.preferences_config.configurator_metadata = self.metadata_editor.toPlainText()
        self.preferences_config.configurator_icon_prompt = (
            self.icon_prompt_editor.toPlainText()
        )
