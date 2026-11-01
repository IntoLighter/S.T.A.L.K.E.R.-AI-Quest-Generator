from config.constants.main import constants_config
from generation.entity import QuestData
from generation.workers.base import BaseWorker
from PySide6.QtCore import Slot
from utils.translation import ui

from ui.windows.main.tab.base import Tab


class MetadataTab(Tab):
    def __init__(self) -> None:
        super().__init__()
        self.metadata_label, self.metadata_editor = self.create_plain_text_editor(
            constants_config.ui.metadata_editor_size,
        )
        self.task_label, self.task_editor = self.create_plain_text_editor(
            constants_config.ui.editor_size,
        )
        self.article_label, self.article_editor = self.create_plain_text_editor(
            constants_config.ui.editor_size,
        )
        self.infoportions_label, self.infoportions_editor = (
            self.create_plain_text_editor(
                constants_config.ui.editor_size,
            )
        )
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.metadata_label.setText(ui("Metadata"))
        self.task_label.setText(ui("Task"))
        self.article_label.setText(ui("Description"))
        self.infoportions_label.setText(ui("Info portions"))

    def bind_worker(self, worker: BaseWorker) -> None:
        worker.metadata_chunk_ready.connect(self.show_metadata_chunk)
        worker.metadata_ready.connect(self.update_metadata)
        worker.quest_data_ready.connect(self.show_quest_data)

    @Slot(str)
    def show_metadata_chunk(self, chunk: str) -> None:
        self.append_chunk(self.metadata_editor, chunk)

    @Slot(str)
    def update_metadata(self, metadata: str) -> None:
        self.metadata_editor.setPlainText(metadata)

    @Slot(QuestData)
    def show_quest_data(self, quest_data: QuestData) -> None:
        editor_to_record = {
            self.task_editor: quest_data.task,
            self.article_editor: quest_data.article,
            self.infoportions_editor: quest_data.infoportions,
        }

        for editor, record in editor_to_record.items():
            editor.setPlainText(record)

    def clear(self) -> None:
        self.metadata_editor.clear()
        self.task_editor.clear()
        self.article_editor.clear()
        self.infoportions_editor.clear()
