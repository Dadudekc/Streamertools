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
            label = QLabel(param["label"])

            if param["type"] in ["int", "float"]:
                # Create a slider control
                slider_layout = QHBoxLayout()
                slider = QSlider(Qt.Horizontal)

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

                value_label = QLabel(
                    str(slider.value() if param["type"] == "int" else slider.value() / 10)
                )

                # Connect slider events
                slider.valueChanged.connect(
                    lambda value, p=param, lbl=value_label: self.on_slider_change(value, p, lbl, callback)
                )

                slider_layout.addWidget(slider)
                slider_layout.addWidget(value_label)
                self.form_layout.addRow(label, slider_layout)

                self.controls[param["name"]] = slider

            elif param["type"] == "str" and "options" in param:
                # Create a dropdown control
                combo = QComboBox()
                combo.addItems(param["options"])

                # Set the current value
                current_value = current_params.get(param["name"], param["default"])
                index = combo.findText(current_value, Qt.MatchFixedString)
                if index >= 0:
                    combo.setCurrentIndex(index)

                # Connect combo change event
                combo.currentTextChanged.connect(lambda value, p=param: callback(p["name"], value, None))

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
        if param["type"] == "float":
            value = value / 10  # Convert back to float for float sliders

        label_widget.setText(str(value) if param["type"] == "int" else f"{value:.1f}")
        callback(param["name"], value, label_widget)
