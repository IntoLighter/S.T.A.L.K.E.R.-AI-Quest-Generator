from collections.abc import Callable

from config.preferences.main import PreferencesConfig

from generation.entity import ConfiguratorParameters, IconRecords
from generation.models.text.main import TextModel
from generation.stages.base import TextStreamingStage
from generation.workers.base import BaseWorker


class ConfiguratorWorker(BaseWorker):
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
        return self._build_text(
            self.parameters.concept,
            self.concept_stage,
            self.quest_prompt,
            should_generate=self.parameters.should_generate_concept,
        )

    def build_metadata_text(self, concept: str) -> str | None:
        return self._build_text(
            self.parameters.metadata,
            self.metadata_text_stage,
            concept,
            should_generate=self.parameters.should_generate_metadata,
        )

    def build_icon_prompt(self, concept: str) -> str | None:
        return self._build_text(
            self.parameters.icon_prompt,
            self.icon_prompt_stage,
            concept,
            should_generate=self.parameters.should_generate_icon,
        )

    def build_icon_records(self, icon_prompt: str) -> IconRecords | None:
        return self._build_artifact(
            self.icon_records_stage.create,
            icon_prompt,
            should_generate=self.parameters.should_generate_icon,
        )

    def _build_text(
        self,
        value: str,
        stage: TextStreamingStage,
        user_content: str,
        *,
        should_generate: bool,
    ) -> str | None:
        if value:
            stage.emit_chunk(value)
            return value

        return self._build_artifact(
            stage.create, user_content, should_generate=should_generate
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
