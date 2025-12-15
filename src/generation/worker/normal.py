from generation.engine.soc import SoCObjectFactory
from generation.entity import GenerationResult
from generation.worker.main import Worker


class NormalWorker(Worker):
    def perform_work(self) -> GenerationResult:
        result = GenerationResult()

        try:
            result.concept = self.create_concept()

            if self.isInterruptionRequested():
                return result

            if self.preferences_config.should_generate_metadata:
                result.metadata_text = self.create_metadata_text(result.concept)

                if self.isInterruptionRequested():
                    return result

                result.metadata = self.create_metadata(result.metadata_text)

                if result.metadata:
                    title_english = self.create_title_english(result.metadata.title)
                    result.game_records = SoCObjectFactory.create_game_records(
                        result.metadata, title_english
                    )
                    self.game_records_ready.emit(result.game_records)

            if self.preferences_config.should_generate_icon:
                result.icon_prompt = self.create_icon_prompt(result.concept)

                if self.isInterruptionRequested():
                    return result

                if result.icon_prompt:
                    result.icon_records = self.create_icon_records_comfy(result.icon_prompt)
        except Exception as e:
            self.handle_exception_perform_work(e)
        finally:
            return result
