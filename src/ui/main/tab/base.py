from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QVBoxLayout, QWidget

from generation.worker.main import Worker


class Tab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)

    def bind_worker(self, worker: Worker) -> None:
        pass

    def create_plain_text_editor(
        self, title: str, height: int, stretch: int
    ) -> QPlainTextEdit:
        label = QLabel(title)
        self.layout.addWidget(label)

        editor = QPlainTextEdit()
        editor.setReadOnly(True)
        editor.setMinimumHeight(height)
        self.layout.addWidget(editor, stretch)

        return editor

    def create_label_editor(self, title: str) -> QLabel:
        label = QLabel(title)
        self.layout.addWidget(label)

        editor = QLabel()
        self.layout.addWidget(editor)

        return editor

    @staticmethod
    def append_chunk(editor: QPlainTextEdit, chunk: str) -> None:
        user_cursor = editor.textCursor()
        vertical_scroll_pos = editor.verticalScrollBar().value()

        end_cursor = QTextCursor(editor.document())
        end_cursor.movePosition(QTextCursor.MoveOperation.End)
        end_cursor.insertText(chunk)

        editor.setTextCursor(user_cursor)
        editor.verticalScrollBar().setValue(vertical_scroll_pos)

    def clear(self) -> None:
        pass
