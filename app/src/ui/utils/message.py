from PySide6.QtWidgets import QMessageBox, QWidget


def show_parameters_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, parent.tr("Ошибка параметров"), text)


def show_settings_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, parent.tr("Ошибка настроек"), text)
