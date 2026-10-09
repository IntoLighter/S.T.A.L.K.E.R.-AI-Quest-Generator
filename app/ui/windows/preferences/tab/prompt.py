from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig

from ui.utils.layout import get_layout_with_scroll
from ui.widgets.text_option import TextOptionEditor
from ui.windows.preferences.tab.base import Tab


class PromptTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        self.concept_editor = TextOptionEditor(
            label=self.tr("Концепт"),
            option=self.preferences_config.prompt.concept,
            height=constants_config.ui.concept_height,
            stretch=constants_config.ui.concept_stretch,
        )
        self.layout.addWidget(self.concept_editor)

        self.metadata_editor = TextOptionEditor(
            label=self.tr("Метаданные"),
            option=self.preferences_config.prompt.metadata,
            height=constants_config.ui.metadata_height,
            stretch=constants_config.ui.metadata_stretch,
        )
        self.layout.addWidget(self.metadata_editor)

        self.id_editor = TextOptionEditor(
            label=self.tr("ID"),
            option=self.preferences_config.prompt.id,
            height=constants_config.ui.id_height,
            stretch=constants_config.ui.id_stretch,
        )
        self.layout.addWidget(self.id_editor)

        self.icon_editor = TextOptionEditor(
            label=self.tr("Иконка"),
            option=self.preferences_config.prompt.icon,
            height=constants_config.ui.icon_prompt_height,
            stretch=constants_config.ui.icon_prompt_stretch,
        )
        self.layout.addWidget(self.icon_editor)
