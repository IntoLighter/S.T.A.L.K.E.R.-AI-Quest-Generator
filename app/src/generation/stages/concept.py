from __future__ import annotations

from util.logging import log_execution

from generation.stages.base import TextStage


class ConceptStage(TextStage):
    @log_execution
    def generate(self, quest_prompt: str) -> str | None:
        self.emit_status(self.tr("Генерация концепта"))
        return self.stream(quest_prompt)
