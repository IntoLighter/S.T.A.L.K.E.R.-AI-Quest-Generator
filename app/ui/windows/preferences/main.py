from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from config.preferences.repository import PreferencesRepository
from loguru import logger
from PySide6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from utils.translation import set_language, ui

from ui.dialog import BaseDialog
from ui.utils.tabs import get_tabs
from ui.windows.preferences.tab.base import PreferencesTab
from ui.windows.preferences.tab.configurator import ConfiguratorTab
from ui.windows.preferences.tab.general import GeneralTab
from ui.windows.preferences.tab.model import ModelTab
from ui.windows.preferences.tab.prompt.main import PromptTab


class PreferencesDialog(BaseDialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig) -> None:
        super().__init__(parent)
        self.setWindowTitle(ui("Settings"))
        self.preferences_config = preferences_config
        logger.info("Window 'Settings' opened")

        self.main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.general_tab = GeneralTab(self.preferences_config)
        self.tab_widget.addTab(self.general_tab, ui("General"))

        self.model_tab = ModelTab(self.preferences_config)
        self.tab_widget.addTab(self.model_tab, ui("Models"))

        self.prompt_tab = PromptTab(self.preferences_config)
        self.tab_widget.addTab(self.prompt_tab, ui("Prompts"))

        self.configurator_tab = ConfiguratorTab(self.preferences_config)
        self.tab_widget.addTab(self.configurator_tab, ui("Configurator"))

        self.add_close_buttons(self.main_layout, ui("OK"))

    def accept(self) -> None:
        previous_interface_language = self.preferences_config.general.interface_language
        for tab in get_tabs(self.tab_widget, PreferencesTab):
            tab.save()

        repository = PreferencesRepository(constants_config.paths.preferences_path)
        repository.save(self.preferences_config)
        logger.info("Window 'Settings' accepted")
        super().accept()

        if (
            self.preferences_config.general.interface_language
            != previous_interface_language
        ):
            set_language(self.preferences_config.general.interface_language)

    def reject(self) -> None:
        logger.info("Window 'Settings' rejected")
        super().reject()
