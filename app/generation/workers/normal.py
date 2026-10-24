from generation.entity import IconRecords
from generation.workers.main import Worker


class NormalWorker(Worker):
    def build_concept(self) -> str | None:
        return self.concept_stage.create(self.quest_prompt)

    def build_metadata_text(self, concept: str) -> str | None:
        if self.preferences_config.general.should_generate_metadata:
            return self.metadata_text_stage.create(concept)

        return None

    def build_icon_prompt(self, concept: str) -> str | None:
        if self.preferences_config.general.should_generate_icon:
            return self.icon_prompt_stage.create(concept)

        return None

    def build_icon_records(self, icon_prompt: str) -> IconRecords | None:
        if self.preferences_config.general.should_generate_icon:
            return self.icon_records_stage.create(icon_prompt)

        return None
