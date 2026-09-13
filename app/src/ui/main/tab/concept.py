from config.constants import constants_config
from generation.worker.main import Worker
from PySide6.QtCore import Slot

from ui.main.tab.base import Tab


class ConceptTab(Tab):
    def __init__(self) -> None:
        super().__init__()
        self.concept_editor = self.create_plain_text_editor(
            self.tr("Концепт"),
            constants_config.concept_height,
            constants_config.concept_stretch,
        )

    def bind_worker(self, worker: Worker) -> None:
        worker.concept_chunk_ready.connect(self.show_concept_chunk)

    @Slot(str)
    def show_concept_chunk(self, chunk: str) -> None:
        self.append_chunk(self.concept_editor, chunk)

    def clear(self) -> None:
        self.concept_editor.clear()
