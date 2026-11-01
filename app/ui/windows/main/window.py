from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from PySide6.QtCore import QEvent, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSystemTrayIcon,
)
from utils.translation import err, ui

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

        self.set_menubar()
        self.retranslate_ui()

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self) -> None:
        self.file_menu.setTitle(ui("File"))
        self.configurator_action.setText(ui("Configurator"))
        self.settings_action.setText(ui("Settings"))
        self.help_menu.setTitle(ui("Help"))
        self.about_action.setText(ui("About"))
        self.tray.retranslate_ui()
        if not self.main_widget.is_generating:
            self.set_parameters_unspecified_restrictions()

    def set_menubar(self) -> None:
        menubar = self.menuBar()

        self.file_menu = menubar.addMenu("")
        self.configurator_action = self.get_configurator()
        self.file_menu.addAction(self.configurator_action)
        self.settings_action = self.get_settings()
        self.file_menu.addAction(self.settings_action)

        self.help_menu = menubar.addMenu("")
        self.about_action = self.get_about()
        self.help_menu.addAction(self.about_action)

    def get_configurator(self) -> QAction:
        action = QAction(self)
        action.setShortcut(QKeySequence("Ctrl+s"))
        action.triggered.connect(self.show_configurator)
        return action

    @Slot()
    def show_configurator(self) -> None:
        if not self.preferences_config.model.current_text_model:
            QMessageBox.warning(
                self,
                ui("Settings error"),
                err("configurator_text_model_not_set"),
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
        action = QAction(self)
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
            ui("Quest generated"),
            QSystemTrayIcon.MessageIcon.Information,
            constants_config.ui.quest_generated_tray_message_msecs,
        )

    def set_parameters_unspecified_restrictions(self) -> None:
        if not self.preferences_config.model.current_text_model:
            self.show_status(ui("Text model is not set"))
        elif not self.preferences_config.general.save_path:
            self.show_status(ui("Save path is not set"))
        else:
            self.show_status("")

    @Slot(str)
    def show_status(self, status: str) -> None:
        self.status_label.setText(status)

    def get_about(self) -> QAction:
        about_action = QAction(self)
        about_action.triggered.connect(self.show_about)
        return about_action

    @Slot()
    def show_about(self) -> None:
        repo = constants_config.app.repository
        version = ui("Version")
        repository = ui("Repository")

        QMessageBox.about(
            self,
            ui("About"),
            f"""
<h3>{constants_config.app.name}</h3>
<p>{version} {constants_config.app.version}</p>
<p>{repository}: <a href="{repo}">{repo}</a></p>
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
