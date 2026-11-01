import pathlib

from config.preferences.main import PreferencesConfig
from config.preferences.sections.types import Language
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QBoxLayout,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from utils.translation import ui

from ui.utils.layout import add_checkbox_row
from ui.windows.preferences.tab.base import PreferencesTab

LANGUAGE_NAMES = {
    Language.EN: "English",
    Language.RU: "Русский",
}


class GeneralTab(PreferencesTab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config

        self.main_layout = QVBoxLayout(self)

        self.add_language_editor()
        self.add_notifications_editor()
        self.add_should_generate_editors()
        self.add_save_path_editor()

    def add_language_editor(self) -> None:
        group = QGroupBox(ui("Language"))
        group_layout = QVBoxLayout(group)

        self.interface_language_editor = self.add_language_row(
            group_layout,
            ui("Interface"),
            self.preferences_config.general.interface_language,
        )
        self.generation_language_editor = self.add_language_row(
            group_layout,
            ui("Generation"),
            self.preferences_config.general.generation_language,
        )

        self.main_layout.addWidget(group)

    @staticmethod
    def add_language_row(layout: QBoxLayout, text: str, current: Language) -> QComboBox:
        row = QHBoxLayout()
        layout.addLayout(row)
        row.addWidget(QLabel(text))

        editor = QComboBox()
        for language, name in LANGUAGE_NAMES.items():
            editor.addItem(name, language)
        editor.setCurrentIndex(editor.findData(current))
        row.addWidget(editor)
        row.addStretch()

        return editor

    def add_notifications_editor(self) -> None:
        group = QGroupBox(ui("Notifications"))
        group_layout = QVBoxLayout(group)

        self.show_notifications_editor = add_checkbox_row(
            group_layout,
            ui("Show notifications"),
            checked=self.preferences_config.general.show_notifications,
        )

        self.main_layout.addWidget(group)

    def add_should_generate_editors(self) -> None:
        general = self.preferences_config.general

        self.should_generate_concept_editor = add_checkbox_row(
            self.main_layout,
            ui("Generate concept"),
            checked=general.should_generate_concept,
        )
        self.should_generate_metadata_editor = add_checkbox_row(
            self.main_layout,
            ui("Generate metadata"),
            checked=general.should_generate_metadata,
        )
        self.should_generate_icon_editor = add_checkbox_row(
            self.main_layout,
            ui("Generate icon"),
            checked=general.should_generate_icon,
        )

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
        self.preferences_config.general.generation_language = Language(
            self.generation_language_editor.currentData()
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

        save_path_str = self.save_path_editor.text()
        save_path = pathlib.Path(save_path_str) if save_path_str else None
        self.preferences_config.general.save_path = save_path
