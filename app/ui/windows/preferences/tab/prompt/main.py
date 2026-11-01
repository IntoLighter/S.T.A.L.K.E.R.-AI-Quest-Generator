from config.preferences.main import PreferencesConfig
from PySide6.QtWidgets import QTabWidget
from utils.translation import ui

from ui.utils.layout import get_layout_with_scroll
from ui.windows.preferences.tab.base import PreferencesTab
from ui.windows.preferences.tab.prompt.tabs.concept import ConceptTab
from ui.windows.preferences.tab.prompt.tabs.icon import IconTab
from ui.windows.preferences.tab.prompt.tabs.metadata import MetadataTab


class PromptTab(PreferencesTab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.main_layout = get_layout_with_scroll(self)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.concept_tab = ConceptTab(preferences_config)
        self.tab_widget.addTab(self.concept_tab, ui("Concept"))

        self.metadata_tab = MetadataTab(preferences_config)
        self.tab_widget.addTab(self.metadata_tab, ui("Metadata"))

        self.icon_tab = IconTab(preferences_config)
        self.tab_widget.addTab(self.icon_tab, ui("Icon"))
