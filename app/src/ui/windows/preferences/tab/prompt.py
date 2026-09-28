from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig

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
            source=self.preferences_config.prompt.concept.source,
            system_content=constants_config.resources.default_concept_prompt,
            custom_content=self.preferences_config.prompt.concept.custom,
            height=constants_config.ui.concept_height,
            stretch=constants_config.ui.concept_stretch,
        )
        self.layout.addWidget(self.concept_editor)

        self.metadata_editor = SystemCustomTextEditor(
            label=self.tr("Метаданные"),
            source=self.preferences_config.prompt.metadata.source,
            system_content=constants_config.resources.default_metadata_prompt,
            custom_content=self.preferences_config.prompt.metadata.custom,
            height=constants_config.ui.metadata_height,
            stretch=constants_config.ui.metadata_stretch,
        )
        self.layout.addWidget(self.metadata_editor)

        self.icon_editor = SystemCustomTextEditor(
            label=self.tr("Иконка"),
            source=self.preferences_config.prompt.icon.source,
            system_content=constants_config.resources.default_icon_prompt,
            custom_content=self.preferences_config.prompt.icon.custom,
            height=constants_config.ui.icon_prompt_height,
            stretch=constants_config.ui.icon_prompt_stretch,
        )
        self.layout.addWidget(self.icon_editor)

    def save(self) -> None:
        self.preferences_config.prompt.concept.source = self.concept_editor.source
        self.preferences_config.prompt.concept.custom = (
            self.concept_editor.custom_content
        )

        self.preferences_config.prompt.metadata.source = self.metadata_editor.source
        self.preferences_config.prompt.metadata.custom = (
            self.metadata_editor.custom_content
        )

        self.preferences_config.prompt.icon.source = self.icon_editor.source
        self.preferences_config.prompt.icon.custom = self.icon_editor.custom_content

