import logging
from typing import Dict, List, Any, Optional
from PyQt5.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QComboBox,
    QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

class StyleTabManager(QWidget):
    """Widget for managing style tabs and parameters."""
    
    style_changed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None, categories: Optional[Dict[str, List[str]]] = None, style_instances: Optional[Dict[str, Any]] = None, settings: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Initialize UI
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Add tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        # Set up style data
        self.categories = categories or {}
        self.style_instances = style_instances or {}
        self.settings = settings or {}
        
        # Initialize tabs
        self.init_tabs()
        
    def init_tabs(self) -> None:
        """Initialize style tabs."""
        try:
            self.tab_widget.clear()
            
            # Create tabs for each category
            for category, styles in self.categories.items():
                tab = QWidget()
                tab_layout = QVBoxLayout()
                tab.setLayout(tab_layout)
                
                # Add style combo box
                style_combo = QComboBox()
                for style in styles:
                    style_combo.addItem(style)
                tab_layout.addWidget(style_combo)
                
                # Add tab
                self.tab_widget.addTab(tab, category)
                
                # Connect signals
                style_combo.currentTextChanged.connect(lambda text, c=category: self._on_style_changed(c, text))
                
            # Set current style if provided
            if self.settings.get('style'):
                self.set_current_style(self.settings['style'])
                
            self.logger.info("Style tabs initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing style tabs: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to initialize style tabs: {str(e)}"
            )
            
    def get_current_style(self) -> str:
        """Get the currently selected style.
        
        Returns:
            str: Current style name or empty string if none selected
        """
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            style_combo = current_tab.findChild(QComboBox)
            if style_combo:
                return style_combo.currentText()
        return ""
        
    def set_current_style(self, style_name: str) -> bool:
        """Set the current style.
        
        Args:
            style_name (str): Style name to set
            
        Returns:
            bool: True if style was set successfully, False otherwise
        """
        try:
            # Find style in categories
            for category, styles in self.categories.items():
                if style_name in styles:
                    # Find and set the correct tab
                    for i in range(self.tab_widget.count()):
                        if self.tab_widget.tabText(i) == category:
                            self.tab_widget.setCurrentIndex(i)
                            tab = self.tab_widget.currentWidget()
                            style_combo = tab.findChild(QComboBox)
                            if style_combo:
                                style_combo.setCurrentText(style_name)
                                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error setting current style: {e}")
            return False
            
    def update_styles(self, categories: Dict[str, List[str]], style_instances: Dict[str, Any]) -> None:
        """Update the available styles.
        
        Args:
            categories (dict): Dictionary of style categories and their styles
            style_instances (dict): Dictionary of style instances
        """
        self.categories = categories
        self.style_instances = style_instances
        self.init_tabs()
        
    def _on_style_changed(self, category: str, style_name: str) -> None:
        """Handle style selection change.
        
        Args:
            category (str): Style category
            style_name (str): Selected style name
        """
        self.style_changed.emit(style_name) 