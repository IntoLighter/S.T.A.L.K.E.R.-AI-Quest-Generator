from config.ui import ui_config
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget


class BaseDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.resize(*ui_config.dialog_size)  # noqa
        self.setWindowFlags(Qt.WindowType.Window)
