from PySide6.QtWidgets import QMessageBox, QWidget


def show_generation_start_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, "Ошибка запуска генерации", text)
