import signal
import sys
import traceback

from config.app import app_config
from config.constants import constants_config
from config.preferences import PreferencesConfig
from loguru import logger
from PySide6.QtCore import QLibraryInfo, QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)
from ui.main.window import MainWindow


def exception_hook(exctype, value, tb):
    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    logger.exception(error_msg)
    QMessageBox.warning(None, "Ошибка", "Произошла непредвиденная ошибка")


def on_app_stopped() -> None:
    logger.info("Application closed")


def setup_logging():
    logger.add(
        constants_config.log_path,
        rotation="5 MB",
        retention=2,
        level="INFO",
        encoding="utf-8",
    )


def create_preferences_config() -> PreferencesConfig:
    try:
        preferences_config = PreferencesConfig.load()
    except Exception as e:
        logger.exception(e)
        QMessageBox.warning(None, "Ошибка файла настроек", str(e))
        preferences_config = PreferencesConfig()
    return preferences_config


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    app.setApplicationName(app_config.name)
    app.setWindowIcon(QIcon(str(constants_config.icon_path)))
    app.aboutToQuit.connect(on_app_stopped)

    setup_logging()

    qt_translator = QTranslator()
    qt_translator.load(
        "qt_ru", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    )
    app.installTranslator(qt_translator)

    preferences_config = create_preferences_config()
    logger.debug(f"preferences path: {constants_config.preferences_path}")
    logger.debug(f"log path: {constants_config.log_path}")
    logger.debug(f"save path: {preferences_config.save_path}")

    window = MainWindow(preferences_config)
    window.show()

    logger.info("Application started")
    sys.exit(app.exec())
