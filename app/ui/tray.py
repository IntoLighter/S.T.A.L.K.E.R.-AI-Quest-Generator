from config.constants.main import constants_config
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMenu,
    QSystemTrayIcon,
)
from utils.translation import ui


class Tray(QSystemTrayIcon):
    openRequested = Signal()
    quitRequested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setIcon(QIcon(constants_config.resources.icon_path))

        menu = QMenu()

        self.open_action = QAction(self)
        self.open_action.triggered.connect(self.openRequested)

        self.quit_action = QAction(self)
        self.quit_action.triggered.connect(self.quitRequested)

        menu.addAction(self.open_action)
        menu.addSeparator()
        menu.addAction(self.quit_action)

        self.setContextMenu(menu)

        self.activated.connect(self.on_activated)

        self.retranslate_ui()
        self.show()

    def retranslate_ui(self) -> None:
        self.open_action.setText(ui("Open"))
        self.quit_action.setText(ui("Quit"))

    @Slot(QSystemTrayIcon.ActivationReason)
    def on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.openRequested.emit()
