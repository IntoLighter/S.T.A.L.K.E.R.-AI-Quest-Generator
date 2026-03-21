from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget


class QWindowDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Window)
