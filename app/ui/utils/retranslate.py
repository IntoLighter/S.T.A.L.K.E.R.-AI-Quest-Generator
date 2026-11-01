from PySide6.QtCore import QEvent


class RetranslateMixin:
    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)  # ty: ignore[unresolved-attribute]

    def retranslate_ui(self) -> None:
        pass
