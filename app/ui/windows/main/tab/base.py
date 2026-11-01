from config.constants.sections.ui import EditorSize
from generation.workers.base import BaseWorker
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QVBoxLayout, QWidget

from ui.utils.retranslate import RetranslateMixin


class GenerationTab(RetranslateMixin, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.main_layout = QVBoxLayout(self)

    def bind_worker(self, worker: BaseWorker) -> None:
        pass

    def create_plain_text_editor(
        self, size: EditorSize
    ) -> tuple[QLabel, QPlainTextEdit]:
        label = QLabel()
        self.main_layout.addWidget(label)

        editor = QPlainTextEdit()
        editor.setReadOnly(True)
        editor.setMinimumHeight(size.height)
        self.main_layout.addWidget(editor, size.stretch)

        return label, editor

    def create_label_editor(self) -> tuple[QLabel, QLabel]:
        label = QLabel()
        self.main_layout.addWidget(label)

        editor = QLabel()
        self.main_layout.addWidget(editor)

        return label, editor

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
