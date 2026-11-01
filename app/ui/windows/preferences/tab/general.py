import pathlib

from config.preferences.main import PreferencesConfig
from config.preferences.sections.general import DEFAULT_PROMPT
from config.preferences.sections.types import Language
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)
from utils.translation import ui

from ui.windows.preferences.tab.base import Tab

LANGUAGE_NAMES = {
    Language.EN: "English",
    Language.RU: "Русский",
}


class GeneralTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config

        self.main_layout = QVBoxLayout(self)

        self.add_language_editor()
        self.add_notifications_editor()
        self.add_should_generate_editors()
        self.add_prompt_template_editor()
        self.add_save_path_editor()

    def add_language_editor(self) -> None:
        group = QGroupBox(ui("Language"))
        group_layout = QVBoxLayout(group)

        row = QHBoxLayout()
        group_layout.addLayout(row)
        label = QLabel(ui("Interface"))
        row.addWidget(label)
        self.interface_language_editor = QComboBox()
        for language, name in LANGUAGE_NAMES.items():
            self.interface_language_editor.addItem(name, language)
        self.interface_language_editor.setCurrentIndex(
            self.interface_language_editor.findData(
                self.preferences_config.general.interface_language
            )
        )
        row.addWidget(self.interface_language_editor)
        row.addStretch()

        self.main_layout.addWidget(group)

    def add_notifications_editor(self) -> None:
        group = QGroupBox(ui("Notifications"))
        group_layout = QVBoxLayout(group)

        row = QHBoxLayout()
        group_layout.addLayout(row)
        label = QLabel(ui("Show notifications"))
        row.addWidget(label)
        self.show_notifications_editor = QCheckBox()
        self.show_notifications_editor.setChecked(
            self.preferences_config.general.show_notifications
        )
        row.addWidget(self.show_notifications_editor)
        row.addStretch()

        self.main_layout.addWidget(group)

    def add_should_generate_editors(self) -> None:
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

    def add_prompt_template_editor(self) -> None:
        row = QHBoxLayout()
        self.main_layout.addLayout(row)

        label = QLabel(ui("Prompt template"))
        row.addWidget(label)

        self.prompt_template_editor = QPlainTextEdit()
        self.prompt_template_editor.setPlainText(
            self.preferences_config.general.prompt_message
        )
        row.addWidget(self.prompt_template_editor, stretch=1)

        reset_button = QPushButton(ui("Reset"))
        reset_button.clicked.connect(self.reset_prompt_template)
        row.addWidget(reset_button)

    @Slot()
    def reset_prompt_template(self) -> None:
        self.prompt_template_editor.setPlainText(DEFAULT_PROMPT)

    def add_save_path_editor(self) -> None:
        row = QHBoxLayout()
        self.main_layout.addLayout(row)

        label = QLabel(ui("Save path"))
        row.addWidget(label)

        self.save_path_editor = QLineEdit()
        self.save_path_editor.setReadOnly(True)

        if self.preferences_config.general.save_path:
            self.save_path_editor.setText(
                str(self.preferences_config.general.save_path)
            )

        row.addWidget(self.save_path_editor, stretch=1)

        browse_btn = QPushButton(ui("Browse..."))
        browse_btn.clicked.connect(self.select_save_path)
        row.addWidget(browse_btn)

        reset_button = QPushButton(ui("Reset"))
        reset_button.clicked.connect(self.reset_save_path)
        row.addWidget(reset_button)

    @Slot()
    def reset_save_path(self) -> None:
        self.save_path_editor.setText("")

    @Slot()
    def select_save_path(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            ui("Select folder"),
            str(pathlib.Path.home()),
            QFileDialog.Option.ShowDirsOnly,
        )
        if folder:
            self.save_path_editor.setText(folder)

    def save(self) -> None:
        self.preferences_config.general.interface_language = Language(
            self.interface_language_editor.currentData()
        )

        self.preferences_config.general.show_notifications = (
            self.show_notifications_editor.isChecked()
        )

        self.preferences_config.general.should_generate_concept = (
            self.should_generate_concept_editor.isChecked()
        )
        self.preferences_config.general.should_generate_metadata = (
            self.should_generate_metadata_editor.isChecked()
        )
        self.preferences_config.general.should_generate_icon = (
            self.should_generate_icon_editor.isChecked()
        )

        self.preferences_config.general.prompt_message = (
            self.prompt_template_editor.toPlainText()
        )

        save_path_str = self.save_path_editor.text()
        save_path = pathlib.Path(save_path_str) if save_path_str else None
        self.preferences_config.general.save_path = save_path
