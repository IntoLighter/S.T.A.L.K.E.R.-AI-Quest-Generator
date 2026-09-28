from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtCore import Qt, Slot, qtTrId
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSystemTrayIcon,
)

from ui.tray import Tray
from ui.windows.configurator.main import ConfiguratorDialog
from ui.windows.main.widget import MainWidget
from ui.windows.preferences.main import PreferencesDialog


class MainWindow(QMainWindow):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.resize(*constants_config.ui.window_size)  # noqa
        self.setWindowTitle(constants_config.app.name)
        self.preferences_config = preferences_config
        self.close_requested = False

        self.tray = Tray()
        self.tray.openRequested.connect(self.open)
        self.tray.quitRequested.connect(self.quit)

        self.main_widget = MainWidget(preferences_config=self.preferences_config)
        self.main_widget.status_update_signal.connect(self.show_status)
        self.main_widget.generation_completed.connect(self.on_generation_completed)
        self.setCentralWidget(self.main_widget)

        self.status_label = QLabel()
        self.statusBar().addWidget(self.status_label)
        self.set_parameters_unspecified_restrictions()

        self.set_menubar()

    def set_menubar(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu(qtTrId("File"))
        file_menu.addAction(self.get_configurator())
        file_menu.addAction(self.get_settings())

        help_menu = menubar.addMenu(self.tr("Помощь"))
        help_menu.addAction(self.get_about())

    def get_configurator(self) -> QAction:
        action = QAction(self.tr("Конфигуратор"), self)
        action.setShortcuts(QKeySequence("Ctrl+s"))
        action.triggered.connect(self.show_configurator)
        return action

    @Slot()
    def show_configurator(self) -> None:
        if not self.preferences_config.model.current_text_model:
            QMessageBox.warning(
                self,
                self.tr("Ошибка настроек"),
                self.tr(
                    "Невозможно запустить конфигуратор. Текстовая модель не задана."
                ),
            )
            return

        dialog = ConfiguratorDialog(
            parent=self, preferences_config=self.preferences_config
        )
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.main_widget.prompt_editor.prompt = dialog.parameters.prompt
            self.main_widget.generate_quest_configurator(dialog.parameters)

    def get_settings(self) -> QAction:
        action = QAction(self.tr("Настройки"), self)
        action.setMenuRole(QAction.MenuRole.PreferencesRole)
        action.setShortcuts((QKeySequence("Ctrl+,"), QKeySequence("Ctrl+б")))
        action.triggered.connect(self.open_settings)
        return action

    @Slot()
    def open_settings(self) -> None:
        dialog = PreferencesDialog(
            parent=self, preferences_config=self.preferences_config
        )
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.set_parameters_unspecified_restrictions()

    @Slot()
    def on_generation_completed(self) -> None:
        if self.preferences_config.general.show_notifications:
            self.show_generation_complete_tray_message()
        self.set_parameters_unspecified_restrictions()

    def show_generation_complete_tray_message(self) -> None:
        self.tray.showMessage(
            constants_config.app.name,
            "Квест сгенерирован",
            QSystemTrayIcon.MessageIcon.Information,
            constants_config.ui.quest_generated_tray_message_msecs,
        )

    def set_parameters_unspecified_restrictions(self) -> None:
        if not self.preferences_config.model.current_text_model:
            self.show_status(self.tr("Текстовая модель не задана"))
        elif not self.preferences_config.general.save_path:
            self.show_status(self.tr("Путь сохранения не задан"))
        else:
            self.show_status("")

    @Slot(str)
    def show_status(self, status: str) -> None:
        self.status_label.setText(status)

    def get_about(self) -> QAction:
        about_action = QAction(self.tr("О программе"), self)
        about_action.triggered.connect(self.show_about)
        return about_action

    @Slot()
    def show_about(self) -> None:
        QMessageBox.about(
            self,
            self.tr("О программе"),
            f"""
<h3>{constants_config.app.name}</h3>
<p>{self.tr("Версия")} {constants_config.app.version}</p>
<p>{self.tr("Repository")}: <a href="{constants_config.app.repository}">{constants_config.app.repository}</a></p>
            """,
        )

    @Slot()
    def open(self) -> None:
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)
        self.raise_()
        self.activateWindow()

    @Slot()
    def quit(self) -> None:
        self.close_requested = True
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.close_requested or __debug__:
            event.accept()
            return

        self.hide()
        event.ignore()
