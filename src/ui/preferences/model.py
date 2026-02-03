from PySide6.QtCore import Slot, Qt

from config.constants import constants_config
from config.preferences import PreferencesConfig, ModelType
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QLabel,
    QSlider,
    QTextEdit,
)

from config.text import text_config
from misc import get_layout_with_scroll
from ui.preferences.tab import Tab


class ModelTab(Tab):
    def __init__(self, preferences_config: PreferencesConfig) -> None:
        super().__init__()
        self.preferences_config = preferences_config
        self.layout = get_layout_with_scroll(self)

        label = QLabel("Текст")
        self.layout.addWidget(label)

        self.group = QButtonGroup(self)
        row = QHBoxLayout()
        self.layout.addLayout(row)
        self.local_model_button = QRadioButton("Локальная")
        self.remote_model_button = QRadioButton("Удаленная")
        self.group.addButton(self.local_model_button)
        self.group.addButton(self.remote_model_button)
        type_to_button = {
            ModelType.Local: self.local_model_button,
            ModelType.Remote: self.remote_model_button,
        }
        type_to_button[preferences_config.model_type].setChecked(True)
        row.addWidget(self.local_model_button)
        row.addWidget(self.remote_model_button)

        self.local_model_parameters = QWidget()
        self.layout.addWidget(self.local_model_parameters)
        column = QVBoxLayout(self.local_model_parameters)
        column.setContentsMargins(0, 0, 0, 0)
        row = QHBoxLayout()
        column.addLayout(row)
        self.local_model_editor = QLineEdit(self.preferences_config.local_model)
        row.addWidget(self.local_model_editor)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_local_model)
        row.addWidget(reset_button)

        self.remote_model_parameters = QWidget()
        self.layout.addWidget(self.remote_model_parameters)
        column = QVBoxLayout(self.remote_model_parameters)
        column.setContentsMargins(0, 0, 0, 0)
        row = QHBoxLayout()
        column.addLayout(row)
        self.remote_model_editor = QLineEdit(self.preferences_config.remote_model)
        row.addWidget(self.remote_model_editor)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_remote_model)
        row.addWidget(reset_button)

        self.group.buttonToggled.connect(self.update_parameters)
        self.update_parameters()

        row = QHBoxLayout()
        self.layout.addLayout(row)
        label = QLabel("Температура концепта")
        row.addWidget(label)
        self.concept_temperature_slider = QSlider(Qt.Horizontal)
        self.concept_temperature_slider.setRange(0, 200)
        self.concept_temperature_slider.setSingleStep(5)
        self.concept_temperature_slider.setPageStep(10)
        self.concept_temperature_slider.setValue(
            int(self.preferences_config.concept_temperature * 100)
        )
        row.addWidget(self.concept_temperature_slider)
        self.concept_temperature_label = QLabel(
            f"{self.preferences_config.concept_temperature:.2f}"
        )
        row.addWidget(self.concept_temperature_label)
        self.concept_temperature_slider.valueChanged.connect(
            self.update_concept_temperature_label
        )
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_concept_temperature)
        row.addWidget(reset_button)

        row = QHBoxLayout()
        self.layout.addLayout(row)
        label = QLabel("Top-p концепта")
        row.addWidget(label)
        self.concept_top_p_slider = QSlider(Qt.Horizontal)
        self.concept_top_p_slider.setRange(0, 100)
        self.concept_top_p_slider.setSingleStep(5)
        self.concept_top_p_slider.setPageStep(10)
        self.concept_top_p_slider.setValue(
            int(self.preferences_config.concept_top_p * 100)
        )
        row.addWidget(self.concept_top_p_slider)
        self.concept_top_p_label = QLabel(
            f"{self.preferences_config.concept_top_p:.2f}"
        )
        row.addWidget(self.concept_top_p_label)
        self.concept_top_p_slider.valueChanged.connect(self.update_concept_top_p_label)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_concept_top_p)
        row.addWidget(reset_button)

        label = QLabel("Иконка")
        self.layout.addWidget(label)

        row = QHBoxLayout()
        self.layout.addLayout(row)
        label = QLabel("Workflow")
        row.addWidget(label)
        self.icon_workflow_editor = QTextEdit()
        self.icon_workflow_editor.setPlainText(self.preferences_config.icon_workflow)
        self.icon_workflow_editor.setMinimumHeight(
            constants_config.icon_workflow_height
        )
        row.addWidget(self.icon_workflow_editor, constants_config.icon_workflow_stretch)
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_icon_workflow)
        row.addWidget(reset_button)

        self.layout.addStretch()

    @Slot()
    def reset_local_model(self):
        self.local_model_editor.setText(text_config.default_local_model)

    @Slot()
    def reset_remote_model(self):
        self.remote_model_editor.setText(text_config.default_remote_model)

    @Slot()
    def update_parameters(self):
        button_to_parameters = {
            self.local_model_button: self.local_model_parameters,
            self.remote_model_button: self.remote_model_parameters,
        }

        current_parameters = button_to_parameters[self.group.checkedButton()]
        other_parameters = next(
            v for v in button_to_parameters.values() if v != current_parameters
        )
        current_parameters.show()
        other_parameters.hide()

    @Slot(int)
    def update_concept_temperature_label(self, value: int) -> None:
        self.concept_temperature_label.setText(f"{value / 100:.2f}")

    @Slot()
    def reset_concept_temperature(self) -> None:
        self.concept_temperature_slider.setValue(
            int(constants_config.default_concept_temperature * 100)
        )

    @Slot(int)
    def update_concept_top_p_label(self, value: int) -> None:
        self.concept_top_p_label.setText(f"{value / 100:.2f}")

    @Slot()
    def reset_concept_top_p(self) -> None:
        self.concept_top_p_slider.setValue(
            int(constants_config.default_concept_top_p * 100)
        )

    @Slot()
    def reset_icon_workflow(self) -> None:
        self.icon_workflow_editor.setPlainText(constants_config.default_icon_workflow)

    def save(self) -> None:
        button_to_type = {
            self.local_model_button: ModelType.Local,
            self.remote_model_button: ModelType.Remote,
        }
        self.preferences_config.model_type = button_to_type[self.group.checkedButton()]

        self.preferences_config.local_model = self.local_model_editor.text()
        self.preferences_config.remote_model = self.remote_model_editor.text()

        self.preferences_config.concept_temperature = (
            self.concept_temperature_slider.value() / 100
        )

        self.preferences_config.concept_top_p = self.concept_top_p_slider.value() / 100

        self.preferences_config.icon_workflow_value = (
            self.icon_workflow_editor.toPlainText()
        )
