from loguru import logger

from config.constants import constants_config
from config.preferences import PreferencesConfig
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.dialog import Dialog
from ui.preferences.configurator import ConfiguratorTab
from ui.preferences.general import GeneralTab
from ui.preferences.model import ModelTab
from ui.preferences.prompt import PromptTab
from ui.preferences.tab import Tab


class PreferencesDialog(Dialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig) -> None:
        super().__init__(parent)
        self.resize(*constants_config.window_dims)  # noqa
        self.setWindowTitle("Настройки")
        self.preferences_config = preferences_config
        logger.info("Window 'Settings' opened")

        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.general_tab = GeneralTab(self.preferences_config)
        self.tab_widget.addTab(self.general_tab, "Основные")

        self.model_tab = ModelTab(self.preferences_config)
        self.tab_widget.addTab(self.model_tab, "Модели")

        self.prompt_tab = PromptTab(self.preferences_config)
        self.tab_widget.addTab(self.prompt_tab, "Промпты")

        self.configurator_tab = ConfiguratorTab(self.preferences_config)
        self.tab_widget.addTab(self.configurator_tab, "Конфигуратор")

        self.add_close_buttons()

    def add_close_buttons(self) -> None:
        row = QHBoxLayout()
        self.layout.addLayout(row)

        ok_btn = QPushButton("ОК")
        ok_btn.clicked.connect(self.accept)
        row.addWidget(ok_btn, stretch=1)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(cancel_btn, stretch=1)

    def accept(self) -> None:
        for tab in self.tabs:
            tab.save()

        self.preferences_config.save()
        logger.info("Window 'Settings' accepted")
        super().accept()

    @property
    def tabs(self) -> list[Tab]:
        return [self.general_tab, self.model_tab, self.configurator_tab, self.prompt_tab]

    def reject(self) -> None:
        logger.info("Window 'Settings' rejected")
        super().reject()
