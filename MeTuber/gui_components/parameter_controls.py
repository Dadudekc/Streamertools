# gui_components/parameter_controls.py

from PyQt5.QtWidgets import QWidget, QFormLayout, QSlider, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from functools import partial  # Import partial to avoid lambda closure issues


class ParameterControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)
        self.controls = {}

    def update_parameters(self, parameters, current_params, callback):
        # Clear existing controls
        self.clear_layout()

        self.controls = {}  # Reset controls

        for param in parameters:
            label = QLabel(param.get("label", "Unknown Parameter"))

            if param["type"] in ["int", "float"]:
                self._add_slider_control(param, current_params, callback, label)

            elif param["type"] == "str" and "options" in param:
                self._add_combobox_control(param, current_params, callback, label)

            else:
                print(f"Unsupported parameter type: {param['type']}")  # Debugging output
                    
    def _add_slider_control(self, param, current_params, callback, label):
        """
        Adds a slider control for numeric parameters (int or float).

        Args:
            param (dict): Parameter definition.
            current_params (dict): Current parameter values.
            callback (function): Function to call when the value changes.
            label (QLabel): The label widget for the parameter.
        """
        slider_layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)

        # Configure slider based on type
        if param["type"] == "int":
            slider.setMinimum(param["min"])
            slider.setMaximum(param["max"])
            slider.setSingleStep(param["step"])
            slider.setValue(current_params.get(param["name"], param["default"]))

        elif param["type"] == "float":
            slider.setMinimum(int(param["min"] * 10))
            slider.setMaximum(int(param["max"] * 10))
            slider.setSingleStep(int(param["step"] * 10))
            slider.setValue(int(current_params.get(param["name"], param["default"]) * 10))

        # Fix layout misalignment by ensuring consistent label formatting
        value_label = QLabel(str(slider.value()))
        value_label.setMinimumWidth(50)  # Ensures space for numbers
        slider_layout.addWidget(label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)

        # Connect value change event
        slider.valueChanged.connect(lambda value: self.on_slider_change(value, param, value_label, callback))

        self.form_layout.addRow(slider_layout)  # Ensures uniform layout

        # Store control reference
        self.controls[param["name"]] = slider

    def _add_combobox_control(self, param, current_params, callback, label):
        combo = QComboBox()
        combo.addItems(param["options"])

        current_value = current_params.get(param["name"], param["default"])
        index = combo.findText(current_value, Qt.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index)

        # Connect combobox selection change to callback
        combo.currentTextChanged.connect(partial(callback, param["name"], combo.currentText(), None))

        self.form_layout.addRow(label, combo)
        self.controls[param["name"]] = combo

    def clear_layout(self):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.form_layout.invalidate()
        self.form_layout.update()
        self.update()

    def on_slider_change(self, value, param, label_widget, callback, is_float):
        """
        Handle slider value changes and update the associated label.

        Args:
            value (int): The new slider value.
            param (dict): The parameter associated with the slider.
            label_widget (QLabel): The label to update with the slider's value.
            callback (function): The callback to invoke with the updated parameter value.
            is_float (bool): Whether the parameter is a float.
        """
        # Adjust value for float sliders
        if is_float:
            value = value / 10  # Convert back to float for display and callback

        # Update the label with the new value
        label_widget.setText(str(value) if not is_float else f"{value:.1f}")

        # Call the callback with the updated value
        callback(param["name"], value, label_widget)
