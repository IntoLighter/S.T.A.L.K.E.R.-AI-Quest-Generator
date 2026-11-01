from config.constants.sections.ui import EditorSize
from PySide6.QtWidgets import (
    QBoxLayout,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


def get_layout_with_scroll(parent: QWidget) -> QVBoxLayout:
    main_layout = QVBoxLayout(parent)

    scroll = QScrollArea(widgetResizable=True)
    main_layout.addWidget(scroll)

    scroll_widget = QWidget()
    layout = QVBoxLayout(scroll_widget)
    scroll.setWidget(scroll_widget)

    return layout


def add_checkbox_row(layout: QBoxLayout, text: str, *, checked: bool) -> QCheckBox:
    row = QHBoxLayout()
    layout.addLayout(row)

    row.addWidget(QLabel(text))

    checkbox = QCheckBox()
    checkbox.setChecked(checked)
    row.addWidget(checkbox)
    row.addStretch()

    return checkbox


def add_text_editor(layout: QBoxLayout, text: str, size: EditorSize) -> QPlainTextEdit:
    editor = QPlainTextEdit()
    editor.setPlainText(text)
    editor.setMinimumHeight(size.height)
    layout.addWidget(editor, size.stretch)

    return editor
