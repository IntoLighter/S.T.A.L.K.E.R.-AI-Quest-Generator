from loguru import logger

from config.constants import constants_config
from config.preferences import PreferencesConfig
from generation.entity import ConfiguratorParameters
from misc import get_layout_with_scroll, show_parameters_error
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QWidget,
)

from ui.dialog import Dialog
from ui.editor.prompt import PromptEditor


class ConfiguratorDialog(Dialog):
    def __init__(self, parent: QWidget, preferences_config: PreferencesConfig) -> None:
        super().__init__(parent)
        self.resize(*constants_config.window_dims)  # noqa
        self.setWindowTitle("Конфигуратор")
        self.preferences_config = preferences_config
        logger.info("Window 'Configurator' created")

        self.layout = get_layout_with_scroll(self)

        self.prompt_editor = PromptEditor(preferences_config)
        self.layout.addWidget(self.prompt_editor)

        label = QLabel("Концепт")
        self.layout.addWidget(label)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        label = QLabel("Генерировать концепт")
        row.addWidget(label)
        self.should_generate_concept_editor = QCheckBox()
        self.should_generate_concept_editor.setChecked(
            self.preferences_config.should_generate_concept
        )
        row.addWidget(self.should_generate_concept_editor)
        row.addStretch()
        self.concept_editor = QTextEdit()
        self.concept_editor.setPlainText(self.preferences_config.concept_default)
        self.concept_editor.setMinimumHeight(constants_config.concept_height)
        self.layout.addWidget(self.concept_editor, constants_config.concept_stretch)

        label = QLabel("Метаданные")
        self.layout.addWidget(label)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        label = QLabel("Генерировать метаданные")
        row.addWidget(label)
        self.should_generate_metadata_editor = QCheckBox()
        self.should_generate_metadata_editor.setChecked(
            self.preferences_config.should_generate_metadata
        )
        row.addWidget(self.should_generate_metadata_editor)
        row.addStretch()
        self.metadata_editor = QTextEdit()
        self.metadata_editor.setPlainText(self.preferences_config.metadata_default)
        self.metadata_editor.setMinimumHeight(constants_config.metadata_height)
        self.layout.addWidget(self.metadata_editor, constants_config.metadata_stretch)

        label = QLabel("Промпт иконки")
        self.layout.addWidget(label)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        label = QLabel("Генерировать иконку")
        row.addWidget(label)
        self.should_generate_icon_editor = QCheckBox()
        self.should_generate_icon_editor.setChecked(
            self.preferences_config.should_generate_icon
        )
        row.addWidget(self.should_generate_icon_editor)
        row.addStretch()
        self.icon_prompt_editor = QTextEdit()
        self.icon_prompt_editor.setPlainText(
            self.preferences_config.icon_prompt_default
        )
        self.icon_prompt_editor.setMinimumHeight(constants_config.editor_height)
        self.layout.addWidget(self.icon_prompt_editor, constants_config.editor_stretch)

        self.add_close_buttons()

    def add_close_buttons(self) -> None:
        row = QHBoxLayout()
        self.layout.addLayout(row)

        ok_btn = QPushButton("Сгенерировать")
        ok_btn.clicked.connect(self.accept)
        row.addWidget(ok_btn, stretch=1)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(cancel_btn, stretch=1)

    def accept(self) -> None:
        parameters = self.parameters

        if not (
            parameters.should_generate_concept
            or parameters.should_generate_metadata
            or parameters.should_generate_icon
        ):
            show_parameters_error(self, "Невозможно запустить пустую генерацию.")
            return

        if (
            parameters.should_generate_metadata
            and not parameters.metadata
            and not (parameters.should_generate_concept or parameters.concept)
        ):
            show_parameters_error(
                self, "Невозможно сгенерировать метаданные без концепта."
            )
            return

        if (
            parameters.should_generate_icon
            and not parameters.icon_prompt
            and not (parameters.should_generate_concept or parameters.concept)
        ):
            show_parameters_error(
                self, "Невозможно сгенерировать промпт иконки без концепта."
            )
            return

        logger.info("Window 'Settings' accepted")
        super().accept()

    @property
    def parameters(self) -> ConfiguratorParameters:
        return ConfiguratorParameters(
            self.should_generate_concept_editor.isChecked(),
            self.should_generate_metadata_editor.isChecked(),
            self.should_generate_icon_editor.isChecked(),
            self.prompt_editor.prompt,
            self.concept_editor.toPlainText(),
            self.metadata_editor.toPlainText(),
            self.icon_prompt_editor.toPlainText(),
        )

    def reject(self) -> None:
        logger.info("Window 'Settings' rejected")
        super().reject()
