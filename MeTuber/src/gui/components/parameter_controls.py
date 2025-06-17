import logging
from typing import Dict, Any, List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QSlider, QComboBox, QSpinBox, QDoubleSpinBox,
    QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from styles.base import Style

class ParameterControls(QWidget):
    """Component for managing style parameters."""
    
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.current_style = None
        self.parameter_widgets = {}
        self.init_ui()
    
    def init_ui(self) -> None:
        """Initialize the parameter controls UI."""
        try:
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)
            self.logger.info("Parameter controls initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing parameter controls: {e}")
            QMessageBox.critical(
                self.parent(),
                "Error",
                f"Failed to initialize parameter controls: {str(e)}"
            )
    
    def set_style(self, style: Style) -> None:
        """Set the current style and update parameter controls."""
        try:
            # Clear existing controls
            self.clear_controls()
            
            if not style:
                self.logger.warning("No style provided")
                return
            
            self.current_style = style
            self.logger.info(f"Setting parameters for style: {style.name}")
            
            # Create parameter group
            group = QGroupBox("Style Parameters")
            form_layout = QFormLayout()
            
            # Create controls for each parameter
            for param in style.define_parameters():
                name = param["name"]
                param_type = param["type"]
                default = param.get("default", 0)
                
                # Create appropriate control based on parameter type
                if param_type == "int":
                    control = self._create_int_control(param, default)
                elif param_type == "float":
                    control = self._create_float_control(param, default)
                elif param_type == "str" and "options" in param:
                    control = self._create_option_control(param, default)
                else:
                    self.logger.warning(f"Unsupported parameter type: {param_type}")
                    continue
                
                # Add to form layout
                form_layout.addRow(QLabel(name), control)
                self.parameter_widgets[name] = control
            
            group.setLayout(form_layout)
            self.layout.addWidget(group)
            
        except Exception as e:
            self.logger.error(f"Error setting style parameters: {e}")
            QMessageBox.critical(
                self.parent(),
                "Error",
                f"Failed to set style parameters: {str(e)}"
            )
    
    def _create_int_control(self, param: Dict[str, Any], default: int) -> QSlider:
        """Create an integer parameter control."""
        try:
            control = QSlider(Qt.Horizontal)
            control.setMinimum(param.get("min", 0))
            control.setMaximum(param.get("max", 100))
            control.setValue(default)
            control.setTickPosition(QSlider.TicksBelow)
            control.setTickInterval(param.get("step", 1))
            control.valueChanged.connect(lambda: self._on_parameter_changed())
            return control
            
        except Exception as e:
            self.logger.error(f"Error creating integer control: {e}")
            return QSlider(Qt.Horizontal)
    
    def _create_float_control(self, param: Dict[str, Any], default: float) -> QDoubleSpinBox:
        """Create a float parameter control."""
        try:
            control = QDoubleSpinBox()
            control.setMinimum(param.get("min", 0.0))
            control.setMaximum(param.get("max", 1.0))
            control.setValue(default)
            control.setSingleStep(param.get("step", 0.01))
            control.setDecimals(2)
            control.valueChanged.connect(lambda: self._on_parameter_changed())
            return control
            
        except Exception as e:
            self.logger.error(f"Error creating float control: {e}")
            return QDoubleSpinBox()
    
    def _create_option_control(self, param: Dict[str, Any], default: str) -> QComboBox:
        """Create an option parameter control."""
        try:
            control = QComboBox()
            control.addItems(param["options"])
            if default in param["options"]:
                control.setCurrentText(default)
            control.currentTextChanged.connect(lambda: self._on_parameter_changed())
            return control
            
        except Exception as e:
            self.logger.error(f"Error creating option control: {e}")
            return QComboBox()
    
    def _on_parameter_changed(self) -> None:
        """Handle parameter value changes."""
        try:
            params = self.get_parameters()
            self.parameters_changed.emit(params)
        except Exception as e:
            self.logger.error(f"Error handling parameter change: {e}")
    
    def clear_controls(self) -> None:
        """Clear all parameter controls."""
        try:
            # Remove all widgets from layout
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            self.parameter_widgets.clear()
            self.current_style = None
            self.logger.info("Parameter controls cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing controls: {e}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current parameter values."""
        params = {}
        try:
            if not self.current_style:
                return params
            
            for param in self.current_style.define_parameters():
                name = param["name"]
                param_type = param["type"]
                control = self.parameter_widgets.get(name)
                
                if not control:
                    continue
                
                if param_type == "int":
                    params[name] = control.value()
                elif param_type == "float":
                    params[name] = control.value()
                elif param_type == "str" and "options" in param:
                    params[name] = control.currentText()
            
            self.logger.debug(f"Current parameters: {params}")
            return params
            
        except Exception as e:
            self.logger.error(f"Error getting parameters: {e}")
            return {}
    
    def set_parameters(self, params: Dict[str, Any]) -> None:
        """Set parameter values."""
        try:
            if not self.current_style:
                return
            
            for name, value in params.items():
                control = self.parameter_widgets.get(name)
                if not control:
                    continue
                
                if isinstance(control, QSlider):
                    control.setValue(int(value))
                elif isinstance(control, QDoubleSpinBox):
                    control.setValue(float(value))
                elif isinstance(control, QComboBox):
                    control.setCurrentText(str(value))
            
            self.logger.debug(f"Parameters set to: {params}")
            
        except Exception as e:
            self.logger.error(f"Error setting parameters: {e}")
            QMessageBox.critical(
                self.parent(),
                "Error",
                f"Failed to set parameters: {str(e)}"
            ) 