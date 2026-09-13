import platform
import webbrowser
from urllib.parse import urlencode

from config.app import app_config
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget


class ExceptionDialog(QObject):
    def __init__(self, stacktrace: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.stacktrace = stacktrace

        self.msg = QMessageBox(
            QMessageBox.Icon.Warning,
            self.tr("Ошибка"),
            self.tr("Произошла непредвиденная ошибка"),
            parent=parent,
            detailedText=stacktrace,
            buttons=QMessageBox.StandardButton.Close,
        )

        copy_btn = self.msg.addButton(
            self.tr("Копировать"), QMessageBox.ButtonRole.ActionRole
        )
        copy_btn.clicked.connect(self.copy)

        report_btn = self.msg.addButton(
            self.tr("Сообщить"), QMessageBox.ButtonRole.ActionRole
        )
        report_btn.clicked.connect(self.report)

    def copy(self) -> None:
        QApplication.clipboard().setText(self.stacktrace)

    def report(self) -> None:
        system_info_dict = {
            "OS": platform.system(),
            "OS Version": platform.version(),
        }

        system_info = "\n".join(f"{k}: {v}" for k, v in system_info_dict.items())

        url = f"{app_config.repository}/issues/new?" + urlencode(
            {
                "template": "bug.yaml",
                "stacktrace": self.stacktrace,
                "system-info": system_info,
            }
        )

        webbrowser.open(url)

    def show(self) -> None:
        self.msg.show()
