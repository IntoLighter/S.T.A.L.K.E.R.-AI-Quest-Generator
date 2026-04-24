from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSlider,
    QTextEdit,
)

from config.constants import constants_config
from config.preferences import ModelType, PreferencesConfig
from generation.model.local import LocalModel
from generation.model.remote import RemoteModel
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

        self.local_model_dropdown = QComboBox()
        model = LocalModel(preferences_config)
        self.local_model_dropdown.addItems(model.get_models())
        index = self.local_model_dropdown.findText(preferences_config.local_model)
        self.local_model_dropdown.setCurrentIndex(index)
        self.layout.addWidget(self.local_model_dropdown)

        self.remote_model_dropdown = QComboBox()
        model = RemoteModel(preferences_config)
        self.remote_model_dropdown.addItems(model.get_models())
        index = self.remote_model_dropdown.findText(preferences_config.remote_model)
        self.remote_model_dropdown.setCurrentIndex(index)
        self.layout.addWidget(self.remote_model_dropdown)

        self.group.buttonToggled.connect(self.update_text_model_dropdown)
        self.update_text_model_dropdown()

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
    def update_text_model_dropdown(self):
        button_to_dropdown = {
            self.local_model_button: self.local_model_dropdown,
            self.remote_model_button: self.remote_model_dropdown,
        }

        current_dropdown = button_to_dropdown[self.group.checkedButton()]
        other_dropdown = next(
            v for v in button_to_dropdown.values() if v != current_dropdown
        )
        current_dropdown.show()
        other_dropdown.hide()

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

        self.preferences_config.local_model = self.local_model_dropdown.currentText()
        self.preferences_config.remote_model = self.remote_model_dropdown.currentText()

        self.preferences_config.concept_temperature = (
            self.concept_temperature_slider.value() / 100
        )

        self.preferences_config.concept_top_p = self.concept_top_p_slider.value() / 100

        self.preferences_config.icon_workflow_value = (
            self.icon_workflow_editor.toPlainText()
        )
