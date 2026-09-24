from config.constants import constants_config
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMenu,
    QSystemTrayIcon,
)


class Tray(QSystemTrayIcon):
    openRequested = Signal()
    quitRequested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setIcon(QIcon(constants_config.icon_path))

        menu = QMenu()

        open_action = QAction("Открыть", self)
        open_action.triggered.connect(self.openRequested)

        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.quitRequested)

        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(quit_action)

        self.setContextMenu(menu)

        self.activated.connect(self.on_activated)

        self.show()

    @Slot(QSystemTrayIcon.ActivationReason)
    def on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.openRequested.emit()
