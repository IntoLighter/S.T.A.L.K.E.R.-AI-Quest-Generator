from config.constants.main import constants_config
from config.preferences.main import PreferencesConfig
from generation.entity import ConfiguratorParameters
from loguru import logger
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QWidget,
)
from utils.translation import err, ui

from ui.dialog import BaseDialog
from ui.utils.layout import get_layout_with_scroll
from ui.utils.message import show_generation_start_error
from ui.widgets.prompt import PromptEditor


class ConfiguratorDialog(BaseDialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig) -> None:
        super().__init__(parent)
        self.setWindowTitle(ui("Configurator"))
        self.preferences_config = preferences_config
        logger.info("Window 'Configurator' created")

        self.main_layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor(preferences_config)
        self.main_layout.addWidget(self.prompt_editor)

        label = QLabel(ui("Concept"))
        self.main_layout.addWidget(label)
        row = QHBoxLayout()
        self.main_layout.addLayout(row)
        label = QLabel(ui("Generate concept"))
        row.addWidget(label)
        self.should_generate_concept_editor = QCheckBox()
        self.should_generate_concept_editor.setChecked(
            self.preferences_config.general.should_generate_concept
        )
        row.addWidget(self.should_generate_concept_editor)
        row.addStretch()
        self.concept_editor = QPlainTextEdit()
        self.concept_editor.setPlainText(self.preferences_config.configurator.concept)
        self.concept_editor.setMinimumHeight(constants_config.ui.concept_height)
        self.main_layout.addWidget(
            self.concept_editor, constants_config.ui.concept_stretch
        )

        label = QLabel(ui("Metadata"))
        self.main_layout.addWidget(label)
        row = QHBoxLayout()
        self.main_layout.addLayout(row)
        label = QLabel(ui("Generate metadata"))
        row.addWidget(label)
        self.should_generate_metadata_editor = QCheckBox()
        self.should_generate_metadata_editor.setChecked(
            self.preferences_config.general.should_generate_metadata
        )
        row.addWidget(self.should_generate_metadata_editor)
        row.addStretch()
        self.metadata_editor = QPlainTextEdit()
        self.metadata_editor.setPlainText(self.preferences_config.configurator.metadata)
        self.metadata_editor.setMinimumHeight(constants_config.ui.metadata_height)
        self.main_layout.addWidget(
            self.metadata_editor, constants_config.ui.metadata_stretch
        )

        label = QLabel(ui("Icon prompt"))
        self.main_layout.addWidget(label)
        row = QHBoxLayout()
        self.main_layout.addLayout(row)
        label = QLabel(ui("Generate icon"))
        row.addWidget(label)
        self.should_generate_icon_editor = QCheckBox()
        self.should_generate_icon_editor.setChecked(
            self.preferences_config.general.should_generate_icon
        )
        row.addWidget(self.should_generate_icon_editor)
        row.addStretch()
        self.icon_prompt_editor = QPlainTextEdit()
        self.icon_prompt_editor.setPlainText(
            self.preferences_config.configurator.icon_prompt
        )
        self.icon_prompt_editor.setMinimumHeight(constants_config.ui.icon_prompt_height)
        self.main_layout.addWidget(
            self.icon_prompt_editor, constants_config.ui.icon_prompt_stretch
        )

        self.add_close_buttons()

    def add_close_buttons(self) -> None:
        row = QHBoxLayout()
        self.main_layout.addLayout(row)

        ok_btn = QPushButton(ui("Generate"))
        ok_btn.clicked.connect(self.accept)
        row.addWidget(ok_btn, stretch=1)

        cancel_btn = QPushButton(ui("Cancel"))
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(cancel_btn, stretch=1)

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

        logger.info("Window 'Settings' accepted")
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
        logger.info("Window 'Settings' rejected")
        super().reject()
