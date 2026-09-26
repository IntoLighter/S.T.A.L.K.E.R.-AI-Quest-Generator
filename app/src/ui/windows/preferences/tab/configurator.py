from config.constants import constants_config
from config.preferences import PreferencesConfig
from ui.utils.layout import get_layout_with_scroll
from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
)

from ui.windows.preferences.tab.base import Tab


class ConfiguratorTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        label = QLabel(self.tr("Концепт"))
        self.layout.addWidget(label)
        self.concept_editor = QPlainTextEdit()
        self.concept_editor.setPlainText(self.preferences_config.configurator_concept)
        self.concept_editor.setMinimumHeight(constants_config.concept_height)
        self.layout.addWidget(self.concept_editor, constants_config.concept_stretch)

        label = QLabel(self.tr("Метаданные"))
        self.layout.addWidget(label)
        self.metadata_editor = QPlainTextEdit()
        self.metadata_editor.setPlainText(self.preferences_config.configurator_metadata)
        self.metadata_editor.setMinimumHeight(constants_config.metadata_height)
        self.layout.addWidget(self.metadata_editor, constants_config.metadata_stretch)

        label = QLabel(self.tr("Промпт иконки"))
        self.layout.addWidget(label)
        self.icon_prompt_editor = QPlainTextEdit()
        self.icon_prompt_editor.setPlainText(
            self.preferences_config.configurator_icon_prompt
        )
        self.icon_prompt_editor.setMinimumHeight(constants_config.icon_prompt_height)
        self.layout.addWidget(
            self.icon_prompt_editor, constants_config.icon_prompt_stretch
        )

    def save(self) -> None:
        self.preferences_config.configurator_concept = self.concept_editor.toPlainText()
        self.preferences_config.configurator_metadata = (
            self.metadata_editor.toPlainText()
        )
        self.preferences_config.configurator_icon_prompt = (
            self.icon_prompt_editor.toPlainText()
        )
