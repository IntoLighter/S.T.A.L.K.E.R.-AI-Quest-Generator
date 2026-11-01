from PySide6.QtWidgets import QTabWidget, QWidget


def get_tabs[T: QWidget](tab_widget: QTabWidget, tab_type: type[T]) -> list[T]:
    return [
        tab
        for i in range(tab_widget.count())
        if isinstance(tab := tab_widget.widget(i), tab_type)
    ]
