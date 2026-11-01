from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QLabel
from utils.translation import ui

from ui.utils.layout import add_text_editor, get_layout_with_scroll
from ui.windows.preferences.tab.base import Tab


class ConfiguratorTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.main_layout = get_layout_with_scroll(self)

        configurator = self.preferences_config.configurator

        self.main_layout.addWidget(QLabel(ui("Concept")))
        self.concept_editor = add_text_editor(
            self.main_layout,
            configurator.concept,
            constants_config.ui.concept_editor_size,
        )

        self.main_layout.addWidget(QLabel(ui("Metadata")))
        self.metadata_editor = add_text_editor(
            self.main_layout,
            configurator.metadata,
            constants_config.ui.metadata_editor_size,
        )

        self.main_layout.addWidget(QLabel(ui("Icon prompt")))
        self.icon_prompt_editor = add_text_editor(
            self.main_layout,
            configurator.icon_prompt,
            constants_config.ui.icon_prompt_editor_size,
        )

    def save(self) -> None:
        self.preferences_config.configurator.concept = self.concept_editor.toPlainText()
        self.preferences_config.configurator.metadata = (
            self.metadata_editor.toPlainText()
        )
        self.preferences_config.configurator.icon_prompt = (
            self.icon_prompt_editor.toPlainText()
        )
