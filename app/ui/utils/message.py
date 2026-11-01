from PySide6.QtWidgets import QMessageBox, QWidget
from utils.translation import ui


def show_generation_start_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, ui("Generation start error"), text)
