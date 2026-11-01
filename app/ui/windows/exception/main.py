import platform
import webbrowser
from urllib.parse import urlencode

from config.constants.main import constants_config
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from utils.translation import err, ui


class ExceptionDialog:
    def __init__(self, stacktrace: str, parent: QWidget | None = None) -> None:
        self.stacktrace = stacktrace

        self.msg = QMessageBox(
            QMessageBox.Icon.Warning,
            ui("Error"),
            err("unexpected_error"),
            parent=parent,
            detailedText=stacktrace,
            buttons=QMessageBox.StandardButton.Close,
        )

        copy_btn = self.msg.addButton(ui("Copy"), QMessageBox.ButtonRole.ActionRole)
        copy_btn.clicked.connect(self.copy)

        report_btn = self.msg.addButton(ui("Report"), QMessageBox.ButtonRole.ActionRole)
        report_btn.clicked.connect(self.report)

    def copy(self) -> None:
        QApplication.clipboard().setText(self.stacktrace)

    def report(self) -> None:
        system_info_dict = {
            "OS": platform.system(),
            "OS Version": platform.version(),
        }

        system_info = "\n".join(f"{k}: {v}" for k, v in system_info_dict.items())

        url = f"{constants_config.app.repository}/issues/new?" + urlencode(
            {
                "template": "bug.yaml",
                "stacktrace": self.stacktrace,
                "system-info": system_info,
            }
        )

        webbrowser.open(url)

    def show(self) -> None:
        self.msg.show()
