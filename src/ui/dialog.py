from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget

from config.constants import constants_config


class QWindowDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.resize(*constants_config.dialog_size)  # noqa
        self.setWindowFlags(Qt.WindowType.Window)
