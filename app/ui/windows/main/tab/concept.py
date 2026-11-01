from config.constants.main import constants_config
from generation.workers.base import BaseWorker
from PySide6.QtCore import Slot
from utils.translation import ui

from ui.windows.main.tab.base import Tab


class ConceptTab(Tab):
    def __init__(self) -> None:
        super().__init__()
        self.concept_label, self.concept_editor = self.create_plain_text_editor(
            constants_config.ui.concept_editor_size,
        )
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.concept_label.setText(ui("Concept"))

    def bind_worker(self, worker: BaseWorker) -> None:
        worker.concept_chunk_ready.connect(self.show_concept_chunk)

    @Slot(str)
    def show_concept_chunk(self, chunk: str) -> None:
        self.append_chunk(self.concept_editor, chunk)

    def clear(self) -> None:
        self.concept_editor.clear()
