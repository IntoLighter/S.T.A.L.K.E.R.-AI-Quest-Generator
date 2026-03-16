import platform
from urllib.parse import urlencode
import webbrowser

from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

from config.app import app_config


class ExceptionDialog:
    def __init__(self, stacktrace: str, parent: QWidget | None = None) -> None:
        self.stacktrace = stacktrace

        self.msg = QMessageBox(
            QMessageBox.Icon.Warning,
            "Ошибка",
            "Произошла непредвиденная ошибка",
            parent=parent,
            detailedText=stacktrace,
            buttons=QMessageBox.StandardButton.Close,
        )

        copy_btn = self.msg.addButton("Копировать", QMessageBox.ButtonRole.ActionRole)
        copy_btn.clicked.connect(self.copy)

        report_btn = self.msg.addButton("Сообщить", QMessageBox.ButtonRole.ActionRole)
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

    def exec(self) -> None:
        self.msg.exec()
