from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QTabWidget

from ui.utils.layout import get_layout_with_scroll
from ui.windows.preferences.tab.base import Tab
from ui.windows.preferences.tab.prompt.tabs.concept import ConceptTab
from ui.windows.preferences.tab.prompt.tabs.icon import IconTab
from ui.windows.preferences.tab.prompt.tabs.metadata import MetadataTab


class PromptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.concept_tab = ConceptTab(preferences_config)
        self.tab_widget.addTab(self.concept_tab, self.tr("Концепт"))

        self.metadata_tab = MetadataTab(preferences_config)
        self.tab_widget.addTab(self.metadata_tab, self.tr("Метаданные"))

        self.icon_tab = IconTab(preferences_config)
        self.tab_widget.addTab(self.icon_tab, self.tr("Иконка"))
