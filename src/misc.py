import sys
from functools import wraps
from pathlib import Path

from loguru import logger

from config.constants import constants_config
from PIL import Image
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


def get_prompt_from_file(filename: str):
    path = constants_config.prompt_path / filename
    return path.read_text(encoding="utf-8")


def get_resource_file_content(path: Path):
    return path.read_text(encoding="utf-8")


def get_unique_name_path(path: Path) -> Path:
    new_path = path
    counter = 1

    while new_path.exists():
        new_path = new_path.with_name(f"{path.name} {counter}")
        counter += 1

    return new_path


def get_unique_counter_name_path(path: Path) -> Path:
    counter = 1
    new_path = path / str(counter)

    while new_path.exists():
        counter += 1
        new_path = new_path.with_name(f"{counter}")

    return new_path


def get_pixmap(image: Image.Image) -> QPixmap:
    bytes = image.tobytes("raw", "RGB")
    w, h = image.size
    bytes_per_line = w * 3
    qimg = QImage(bytes, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    return pixmap


def get_layout_with_scroll(parent: QWidget):
    main_layout = QVBoxLayout(parent)

    scroll = QScrollArea(widgetResizable=True)
    main_layout.addWidget(scroll)

    scroll_widget = QWidget()
    layout = QVBoxLayout(scroll_widget)
    scroll.setWidget(scroll_widget)

    return layout


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{func.__name__} started")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} completed")
        return result

    return wrapper


def show_parameters_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, "Ошибка параметров", text)


def show_settings_error(parent: QWidget, text: str) -> None:
    QMessageBox.warning(parent, "Ошибка настроек", text)


class AppError(Exception):
    pass
