from collections.abc import Callable

from generation.entity import IconRecords
from generation.workers.base import BaseWorker


class NormalWorker(BaseWorker):
    def build_concept(self) -> str | None:
        return self.concept_stage.create(self.quest_prompt)

    def build_metadata_text(self, concept: str) -> str | None:
        return self._build_artifact(
            self.metadata_text_stage.create,
            concept,
            should_generate=self.preferences_config.general.should_generate_metadata,
        )

    def build_icon_prompt(self, concept: str) -> str | None:
        return self._build_artifact(
            self.icon_prompt_stage.create,
            concept,
            should_generate=self.preferences_config.general.should_generate_icon,
        )

    def build_icon_records(self, icon_prompt: str) -> IconRecords | None:
        return self._build_artifact(
            self.icon_records_stage.create,
            icon_prompt,
            should_generate=self.preferences_config.general.should_generate_icon,
        )

    def _build_artifact[T](
        self,
        create: Callable[[str], T | None],
        user_content: str,
        *,
        should_generate: bool,
    ) -> T | None:
        if should_generate:
            return create(user_content)

        return None
