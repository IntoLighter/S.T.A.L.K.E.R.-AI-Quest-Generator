from PySide6.QtWidgets import QMessageBox, QWidget


def show_generation_start_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, parent.tr("Ошибка запуска генерации"), text)
