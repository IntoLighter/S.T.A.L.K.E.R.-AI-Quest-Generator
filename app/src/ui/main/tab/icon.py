from config.constants import constants_config
from generation.entity import IconRecords
from generation.worker.main import Worker
from ui.utils.image import get_pixmap
from PySide6.QtCore import Slot

from ui.main.tab.base import Tab


class IconTab(Tab):
    def __init__(self) -> None:
        super().__init__()
        self.icon_prompt_editor = self.create_plain_text_editor(
            self.tr("Промпт"),
            constants_config.icon_prompt_height,
            constants_config.icon_prompt_stretch,
        )
        self.icon_soc_editor = self.create_label_editor(self.tr("SoC"))
        self.icon_editor = self.create_label_editor(self.tr("Оригинал"))

    def bind_worker(self, worker: Worker) -> None:
        worker.icon_prompt_chunk_ready.connect(self.show_icon_prompt_chunk)
        worker.icon_ready.connect(self.show_icon)

    @Slot(str)
    def show_icon_prompt_chunk(self, chunk: str) -> None:
        self.append_chunk(self.icon_prompt_editor, chunk)

    @Slot(IconRecords)
    def show_icon(self, icon_records: IconRecords) -> None:
        self.icon_editor.setPixmap(get_pixmap(icon_records.icon))
        self.icon_soc_editor.setPixmap(get_pixmap(icon_records.icon_soc))

    def clear(self) -> None:
        self.icon_prompt_editor.clear()
        self.icon_soc_editor.clear()
        self.icon_editor.clear()
