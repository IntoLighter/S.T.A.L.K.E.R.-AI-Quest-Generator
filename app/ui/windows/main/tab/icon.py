from config.constants.main import constants_config
from generation.entity import IconRecords
from generation.workers.base import BaseWorker
from PySide6.QtCore import Slot
from utils.translation import ui

from ui.utils.image import get_pixmap
from ui.windows.main.tab.base import GenerationTab


class IconTab(GenerationTab):
    def __init__(self) -> None:
        super().__init__()
        self.icon_prompt_label, self.icon_prompt_editor = self.create_plain_text_editor(
            constants_config.ui.icon_prompt_editor_size,
        )
        self.icon_game_label, self.icon_game_editor = self.create_label_editor()
        self.icon_label, self.icon_editor = self.create_label_editor()
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.icon_prompt_label.setText(ui("Prompt"))
        self.icon_game_label.setText(ui("Game"))
        self.icon_label.setText(ui("Original"))

    def bind_worker(self, worker: BaseWorker) -> None:
        worker.icon_prompt_chunk_ready.connect(self.show_icon_prompt_chunk)
        worker.icon_ready.connect(self.show_icon)

    @Slot(str)
    def show_icon_prompt_chunk(self, chunk: str) -> None:
        self.append_chunk(self.icon_prompt_editor, chunk)

    @Slot(IconRecords)
    def show_icon(self, icon_records: IconRecords) -> None:
        self.icon_editor.setPixmap(get_pixmap(icon_records.icon))
        self.icon_game_editor.setPixmap(get_pixmap(icon_records.icon_game))

    def clear(self) -> None:
        self.icon_prompt_editor.clear()
        self.icon_game_editor.clear()
        self.icon_editor.clear()
