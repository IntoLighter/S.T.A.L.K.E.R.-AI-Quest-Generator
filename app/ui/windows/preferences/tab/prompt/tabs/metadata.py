from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QVBoxLayout
from utils.translation import ui

from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import PreferencesTab


class MetadataTab(PreferencesTab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.main_layout = QVBoxLayout(self)

        self.metadata_editor = TextOptionEditor(
            label=ui("Metadata"),
            option=self.preferences_config.prompt.metadata,
            size=constants_config.ui.metadata_editor_size,
        )
        self.main_layout.addWidget(self.metadata_editor)

        self.id_editor = TextOptionEditor(
            label="ID",
            option=self.preferences_config.prompt.id,
            size=constants_config.ui.id_editor_size,
        )
        self.main_layout.addWidget(self.id_editor)
