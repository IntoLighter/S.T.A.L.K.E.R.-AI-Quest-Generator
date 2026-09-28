from config.constants.main import constants_config
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget


class BaseDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.resize(*constants_config.ui.dialog_size)  # noqa
        self.setWindowFlags(Qt.WindowType.Window)
