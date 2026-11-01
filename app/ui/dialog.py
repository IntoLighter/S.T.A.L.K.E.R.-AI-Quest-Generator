from config.constants.main import constants_config
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QDialog, QHBoxLayout, QPushButton, QWidget
from utils.translation import ui


class BaseDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.resize(*constants_config.ui.dialog_size)
        self.setWindowFlags(Qt.WindowType.Window)

    def add_close_buttons(self, layout: QBoxLayout, accept_text: str) -> None:
        row = QHBoxLayout()
        layout.addLayout(row)

        ok_btn = QPushButton(accept_text)
        ok_btn.clicked.connect(self.accept)
        row.addWidget(ok_btn, stretch=1)

        cancel_btn = QPushButton(ui("Cancel"))
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(cancel_btn, stretch=1)
