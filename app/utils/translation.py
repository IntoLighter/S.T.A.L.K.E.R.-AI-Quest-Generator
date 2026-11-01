from loguru import logger
from PySide6.QtCore import QCoreApplication, QLibraryInfo, QTranslator

TRANSLATIONS_PATH = ":/translations"
GROUPS = ("ui", "errors")

_translators: list[QTranslator] = []


def ui(text: str) -> str:
    return QCoreApplication.translate("", text)


def err(error_id: str) -> str:
    return QCoreApplication.translate("", error_id)


def set_language(language: str) -> None:
    app = QCoreApplication.instance()
    if app is None:
        raise RuntimeError("QCoreApplication is not created")

    for translator in _translators:
        app.removeTranslator(translator)
    _translators.clear()

    sources = [(f"{group}_{language}", TRANSLATIONS_PATH) for group in GROUPS]
    sources.append(
        (
            f"qt_{language}",
            QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
        )
    )

    for filename, directory in sources:
        translator = QTranslator()
        if translator.load(filename, directory):
            app.installTranslator(translator)
            _translators.append(translator)
        else:
            logger.debug(f"Translation not found: {directory}/{filename}")
