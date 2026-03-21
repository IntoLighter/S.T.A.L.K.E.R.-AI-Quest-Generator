from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget

from config.preferences import PreferencesConfig


class QWindowDialog(QDialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Window)
        self.resize(*preferences_config.window_dims)  # noqa
