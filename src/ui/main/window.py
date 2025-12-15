from config.constants import constants_config
from config.preferences import PreferencesConfig
from config.text import text_config
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from ui.configurator import ConfiguratorDialog
from ui.main.widget import MainWidget
from ui.preferences.main import PreferencesDialog


class MainWindow(QMainWindow):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.resize(*constants_config.window_dims)  # noqa
        self.setWindowTitle(text_config.app_name)
        self.preferences_config = preferences_config

        self.main_widget = MainWidget(self.preferences_config, self.show_status)
        self.setCentralWidget(self.main_widget)

        self.status_label = QLabel()
        self.statusBar().addWidget(self.status_label)
        self.was_model_unspecified = False
        self.set_models_unspecified_restrictions()

        self.set_menubar()

    def set_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")
        file_menu.addAction(self.get_configurator())
        file_menu.addAction(self.get_settings())

        help_menu = menubar.addMenu("Помощь")
        help_menu.addAction(self.get_about())

    def get_configurator(self) -> QAction:
        action = QAction("Конфигуратор", self)
        action.setShortcuts((QKeySequence("Ctrl+S"), QKeySequence("Ctrl+Ы")))
        action.triggered.connect(self.show_configurator)
        return action

    @Slot()
    def show_configurator(self) -> None:
        if not self.preferences_config.current_model:
            QMessageBox.warning(self, "Ошибка настроек", "Невозможно запустить конфигуратор пока текстовая модель не задана.")
            return

        dialog = ConfiguratorDialog(self, self.preferences_config)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.main_widget.generate_quest_configurator(dialog.parameters)

    def get_settings(self) -> QAction:
        action = QAction("Настройки", self)
        action.setMenuRole(QAction.MenuRole.PreferencesRole)
        action.setShortcuts((QKeySequence("Ctrl+,"), QKeySequence("Ctrl+б")))
        action.triggered.connect(self.open_settings)
        return action

    @Slot()
    def open_settings(self) -> None:
        dialog = PreferencesDialog(self, self.preferences_config)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.set_models_unspecified_restrictions()

    def set_models_unspecified_restrictions(self) -> None:
        if not self.preferences_config.current_model:
            self.was_model_unspecified = True
            self.main_widget.generate_button.setEnabled(False)
            self.show_status("Текстовая модель не задана")
        elif self.was_model_unspecified:
            self.was_model_unspecified = False
            self.main_widget.generate_button.setEnabled(True)
            self.show_status("")

    @Slot(str)
    def show_status(self, status: str) -> None:
        self.status_label.setText(status)

    def get_about(self) -> QAction:
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        return about_action

    @Slot()
    def show_about(self) -> None:
        QMessageBox.about(
            self,
            "О программе",
            f"""
<h3>{text_config.app_name}</h3>
<p>Версия {constants_config.app_version}</p>
<p>Путь до конфигов {str(constants_config.config_path)}</p>
            """,
        )
