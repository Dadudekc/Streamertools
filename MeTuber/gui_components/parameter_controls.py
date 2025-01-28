# File: gui_components/parameter_controls.py

from PyQt5.QtWidgets import QWidget, QFormLayout, QSlider, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt


class ParameterControls(QWidget):
    """
    A GUI component that dynamically generates parameter controls based on the selected style.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)
        self.controls = {}

    def update_parameters(self, parameters, current_params, callback):
        """
        Update the parameter controls based on the selected style's parameters.

        Args:
            parameters (list): List of parameter dictionaries from the style.
            current_params (dict): Current parameter values.
            callback (function): Function to call when a parameter changes.
        """
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
        Add a slider control for numeric parameters (int or float).

        Args:
            param (dict): Parameter definition.
            current_params (dict): Current parameter values.
            callback (function): Function to call when the value changes.
            label (QLabel): The label widget for the parameter.
        """
        slider_layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)

        # Configure slider for int or float parameters
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

        # Add a label to display the current value
        value_label = QLabel(
            str(slider.value() if param["type"] == "int" else slider.value() / 10)
        )

        # Connect slider value changes to the callback
        slider.valueChanged.connect(
            lambda value: self.on_slider_change(value, param, value_label, callback)
        )

        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        self.form_layout.addRow(label, slider_layout)

        # Store the control for reference
        self.controls[param["name"]] = slider

    def _add_combobox_control(self, param, current_params, callback, label):
        """
        Add a combo box control for string parameters with predefined options.

        Args:
            param (dict): Parameter definition.
            current_params (dict): Current parameter values.
            callback (function): Function to call when the value changes.
            label (QLabel): The label widget for the parameter.
        """
        combo = QComboBox()
        combo.addItems(param["options"])

        # Set the current value
        current_value = current_params.get(param["name"], param["default"])
        index = combo.findText(current_value, Qt.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index)

        # Connect combo box value changes to the callback
        combo.currentTextChanged.connect(
            lambda value: callback(param["name"], value, None)
        )

        self.form_layout.addRow(label, combo)
        self.controls[param["name"]] = combo

    def clear_layout(self):
        """
        Clear all widgets from the layout.
        """
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def on_slider_change(self, value, param, label_widget, callback):
        """
        Handle slider value changes and update the associated label.

        Args:
            value (int): The new slider value.
            param (dict): The parameter associated with the slider.
            label_widget (QLabel): The label to update with the slider's value.
            callback (function): The callback to invoke with the updated parameter value.
        """
        # Adjust value for float sliders
        if param["type"] == "float":
            value = value / 10  # Convert back to float for display and callback

        # Update the label with the new value
        label_widget.setText(str(value) if param["type"] == "int" else f"{value:.1f}")

        # Debugging output
        print(f"Slider '{param['name']}' updated: {value}")

        # Call the callback with the updated value
        callback(param["name"], value, label_widget)
