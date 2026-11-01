from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QVBoxLayout
from utils.translation import ui

from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import Tab


class ConceptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.main_layout = QVBoxLayout(self)

        self.editor = TextOptionEditor(
            label=ui("Concept"),
            option=self.preferences_config.prompt.concept,
            size=constants_config.ui.concept_editor_size,
        )
        self.main_layout.addWidget(self.editor)
