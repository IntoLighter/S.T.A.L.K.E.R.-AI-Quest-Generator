from config.layout import layout_config
from config.preferences import PreferencesConfig
from config.resources import resources_config

from ui.utils.layout import get_layout_with_scroll
from ui.widgets.system_custom_text_editor import SystemCustomTextEditor
from ui.windows.preferences.tab.base import Tab


class PromptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        self.concept_editor = SystemCustomTextEditor(
            label=self.tr("Концепт"),
            source=self.preferences_config.concept_prompt.source,
            system_content=resources_config.default_concept_prompt,
            custom_content=self.preferences_config.concept_prompt.custom,
            height=layout_config.concept_height,
            stretch=layout_config.concept_stretch,
        )
        self.layout.addWidget(self.concept_editor)

        self.metadata_editor = SystemCustomTextEditor(
            label=self.tr("Метаданные"),
            source=self.preferences_config.metadata_prompt.source,
            system_content=resources_config.default_metadata_prompt,
            custom_content=self.preferences_config.metadata_prompt.custom,
            height=layout_config.metadata_height,
            stretch=layout_config.metadata_stretch,
        )
        self.layout.addWidget(self.metadata_editor)

        self.icon_editor = SystemCustomTextEditor(
            label=self.tr("Иконка"),
            source=self.preferences_config.icon_prompt.source,
            system_content=resources_config.default_icon_prompt,
            custom_content=self.preferences_config.icon_prompt.custom,
            height=layout_config.icon_prompt_height,
            stretch=layout_config.icon_prompt_stretch,
        )
        self.layout.addWidget(self.icon_editor)

    def save(self) -> None:
        self.preferences_config.concept_prompt.source = self.concept_editor.source
        self.preferences_config.concept_prompt.custom = (
            self.concept_editor.custom_content
        )

        self.preferences_config.metadata_prompt.source = self.metadata_editor.source
        self.preferences_config.metadata_prompt.custom = (
            self.metadata_editor.custom_content
        )

        self.preferences_config.icon_prompt.source = self.icon_editor.source
        self.preferences_config.icon_prompt.custom = self.icon_editor.custom_content
