from config.constants import constants_config
from generation.entity import GameRecords
from generation.worker.main import Worker
from PySide6.QtCore import Slot

from ui.main.tab.base import Tab


class MetadataTab(Tab):
    def __init__(self) -> None:
        super().__init__()
        self.metadata_editor = self.create_plain_text_editor(
            self.tr("Метаданные"),
            constants_config.metadata_height,
            constants_config.metadata_stretch,
        )
        self.task_editor = self.create_plain_text_editor(
            self.tr("Задание"),
            constants_config.editor_height,
            constants_config.editor_stretch,
        )
        self.article_editor = self.create_plain_text_editor(
            self.tr("Описание"),
            constants_config.editor_height,
            constants_config.editor_stretch,
        )
        self.infoportions_editor = self.create_plain_text_editor(
            self.tr("Инфопоршни"),
            constants_config.editor_height,
            constants_config.editor_stretch,
        )

    def bind_worker(self, worker: Worker) -> None:
        worker.metadata_chunk_ready.connect(self.show_metadata_chunk)
        worker.metadata_ready.connect(self.update_metadata)
        worker.game_records_ready.connect(self.show_game_records)

    @Slot(str)
    def show_metadata_chunk(self, chunk: str) -> None:
        self.append_chunk(self.metadata_editor, chunk)

    @Slot(str)
    def update_metadata(self, metadata: str) -> None:
        self.metadata_editor.setPlainText(metadata)

    @Slot(GameRecords)
    def show_game_records(self, quest_records: GameRecords) -> None:
        editor_to_record = {
            self.task_editor: quest_records.task,
            self.article_editor: quest_records.article,
            self.infoportions_editor: quest_records.infoportions,
        }

        for editor, record in editor_to_record.items():
            editor.setPlainText(record)

    def clear(self) -> None:
        self.metadata_editor.clear()
        self.task_editor.clear()
        self.article_editor.clear()
        self.infoportions_editor.clear()
