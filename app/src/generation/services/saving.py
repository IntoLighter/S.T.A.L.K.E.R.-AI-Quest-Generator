from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from util.path import get_unique_counter_name_path, get_unique_name_path

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
        on_error: Callable[[Exception], None],
    ) -> None:
        self.save_path = save_path
        self.quest_prompt = quest_prompt
        self.on_error = on_error

    def save(self, result: GenerationResult) -> None:
        paths = QuestPaths.create(self.create_quest_path(result))
        paths.create_dirs()

        for file in self.collect_text_files(result, paths):
            self.save_text_file(file)

        self.save_icon_records(result, paths)

    def create_quest_path(self, result: GenerationResult) -> Path:
        if result.metadata:
            return get_unique_name_path(self.save_path / result.metadata.title)

        return get_unique_counter_name_path(self.save_path)

    def collect_text_files(
        self, result: GenerationResult, paths: QuestPaths
    ) -> list[TextFile]:
        files = [
            TextFile(
                path=paths.quest / "prompt.txt",
                content=self.quest_prompt,
                encoding="utf-8",
            )
        ]

        if result.concept:
            files.append(
                TextFile(
                    path=paths.generation / "concept.txt",
                    content=result.concept,
                    encoding="utf-8",
                )
            )

        if result.metadata_text:
            files.append(
                TextFile(
                    path=paths.generation / "metadata.json",
                    content=result.metadata_text,
                    encoding="utf-8",
                )
            )

        if result.icon_prompt:
            files.append(
                TextFile(
                    path=paths.generation / "icon_prompt.txt",
                    content=result.icon_prompt,
                    encoding="utf-8",
                )
            )

        if result.quest_data:
            for name, content in (
                ("task.xml", result.quest_data.task),
                ("storyline_info.xml", result.quest_data.article),
                ("info.xml", result.quest_data.infoportions),
            ):
                files.append(
                    TextFile(
                        path=paths.resource / name,
                        content=content,
                        encoding="cp1251",
                    )
                )

        return files

    def save_text_file(self, file: TextFile) -> None:
        try:
            file.path.write_text(file.content, encoding=file.encoding)
        except Exception as e:
            self.on_error(e)

    def save_icon_records(self, result: GenerationResult, paths: QuestPaths) -> None:
        if not result.icon_records:
            return

        for path, icon in (
            (paths.generation / "icon.png", result.icon_records.icon),
            (paths.resource / "icon.png", result.icon_records.icon_soc),
        ):
            try:
                icon.save(path)
            except Exception as e:
                self.on_error(e)
