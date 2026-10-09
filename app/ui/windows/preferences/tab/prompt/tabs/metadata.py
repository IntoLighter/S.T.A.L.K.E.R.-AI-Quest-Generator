from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QVBoxLayout

from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import Tab


class MetadataTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = QVBoxLayout(self)

        self.metadata_editor = TextOptionEditor(
            label=self.tr("Метаданные"),
            option=self.preferences_config.prompt.metadata,
            height=constants_config.ui.metadata_height,
            stretch=constants_config.ui.metadata_stretch,
        )
        self.layout.addWidget(self.metadata_editor)

        self.id_editor = TextOptionEditor(
            label=self.tr("ID"),
            option=self.preferences_config.prompt.id,
            height=constants_config.ui.id_height,
            stretch=constants_config.ui.id_stretch,
        )
        self.layout.addWidget(self.id_editor)
