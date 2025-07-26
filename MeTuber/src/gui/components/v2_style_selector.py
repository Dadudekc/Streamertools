import logging
from typing import Dict, List, Any, Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QComboBox,
    QLabel, QGroupBox, QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class V2StyleSelector(QWidget):
    """V2 Style Selector with broader tabs and dropdown variants."""
    
    style_changed = pyqtSignal(str, str)  # category, style_name
    variant_changed = pyqtSignal(str, str, str)  # category, style_name, variant
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Style data
        self.categories = {}
        self.style_variants = {}
        self.current_category = ""
        self.current_style = ""
        self.current_variant = ""
        
        # UI components
        self.tab_widget = None
        self.category_combos = {}
        self.variant_combos = {}
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the style selector UI."""
        try:
            layout = QVBoxLayout()
            self.setLayout(layout)
            
            # Title
            title = QLabel("🎨 Style Selection")
            title.setFont(QFont("Segoe UI", 16, QFont.Bold))
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            # Create tab widget for main categories
            self.tab_widget = QTabWidget()
            self.tab_widget.setTabPosition(QTabWidget.North)
            layout.addWidget(self.tab_widget)
            
            # Create tabs for each category
            self._create_category_tabs()
            
            self.logger.info("V2 Style Selector UI initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing V2 Style Selector UI: {e}")
    
    def _create_category_tabs(self) -> None:
        """Create tabs for each style category."""
        try:
            # Define the four main categories as per wireframes
            categories = {
                "Artistic": {
                    "description": "Creative and artistic effects",
                    "styles": ["Cartoon", "Sketch", "Watercolor", "Oil Paint", "Comic", "Anime"]
                },
                "Basic": {
                    "description": "Fundamental image adjustments",
                    "styles": ["Brightness", "Contrast", "Saturation", "Blur", "Sharpness", "Noise"]
                },
                "Distortions": {
                    "description": "Geometric and visual distortions",
                    "styles": ["Glitch", "Wave", "Mirror", "Kaleidoscope", "Fish Eye", "Twist"]
                },
                "Color Filters": {
                    "description": "Color manipulation and filters",
                    "styles": ["Sepia", "Vintage", "Neon", "Monochrome", "Duotone", "Color Balance"]
                }
            }
            
            for category_name, category_data in categories.items():
                tab = self._create_category_tab(category_name, category_data)
                self.tab_widget.addTab(tab, category_name)
            
            # Set default category
            if self.tab_widget.count() > 0:
                self.tab_widget.setCurrentIndex(0)
                self.current_category = self.tab_widget.tabText(0)
            
        except Exception as e:
            self.logger.error(f"Error creating category tabs: {e}")
    
    def _create_category_tab(self, category_name: str, category_data: Dict[str, Any]) -> QWidget:
        """Create a tab for a specific category."""
        try:
            tab = QWidget()
            layout = QVBoxLayout()
            tab.setLayout(layout)
            
            # Category description
            desc_label = QLabel(category_data["description"])
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("color: #cccccc; font-style: italic; margin-bottom: 16px;")
            layout.addWidget(desc_label)
            
            # Style selection group
            style_group = QGroupBox("Style")
            style_layout = QVBoxLayout()
            style_group.setLayout(style_layout)
            
            # Style combo box
            style_combo = QComboBox()
            style_combo.addItems(category_data["styles"])
            style_combo.setCurrentText(category_data["styles"][0])
            style_combo.currentTextChanged.connect(
                lambda text, cat=category_name: self._on_style_changed(cat, text)
            )
            style_layout.addWidget(style_combo)
            
            # Store reference to combo box
            self.category_combos[category_name] = style_combo
            
            layout.addWidget(style_group)
            
            # Variant selection group (initially hidden)
            variant_group = QGroupBox("Variant")
            variant_layout = QVBoxLayout()
            variant_group.setLayout(variant_layout)
            
            # Variant combo box
            variant_combo = QComboBox()
            variant_combo.setVisible(False)  # Hidden by default
            variant_combo.currentTextChanged.connect(
                lambda text, cat=category_name, style=style_combo.currentText(): 
                self._on_variant_changed(cat, style, text)
            )
            variant_layout.addWidget(variant_combo)
            
            # Store reference to variant combo box
            self.variant_combos[category_name] = variant_combo
            
            layout.addWidget(variant_group)
            
            # Add spacer to push content to top
            layout.addStretch()
            
            return tab
            
        except Exception as e:
            self.logger.error(f"Error creating category tab for {category_name}: {e}")
            return QWidget()
    
    def set_available_styles(self, categories: Dict[str, List[str]]) -> None:
        """Set the available styles for each category."""
        try:
            self.categories = categories
            
            # Update combo boxes with available styles
            for category_name, styles in categories.items():
                if category_name in self.category_combos:
                    combo = self.category_combos[category_name]
                    current_text = combo.currentText()
                    
                    # Clear and repopulate
                    combo.clear()
                    combo.addItems(styles)
                    
                    # Try to restore previous selection
                    if current_text in styles:
                        combo.setCurrentText(current_text)
                    elif styles:
                        combo.setCurrentText(styles[0])
            
            self.logger.info("Available styles updated")
            
        except Exception as e:
            self.logger.error(f"Error setting available styles: {e}")
    
    def set_style_variants(self, variants: Dict[str, Dict[str, List[str]]]) -> None:
        """Set the available variants for each style."""
        try:
            self.style_variants = variants
            
            # Update variant combo boxes
            for category_name, styles in variants.items():
                if category_name in self.variant_combos:
                    variant_combo = self.variant_combos[category_name]
                    style_combo = self.category_combos.get(category_name)
                    
                    if style_combo:
                        current_style = style_combo.currentText()
                        self._update_variants_for_style(category_name, current_style)
            
            self.logger.info("Style variants updated")
            
        except Exception as e:
            self.logger.error(f"Error setting style variants: {e}")
    
    def _update_variants_for_style(self, category: str, style: str) -> None:
        """Update variants for a specific style."""
        try:
            if category in self.variant_combos:
                variant_combo = self.variant_combos[category]
                
                # Get variants for this style
                variants = self.style_variants.get(category, {}).get(style, [])
                
                if variants:
                    # Show variant combo box
                    variant_combo.setVisible(True)
                    variant_combo.clear()
                    variant_combo.addItems(variants)
                    variant_combo.setCurrentText(variants[0])
                else:
                    # Hide variant combo box
                    variant_combo.setVisible(False)
            
        except Exception as e:
            self.logger.error(f"Error updating variants for {category}/{style}: {e}")
    
    def _on_style_changed(self, category: str, style: str) -> None:
        """Handle style selection change."""
        try:
            self.current_category = category
            self.current_style = style
            
            # Update variants for the new style
            self._update_variants_for_style(category, style)
            
            # Emit style changed signal
            self.style_changed.emit(category, style)
            
            self.logger.info(f"Style changed to {category}/{style}")
            
        except Exception as e:
            self.logger.error(f"Error handling style change: {e}")
    
    def _on_variant_changed(self, category: str, style: str, variant: str) -> None:
        """Handle variant selection change."""
        try:
            self.current_variant = variant
            
            # Emit variant changed signal
            self.variant_changed.emit(category, style, variant)
            
            self.logger.info(f"Variant changed to {category}/{style}/{variant}")
            
        except Exception as e:
            self.logger.error(f"Error handling variant change: {e}")
    
    def get_current_selection(self) -> Dict[str, str]:
        """Get the current style selection."""
        return {
            "category": self.current_category,
            "style": self.current_style,
            "variant": self.current_variant
        }
    
    def set_current_selection(self, category: str, style: str, variant: str = "") -> None:
        """Set the current style selection."""
        try:
            # Set category tab
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == category:
                    self.tab_widget.setCurrentIndex(i)
                    break
            
            # Set style combo
            if category in self.category_combos:
                combo = self.category_combos[category]
                if style in [combo.itemText(j) for j in range(combo.count())]:
                    combo.setCurrentText(style)
            
            # Set variant combo
            if category in self.variant_combos and variant:
                variant_combo = self.variant_combos[category]
                if variant in [variant_combo.itemText(j) for j in range(variant_combo.count())]:
                    variant_combo.setCurrentText(variant)
            
            self.logger.info(f"Current selection set to {category}/{style}/{variant}")
            
        except Exception as e:
            self.logger.error(f"Error setting current selection: {e}")
    
    def get_style_parameters(self) -> Dict[str, Any]:
        """Get parameters for the currently selected style."""
        try:
            # This would typically query the style manager for parameters
            # For now, return a basic structure
            return {
                "category": self.current_category,
                "style": self.current_style,
                "variant": self.current_variant,
                "parameters": {}  # Would be populated by style manager
            }
            
        except Exception as e:
            self.logger.error(f"Error getting style parameters: {e}")
            return {} 