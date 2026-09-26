from config.preferences import PreferencesConfig
from loguru import logger
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.dialog import QWindowDialog
from ui.windows.preferences.tab.base import Tab
from ui.windows.preferences.tab.configurator import ConfiguratorTab
from ui.windows.preferences.tab.general import GeneralTab
from ui.windows.preferences.tab.model import ModelTab
from ui.windows.preferences.tab.prompt import PromptTab


class PreferencesDialog(QWindowDialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig) -> None:
        super().__init__(parent)
        self.setWindowTitle(self.tr("Настройки"))
        self.preferences_config = preferences_config
        logger.info("Window 'Settings' opened")

        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.general_tab = GeneralTab(self.preferences_config)
        self.tab_widget.addTab(self.general_tab, self.tr("Основные"))

        self.model_tab = ModelTab(self.preferences_config)
        self.tab_widget.addTab(self.model_tab, self.tr("Модели"))

        self.prompt_tab = PromptTab(self.preferences_config)
        self.tab_widget.addTab(self.prompt_tab, self.tr("Промпты"))

        self.configurator_tab = ConfiguratorTab(self.preferences_config)
        self.tab_widget.addTab(self.configurator_tab, self.tr("Конфигуратор"))

        self.add_close_buttons()

    def add_close_buttons(self) -> None:
        row = QHBoxLayout()
        self.layout.addLayout(row)

        ok_btn = QPushButton(self.tr("ОК"))
        ok_btn.clicked.connect(self.accept)
        row.addWidget(ok_btn, stretch=1)

        cancel_btn = QPushButton(self.tr("Отмена"))
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
        return [self.tab_widget.widget(i) for i in range(self.tab_widget.count())]

    def reject(self) -> None:
        logger.info("Window 'Settings' rejected")
        super().reject()
