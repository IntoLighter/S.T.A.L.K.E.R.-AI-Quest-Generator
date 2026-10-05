from generation.entity import IconRecords
from generation.workers.main import Worker


class NormalWorker(Worker):
    def build_concept(self) -> str | None:
        return self.concept_stage.generate(self.quest_prompt)

    def build_metadata_text(self, concept: str | None) -> str | None:
        if not self.preferences_config.general.should_generate_metadata:
            return None

        return self.metadata_text_stage.generate(concept)

    def build_icon_prompt(self, concept: str | None) -> str | None:
        if not self.preferences_config.general.should_generate_icon:
            return None

        return self.icon_prompt_stage.generate(concept)

    def build_icon_records(self, icon_prompt: str | None) -> IconRecords | None:
        if not icon_prompt:
            return None

        return self.icon_records_stage.generate(icon_prompt)
