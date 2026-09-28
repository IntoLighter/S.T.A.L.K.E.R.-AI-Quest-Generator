import resource.rc_main  # noqa: F401 I001
import signal
import sys
import traceback
import types

from loguru import logger
from PySide6.QtCore import QCoreApplication, QLibraryInfo, QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from config.constants.main import constants_config
from config.preferences import PreferencesConfig
from config.preferences_repository import preferences_repository
from ui.windows.exception.main import ExceptionDialog
from ui.windows.main.window import MainWindow


def exception_hook(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: types.TracebackType | None,
) -> None:
    stacktrace = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.exception(stacktrace)
    dialog = ExceptionDialog(stacktrace=stacktrace)
    dialog.show()


def on_app_stopped() -> None:
    logger.info("Application closed")


def setup_logging() -> None:
    logger.add(
        constants_config.paths.log_path,
        rotation="5 MB",
        retention=2,
        level="INFO",
        encoding="utf-8",
    )


def create_preferences_config() -> PreferencesConfig:
    try:
        preferences_config = preferences_repository.load()
    except Exception as e:
        logger.exception(e)
        QMessageBox.warning(
            None, QCoreApplication.translate("main", "Ошибка файла настроек"), str(e)
        )
        preferences_config = PreferencesConfig()
    return preferences_config


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    app.setApplicationName(constants_config.app.name)
    app.setWindowIcon(QIcon(constants_config.resources.icon_path))
    app.aboutToQuit.connect(on_app_stopped)

    setup_logging()

    qt_translator = QTranslator()
    qt_translator.load(
        "qt_ru", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    )
    app.installTranslator(qt_translator)

    preferences_config = create_preferences_config()
    logger.debug(f"preferences path: {constants_config.paths.preferences_path}")
    logger.debug(f"log path: {constants_config.paths.log_path}")
    logger.debug(f"save path: {preferences_config.save_path}")

    window = MainWindow(preferences_config=preferences_config)
    window.show()

    logger.info("Application started")
    sys.exit(app.exec())
