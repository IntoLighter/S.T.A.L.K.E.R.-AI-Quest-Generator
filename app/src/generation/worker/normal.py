from generation.worker.main import Worker


class NormalWorker(Worker):
    def build_concept(self) -> str | None:
        return self.concept_stage.generate()

    def build_metadata_text(self, concept: str | None) -> str | None:
        if not self.preferences_config.general.should_generate_metadata:
            return None

        return self.metadata_text_stage.generate(concept)

    def build_icon_prompt(self, concept: str | None) -> str | None:
        if not self.preferences_config.general.should_generate_icon:
            return None

        return self.icon_prompt_stage.generate(concept)

    @property
    def should_generate_icons(self) -> bool:
        return self.preferences_config.general.should_generate_icon
