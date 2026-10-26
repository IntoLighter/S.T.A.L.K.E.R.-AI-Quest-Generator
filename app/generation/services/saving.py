from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config.constants.main import constants_config
from utils.path import get_unique_counter_name_path, get_unique_name_path

from generation.entity import GenerationResult


@dataclass
class TextFile:
    path: Path
    content: str
    encoding: str


@dataclass
class QuestPaths:
    quest: Path
    generation: Path
    resource: Path

    @classmethod
    def create(cls, quest: Path) -> QuestPaths:
        return cls(
            quest=quest,
            generation=quest / "generation",
            resource=quest / "resource",
        )

    def create_dirs(self) -> None:
        for path in (self.quest, self.generation, self.resource):
            path.mkdir(parents=True)


class QuestSaver:
    def __init__(
        self,
        save_path: Path,
        quest_prompt: str,
    ) -> None:
        self.save_path = save_path
        self.quest_prompt = quest_prompt
        self.errors: list[Exception] = []

    def save(self, result: GenerationResult) -> list[Exception]:
        self.errors = []
        try:
            paths = QuestPaths.create(self.create_quest_path(result))
            paths.create_dirs()
        except Exception as e:
            self.errors.append(e)
            return self.errors

        for file in self.collect_text_files(result, paths):
            self.save_text_file(file)

        self.save_icon_records(result, paths)

        return self.errors

    def create_quest_path(self, result: GenerationResult) -> Path:
        if result.metadata:
            return get_unique_name_path(self.save_path / result.metadata.title)

        return get_unique_counter_name_path(self.save_path)

    def collect_text_files(
        self, result: GenerationResult, paths: QuestPaths
    ) -> list[TextFile]:
        generation_encoding = constants_config.generation.generation_encoding
        game_encoding = constants_config.generation.game_encoding

        generation_files = {
            "concept.txt": result.concept,
            "metadata.json": result.metadata_text,
            "icon_prompt.txt": result.icon_prompt,
        }

        resource_files: dict[str, str] = {}
        if result.quest_data:
            resource_files = {
                "task.xml": result.quest_data.task,
                "storyline_info.xml": result.quest_data.article,
                "info.xml": result.quest_data.infoportions,
            }

        return [
            TextFile(
                paths.quest / "prompt.txt", self.quest_prompt, generation_encoding
            ),
            *(
                TextFile(paths.generation / name, content, generation_encoding)
                for name, content in generation_files.items()
                if content
            ),
            *(
                TextFile(paths.resource / name, content, game_encoding)
                for name, content in resource_files.items()
            ),
        ]

    def save_text_file(self, file: TextFile) -> None:
        try:
            file.path.write_text(file.content, encoding=file.encoding)
        except Exception as e:
            self.errors.append(e)

    def save_icon_records(self, result: GenerationResult, paths: QuestPaths) -> None:
        if not result.icon_records:
            return

        for path, icon in (
            (paths.generation / "icon.png", result.icon_records.icon),
            (paths.resource / "icon.png", result.icon_records.icon_game),
        ):
            try:
                icon.save(path)
            except Exception as e:
                self.errors.append(e)
