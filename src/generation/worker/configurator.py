from config.preferences import PreferencesConfig
from generation.engine.soc import SoCObjectFactory

from generation.model.main import Model
from generation.entity import ConfiguratorParameters, GenerationResult
from generation.worker.main import Worker


class ConfiguratorWorker(Worker):
    def __init__(
        self,
        preferences_config: PreferencesConfig,
        text_model: Model,
        prompt: str,
        parameters: ConfiguratorParameters,
    ) -> None:
        super().__init__(preferences_config, text_model, prompt)
        self.parameters = parameters

    def perform_work(self) -> GenerationResult:
        result = GenerationResult()

        try:
            result.concept = self.parameters.concept

            if result.concept:
                self.concept_chunk_ready.emit(result.concept)
            elif self.parameters.should_generate_concept:
                result.concept = self.create_concept()

            if self.isInterruptionRequested():
                return result

            result.metadata_text = self.parameters.metadata

            if result.metadata_text:
                self.metadata_chunk_ready.emit(result.metadata_text)
            elif self.parameters.should_generate_metadata:
                result.metadata_text = self.create_metadata_text(result.concept)

            if self.isInterruptionRequested():
                return result

            if result.metadata_text:
                result.metadata = self.create_metadata(result.metadata_text)

            if result.metadata:
                title_english = self.create_title_english(result.metadata.title)
                result.game_records = SoCObjectFactory.create_game_records(
                    result.metadata, title_english
                )
                self.game_records_ready.emit(result.game_records)

            result.icon_prompt = self.parameters.icon_prompt

            if result.icon_prompt:
                self.icon_prompt_chunk_ready.emit(result.icon_prompt)
            elif self.parameters.should_generate_icon:
                result.icon_prompt = self.create_icon_prompt(result.concept)

            if self.isInterruptionRequested():
                return result

            if result.icon_prompt and self.parameters.should_generate_icon:
                result.icon_records = self.create_icon_records_comfy(result.icon_prompt)
        except Exception as e:
            self.handle_exception_perform_work(e)
        finally:
            return result
