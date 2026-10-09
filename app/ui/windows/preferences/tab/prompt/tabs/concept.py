from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QVBoxLayout

from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import Tab


class ConceptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = QVBoxLayout(self)

        self.editor = TextOptionEditor(
            label=self.tr("Концепт"),
            option=self.preferences_config.prompt.concept,
            height=constants_config.ui.concept_height,
            stretch=constants_config.ui.concept_stretch,
        )
        self.layout.addWidget(self.editor)
