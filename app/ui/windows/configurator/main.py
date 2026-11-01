from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from generation.entity import ConfiguratorParameters
from loguru import logger
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
)
from utils.translation import err, ui

from ui.dialog import BaseDialog
from ui.utils.layout import add_checkbox_row, add_text_editor, get_layout_with_scroll
from ui.utils.message import show_generation_start_error
from ui.widgets.prompt import PromptEditor


class ConfiguratorDialog(BaseDialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig) -> None:
        super().__init__(parent)
        self.setWindowTitle(ui("Configurator"))
        self.preferences_config = preferences_config
        logger.info("Window 'Configurator' created")

        self.main_layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor()
        self.main_layout.addWidget(self.prompt_editor)

        general = self.preferences_config.general
        configurator = self.preferences_config.configurator

        self.main_layout.addWidget(QLabel(ui("Concept")))
        self.should_generate_concept_editor = add_checkbox_row(
            self.main_layout,
            ui("Generate concept"),
            checked=general.should_generate_concept,
        )
        self.concept_editor = add_text_editor(
            self.main_layout,
            configurator.concept,
            constants_config.ui.concept_editor_size,
        )

        self.main_layout.addWidget(QLabel(ui("Metadata")))
        self.should_generate_metadata_editor = add_checkbox_row(
            self.main_layout,
            ui("Generate metadata"),
            checked=general.should_generate_metadata,
        )
        self.metadata_editor = add_text_editor(
            self.main_layout,
            configurator.metadata,
            constants_config.ui.metadata_editor_size,
        )

        self.main_layout.addWidget(QLabel(ui("Icon prompt")))
        self.should_generate_icon_editor = add_checkbox_row(
            self.main_layout,
            ui("Generate icon"),
            checked=general.should_generate_icon,
        )
        self.icon_prompt_editor = add_text_editor(
            self.main_layout,
            configurator.icon_prompt,
            constants_config.ui.icon_prompt_editor_size,
        )

        self.add_close_buttons(self.main_layout, ui("Generate"))

    def accept(self) -> None:
        parameters = self.parameters

        if not (
            parameters.should_generate_concept
            or parameters.should_generate_metadata
            or parameters.should_generate_icon
        ):
            show_generation_start_error(self, err("generation_empty"))
            return

        if (
            parameters.should_generate_metadata
            and not parameters.metadata
            and not (parameters.should_generate_concept or parameters.concept)
        ):
            show_generation_start_error(self, err("metadata_without_concept"))
            return

        if (
            parameters.should_generate_icon
            and not parameters.icon_prompt
            and not (parameters.should_generate_concept or parameters.concept)
        ):
            show_generation_start_error(self, err("icon_prompt_without_concept"))
            return

        logger.info("Window 'Configurator' accepted")
        super().accept()

    @property
    def parameters(self) -> ConfiguratorParameters:
        return ConfiguratorParameters(
            should_generate_concept=self.should_generate_concept_editor.isChecked(),
            should_generate_metadata=self.should_generate_metadata_editor.isChecked(),
            should_generate_icon=self.should_generate_icon_editor.isChecked(),
            prompt=self.prompt_editor.prompt,
            concept=self.concept_editor.toPlainText(),
            metadata=self.metadata_editor.toPlainText(),
            icon_prompt=self.icon_prompt_editor.toPlainText(),
        )

    def reject(self) -> None:
        logger.info("Window 'Configurator' rejected")
        super().reject()
