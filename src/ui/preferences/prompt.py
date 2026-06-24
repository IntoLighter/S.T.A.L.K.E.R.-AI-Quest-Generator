from config.constants import constants_config
from config.preferences import PreferencesConfig
from misc import get_layout_with_scroll
from ui.editor.system_custom_text_editor import SystemCustomTextEditor
from ui.preferences.tab import Tab


class PromptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        self.concept_editor = SystemCustomTextEditor(
            label="Концепт",
            source=self.preferences_config.concept_prompt_source,
            system_content=constants_config.default_concept_prompt,
            custom_content=self.preferences_config.custom_concept_prompt,
            height=constants_config.concept_height,
            stretch=constants_config.concept_stretch,
        )
        self.layout.addWidget(self.concept_editor)

        self.metadata_editor = SystemCustomTextEditor(
            label="Метаданные",
            source=self.preferences_config.metadata_prompt_source,
            system_content=constants_config.default_metadata_prompt,
            custom_content=self.preferences_config.custom_metadata_prompt,
            height=constants_config.metadata_height,
            stretch=constants_config.metadata_stretch,
        )
        self.layout.addWidget(self.metadata_editor)

        self.icon_editor = SystemCustomTextEditor(
            label="Иконка",
            source=self.preferences_config.icon_prompt_source,
            system_content=constants_config.default_icon_prompt,
            custom_content=self.preferences_config.custom_icon_prompt,
            height=constants_config.icon_prompt_height,
            stretch=constants_config.icon_prompt_stretch,
        )
        self.layout.addWidget(self.icon_editor)

    def save(self) -> None:
        self.preferences_config.concept_prompt_source = self.concept_editor.source
        self.preferences_config.custom_concept_prompt = (
            self.concept_editor.custom_content
        )

        self.preferences_config.metadata_prompt_source = self.metadata_editor.source
        self.preferences_config.custom_metadata_prompt = (
            self.metadata_editor.custom_content
        )

        self.preferences_config.icon_prompt_source = self.icon_editor.source
        self.preferences_config.custom_icon_prompt = self.icon_editor.custom_content
