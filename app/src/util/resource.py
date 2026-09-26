from PySide6.QtCore import QFile, QIODevice


def read_resource(path: str) -> str:
    file = QFile(path)

    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        raise RuntimeError(f"Не удалось открыть ресурс: {path}")

    try:
        return bytes(file.readAll()).decode("utf-8")
    finally:
        file.close()
