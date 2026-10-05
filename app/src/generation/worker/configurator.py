from config.preferences.main import PreferencesConfig

from generation.entity import ConfiguratorParameters, IconRecords
from generation.model.text.main import TextModel
from generation.worker.main import Worker


class ConfiguratorWorker(Worker):
    def __init__(
        self,
        preferences_config: PreferencesConfig,
        text_model: TextModel,
        prompt: str,
        parameters: ConfiguratorParameters,
    ) -> None:
        super().__init__(
            preferences_config=preferences_config, text_model=text_model, prompt=prompt
        )
        self.parameters = parameters

    def build_concept(self) -> str | None:
        if self.parameters.concept:
            self.concept_chunk_ready.emit(self.parameters.concept)
            return self.parameters.concept

        if self.parameters.should_generate_concept:
            return self.concept_stage.generate(self.quest_prompt)

        return None

    def build_metadata_text(self, concept: str | None) -> str | None:
        if self.parameters.metadata:
            self.metadata_chunk_ready.emit(self.parameters.metadata)
            return self.parameters.metadata

        if self.parameters.should_generate_metadata:
            return self.metadata_text_stage.generate(concept)

        return None

    def build_icon_prompt(self, concept: str | None) -> str | None:
        if self.parameters.icon_prompt:
            self.icon_prompt_chunk_ready.emit(self.parameters.icon_prompt)
            return self.parameters.icon_prompt

        if self.parameters.should_generate_icon:
            return self.icon_prompt_stage.generate(concept)

        return None

    def build_icon_records(self, icon_prompt: str | None) -> IconRecords | None:
        if not icon_prompt or not self.parameters.should_generate_icon:
            return None

        return self.icon_records_stage.generate(icon_prompt)
