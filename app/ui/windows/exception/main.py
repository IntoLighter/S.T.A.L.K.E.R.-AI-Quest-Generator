import platform
import webbrowser
from urllib.parse import urlencode

from config.constants.main import constants_config
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from utils.translation import err, ui


class ExceptionDialog(QMessageBox):
    def __init__(self, stacktrace: str, parent: QWidget | None = None) -> None:
        super().__init__(
            QMessageBox.Icon.Warning,
            ui("Error"),
            err("unexpected_error"),
            parent=parent,
            detailedText=stacktrace,
            buttons=QMessageBox.StandardButton.Close,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.stacktrace = stacktrace

        copy_btn = self.addButton(ui("Copy"), QMessageBox.ButtonRole.ActionRole)
        copy_btn.clicked.connect(self.copy)

        report_btn = self.addButton(ui("Report"), QMessageBox.ButtonRole.ActionRole)
        report_btn.clicked.connect(self.report)

    @Slot()
    def copy(self) -> None:
        QApplication.clipboard().setText(self.stacktrace)

    @Slot()
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
