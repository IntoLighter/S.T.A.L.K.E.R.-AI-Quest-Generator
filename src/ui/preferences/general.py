import os
import pathlib

from config.preferences import PreferencesConfig
from config.text import text_config
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from ui.preferences.tab import Tab


class GeneralTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig):
        super().__init__()
        self.preferences_config = preferences_config

        self.layout = QVBoxLayout(self)
        self.add_should_generate_editors()
        self.add_prompt_template_editor()
        self.add_save_path_editor()

    def add_should_generate_editors(self) -> None:
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

    def add_prompt_template_editor(self) -> None:
        row = QHBoxLayout()
        self.layout.addLayout(row)

        label = QLabel("Шаблон промпта")
        row.addWidget(label)

        self.prompt_template_editor = QTextEdit()
        self.prompt_template_editor.setPlainText(self.preferences_config.prompt_message)
        row.addWidget(self.prompt_template_editor, stretch=1)

        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_prompt_template)
        row.addWidget(reset_button)

    @Slot()
    def reset_prompt_template(self) -> None:
        self.prompt_template_editor.setPlainText(text_config.default_prompt)

    def add_save_path_editor(self) -> None:
        row = QHBoxLayout()
        self.layout.addLayout(row)

        label = QLabel("Путь сохранения")
        row.addWidget(label)

        self.save_path_editor = QLineEdit()
        self.save_path_editor.setReadOnly(True)

        if self.preferences_config.save_path:
            self.save_path_editor.setText(str(self.preferences_config.save_path))

        row.addWidget(self.save_path_editor, stretch=1)

        browse_btn = QPushButton("Выбрать...")
        browse_btn.clicked.connect(self.select_save_path)
        row.addWidget(browse_btn)

        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_save_path)
        row.addWidget(reset_button)

    @Slot()
    def reset_save_path(self) -> None:
        self.save_path_editor.setText("")

    @Slot()
    def select_save_path(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку",
            os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly,
        )
        if folder:
            self.save_path_editor.setText(folder)

    def save(self) -> None:
        self.preferences_config.should_generate_concept = (
            self.should_generate_concept_editor.isChecked()
        )
        self.preferences_config.should_generate_metadata = (
            self.should_generate_metadata_editor.isChecked()
        )
        self.preferences_config.should_generate_icon = (
            self.should_generate_icon_editor.isChecked()
        )

        self.preferences_config.prompt_message = (
            self.prompt_template_editor.toPlainText()
        )

        save_path_str = self.save_path_editor.text()

        if save_path_str:
            save_path = pathlib.Path(save_path_str)
        else:
            save_path = None

        self.preferences_config.save_path = save_path
