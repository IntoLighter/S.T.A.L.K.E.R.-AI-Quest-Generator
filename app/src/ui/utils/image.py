from PIL import Image
from PySide6.QtGui import QImage, QPixmap


def get_pixmap(image: Image.Image) -> QPixmap:
    bytes = image.tobytes("raw", "RGB")
    w, h = image.size
    bytes_per_line = w * 3
    qimg = QImage(bytes, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    return pixmap