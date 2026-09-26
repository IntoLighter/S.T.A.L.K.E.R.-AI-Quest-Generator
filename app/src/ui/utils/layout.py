from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget


def get_layout_with_scroll(parent: QWidget) -> QVBoxLayout:
    main_layout = QVBoxLayout(parent)

    scroll = QScrollArea(widgetResizable=True)
    main_layout.addWidget(scroll)

    scroll_widget = QWidget()
    layout = QVBoxLayout(scroll_widget)
    scroll.setWidget(scroll_widget)

    return layout