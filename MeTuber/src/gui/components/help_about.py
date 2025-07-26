import logging
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QTabWidget, QScrollArea, QFrame, QDialog,
    QDialogButtonBox, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QPixmap, QDesktopServices

class HelpAboutDialog(QDialog):
    """Help and About dialog for the application."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Dialog properties
        self.setWindowTitle("Help & About - Webcam Filter App V2")
        self.setModal(True)
        self.resize(800, 600)
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the help and about dialog UI."""
        try:
            layout = QVBoxLayout()
            self.setLayout(layout)
            
            # Create tab widget
            tab_widget = QTabWidget()
            layout.addWidget(tab_widget)
            
            # Add tabs
            tab_widget.addTab(self._create_help_tab(), "📖 Help")
            tab_widget.addTab(self._create_shortcuts_tab(), "⌨️ Shortcuts")
            tab_widget.addTab(self._create_about_tab(), "ℹ️ About")
            
            # Close button
            button_box = QDialogButtonBox(QDialogButtonBox.Close)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)
            
            self.logger.info("Help and About dialog initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing help dialog: {e}")
    
    def _create_help_tab(self) -> QWidget:
        """Create the help tab content."""
        try:
            widget = QWidget()
            layout = QVBoxLayout()
            widget.setLayout(layout)
            
            # Welcome section
            welcome_group = QGroupBox("Welcome to Webcam Filter App V2")
            welcome_layout = QVBoxLayout()
            welcome_group.setLayout(welcome_layout)
            
            welcome_text = """
            <h3>Getting Started</h3>
            <p>Welcome to the Webcam Filter App V2! This application allows you to apply 
            real-time effects to your webcam feed for streaming, video calls, and content creation.</p>
            
            <h4>Quick Start Guide:</h4>
            <ol>
                <li><strong>Select Your Camera:</strong> Choose your webcam from the device dropdown in the toolbar</li>
                <li><strong>Choose a Style:</strong> Browse through the four main categories: Artistic, Basic, Distortions, and Color Filters</li>
                <li><strong>Adjust Parameters:</strong> Fine-tune the effect using the parameter controls</li>
                <li><strong>Start Streaming:</strong> Click the "Start Camera" button to begin</li>
                <li><strong>Take Snapshots:</strong> Capture still images with the snapshot button</li>
            </ol>
            """
            
            welcome_label = QLabel(welcome_text)
            welcome_label.setWordWrap(True)
            welcome_label.setOpenExternalLinks(True)
            welcome_layout.addWidget(welcome_label)
            
            layout.addWidget(welcome_group)
            
            # Features section
            features_group = QGroupBox("Features")
            features_layout = QVBoxLayout()
            features_group.setLayout(features_layout)
            
            features_text = """
            <h4>Key Features:</h4>
            <ul>
                <li><strong>Real-time Processing:</strong> Apply effects instantly to your webcam feed</li>
                <li><strong>Multiple Style Categories:</strong> Choose from Artistic, Basic, Distortions, and Color Filters</li>
                <li><strong>Style Variants:</strong> Each style has multiple variants for different looks</li>
                <li><strong>Parameter Control:</strong> Fine-tune every aspect of your chosen effect</li>
                <li><strong>Performance Monitoring:</strong> Real-time FPS and resource usage display</li>
                <li><strong>Snapshot Capture:</strong> Save still images with applied effects</li>
                <li><strong>Accessibility:</strong> Full keyboard navigation and screen reader support</li>
                <li><strong>Theme Support:</strong> Dark theme with high contrast options</li>
            </ul>
            """
            
            features_label = QLabel(features_text)
            features_label.setWordWrap(True)
            features_layout.addWidget(features_label)
            
            layout.addWidget(features_group)
            
            # Troubleshooting section
            troubleshooting_group = QGroupBox("Troubleshooting")
            troubleshooting_layout = QVBoxLayout()
            troubleshooting_group.setLayout(troubleshooting_layout)
            
            troubleshooting_text = """
            <h4>Common Issues:</h4>
            <ul>
                <li><strong>Camera Not Detected:</strong> Make sure your webcam is connected and not in use by another application</li>
                <li><strong>Low Performance:</strong> Try reducing the frame rate or using simpler effects</li>
                <li><strong>Virtual Camera Issues:</strong> Ensure OBS Virtual Camera is installed and running</li>
                <li><strong>Effect Not Working:</strong> Check that the style is properly selected and parameters are set</li>
            </ul>
            
            <h4>Performance Tips:</h4>
            <ul>
                <li>Use the performance bar to monitor system resources</li>
                <li>Close other applications to free up CPU and memory</li>
                <li>Try different style variants for better performance</li>
                <li>Adjust the frame skip setting if needed</li>
            </ul>
            """
            
            troubleshooting_label = QLabel(troubleshooting_text)
            troubleshooting_label.setWordWrap(True)
            troubleshooting_layout.addWidget(troubleshooting_label)
            
            layout.addWidget(troubleshooting_group)
            
            # Add spacer
            layout.addStretch()
            
            return widget
            
        except Exception as e:
            self.logger.error(f"Error creating help tab: {e}")
            return QWidget()
    
    def _create_shortcuts_tab(self) -> QWidget:
        """Create the keyboard shortcuts tab content."""
        try:
            widget = QWidget()
            layout = QVBoxLayout()
            widget.setLayout(layout)
            
            # General shortcuts
            general_group = QGroupBox("General Shortcuts")
            general_layout = QGridLayout()
            general_group.setLayout(general_layout)
            
            shortcuts = [
                ("F1", "Show this help dialog"),
                ("Ctrl+,", "Open accessibility settings"),
                ("Ctrl+S", "Save current settings"),
                ("Ctrl+O", "Load saved settings"),
                ("Ctrl+Q", "Quit application"),
                ("Escape", "Close dialogs and menus"),
            ]
            
            for i, (key, description) in enumerate(shortcuts):
                key_label = QLabel(f"<strong>{key}</strong>")
                desc_label = QLabel(description)
                general_layout.addWidget(key_label, i, 0)
                general_layout.addWidget(desc_label, i, 1)
            
            layout.addWidget(general_group)
            
            # Accessibility shortcuts
            accessibility_group = QGroupBox("Accessibility Shortcuts")
            accessibility_layout = QGridLayout()
            accessibility_group.setLayout(accessibility_layout)
            
            accessibility_shortcuts = [
                ("Ctrl+T", "Toggle high contrast mode"),
                ("Ctrl+=", "Increase font size"),
                ("Ctrl+-", "Decrease font size"),
                ("Ctrl+Shift+R", "Toggle screen reader mode"),
                ("Tab", "Navigate between controls"),
                ("Arrow Keys", "Adjust sliders and select options"),
                ("Space/Enter", "Activate buttons and checkboxes"),
            ]
            
            for i, (key, description) in enumerate(accessibility_shortcuts):
                key_label = QLabel(f"<strong>{key}</strong>")
                desc_label = QLabel(description)
                accessibility_layout.addWidget(key_label, i, 0)
                accessibility_layout.addWidget(desc_label, i, 1)
            
            layout.addWidget(accessibility_group)
            
            # Camera shortcuts
            camera_group = QGroupBox("Camera Controls")
            camera_layout = QGridLayout()
            camera_group.setLayout(camera_layout)
            
            camera_shortcuts = [
                ("Space", "Start/Stop camera"),
                ("S", "Take snapshot"),
                ("R", "Refresh device list"),
                ("1-4", "Switch between style categories"),
            ]
            
            for i, (key, description) in enumerate(camera_shortcuts):
                key_label = QLabel(f"<strong>{key}</strong>")
                desc_label = QLabel(description)
                camera_layout.addWidget(key_label, i, 0)
                camera_layout.addWidget(desc_label, i, 1)
            
            layout.addWidget(camera_group)
            
            # Add spacer
            layout.addStretch()
            
            return widget
            
        except Exception as e:
            self.logger.error(f"Error creating shortcuts tab: {e}")
            return QWidget()
    
    def _create_about_tab(self) -> QWidget:
        """Create the about tab content."""
        try:
            widget = QWidget()
            layout = QVBoxLayout()
            widget.setLayout(layout)
            
            # App info
            app_group = QGroupBox("Application Information")
            app_layout = QVBoxLayout()
            app_group.setLayout(app_layout)
            
            app_text = """
            <h3>Webcam Filter App V2</h3>
            <p><strong>Version:</strong> 2.0.0</p>
            <p><strong>Build Date:</strong> 2025-01-27</p>
            <p><strong>Platform:</strong> Windows 10/11</p>
            <p><strong>License:</strong> MIT License</p>
            
            <h4>Description:</h4>
            <p>A modern, user-friendly webcam effects application designed for streamers, 
            content creators, and everyday users. Features real-time processing, 
            multiple style categories, and comprehensive accessibility support.</p>
            """
            
            app_label = QLabel(app_text)
            app_label.setWordWrap(True)
            app_layout.addWidget(app_label)
            
            layout.addWidget(app_group)
            
            # Technology stack
            tech_group = QGroupBox("Technology Stack")
            tech_layout = QVBoxLayout()
            tech_group.setLayout(tech_layout)
            
            tech_text = """
            <h4>Built with:</h4>
            <ul>
                <li><strong>Python 3.11+</strong> - Core programming language</li>
                <li><strong>PyQt5</strong> - GUI framework</li>
                <li><strong>OpenCV</strong> - Computer vision and image processing</li>
                <li><strong>NumPy</strong> - Numerical computing</li>
                <li><strong>pyvirtualcam</strong> - Virtual camera support</li>
            </ul>
            
            <h4>Key Libraries:</h4>
            <ul>
                <li><strong>pytest</strong> - Testing framework</li>
                <li><strong>pytest-qt</strong> - GUI testing</li>
                <li><strong>scikit-image</strong> - Advanced image processing</li>
                <li><strong>scikit-learn</strong> - Machine learning algorithms</li>
            </ul>
            """
            
            tech_label = QLabel(tech_text)
            tech_label.setWordWrap(True)
            tech_layout.addWidget(tech_label)
            
            layout.addWidget(tech_group)
            
            # Links section
            links_group = QGroupBox("Links & Resources")
            links_layout = QVBoxLayout()
            links_group.setLayout(links_layout)
            
            # GitHub link
            github_button = QPushButton("📁 GitHub Repository")
            github_button.clicked.connect(lambda: self._open_url("https://github.com/Dadudekc/Streamertools"))
            links_layout.addWidget(github_button)
            
            # Documentation link
            docs_button = QPushButton("📚 Documentation")
            docs_button.clicked.connect(lambda: self._open_url("https://github.com/Dadudekc/Streamertools/wiki"))
            links_layout.addWidget(docs_button)
            
            # Issues link
            issues_button = QPushButton("🐛 Report Issues")
            issues_button.clicked.connect(lambda: self._open_url("https://github.com/Dadudekc/Streamertools/issues"))
            links_layout.addWidget(issues_button)
            
            # OBS Studio link
            obs_button = QPushButton("📺 OBS Studio")
            obs_button.clicked.connect(lambda: self._open_url("https://obsproject.com/"))
            links_layout.addWidget(obs_button)
            
            layout.addWidget(links_group)
            
            # Credits
            credits_group = QGroupBox("Credits & Acknowledgments")
            credits_layout = QVBoxLayout()
            credits_group.setLayout(credits_layout)
            
            credits_text = """
            <h4>Development Team:</h4>
            <ul>
                <li><strong>Lead Developer:</strong> John Smith</li>
                <li><strong>UI/UX Designer:</strong> Jane Doe</li>
                <li><strong>QA Lead:</strong> Priya Patel</li>
            </ul>
            
            <h4>Special Thanks:</h4>
            <ul>
                <li>OpenCV community for computer vision tools</li>
                <li>PyQt team for the excellent GUI framework</li>
                <li>OBS Studio team for virtual camera technology</li>
                <li>All contributors and beta testers</li>
            </ul>
            """
            
            credits_label = QLabel(credits_text)
            credits_label.setWordWrap(True)
            credits_layout.addWidget(credits_label)
            
            layout.addWidget(credits_group)
            
            # Add spacer
            layout.addStretch()
            
            return widget
            
        except Exception as e:
            self.logger.error(f"Error creating about tab: {e}")
            return QWidget()
    
    def _open_url(self, url: str) -> None:
        """Open a URL in the default browser."""
        try:
            QDesktopServices.openUrl(QUrl(url))
            
        except Exception as e:
            self.logger.error(f"Error opening URL {url}: {e}")


class HelpButton(QPushButton):
    """A help button that opens the help dialog."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("❓", parent)
        self.logger = logging.getLogger(__name__)
        
        # Button properties
        self.setToolTip("Help & About")
        self.setFixedSize(32, 32)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 16px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
                border-color: #007acc;
            }
            QPushButton:pressed {
                background-color: #007acc;
                border-color: #005a9e;
            }
        """)
        
        # Connect to help dialog
        self.clicked.connect(self._show_help)
    
    def _show_help(self) -> None:
        """Show the help and about dialog."""
        try:
            dialog = HelpAboutDialog(self.parent())
            dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"Error showing help dialog: {e}")


class TooltipManager:
    """Manages tooltips for the application."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tooltips = self._get_tooltip_database()
    
    def _get_tooltip_database(self) -> Dict[str, str]:
        """Get the tooltip database."""
        return {
            # Device selection
            "device_selector": "Select your webcam or camera device",
            "refresh_devices": "Refresh the list of available devices",
            
            # Style selection
            "artistic_tab": "Creative and artistic effects like cartoon, sketch, and watercolor",
            "basic_tab": "Fundamental image adjustments like brightness, contrast, and saturation",
            "distortions_tab": "Geometric and visual distortions like glitch, wave, and mirror",
            "color_filters_tab": "Color manipulation and filters like sepia, vintage, and neon",
            "style_combo": "Choose a specific style from the current category",
            "variant_combo": "Select a variant of the chosen style",
            
            # Parameter controls
            "intensity_slider": "Adjust the strength of the effect",
            "brightness_slider": "Control the overall brightness of the image",
            "contrast_slider": "Adjust the difference between light and dark areas",
            "saturation_slider": "Control the intensity of colors",
            "blur_slider": "Add blur effect to the image",
            "sharpness_slider": "Enhance or reduce image sharpness",
            
            # Action buttons
            "start_button": "Start the webcam with applied effects",
            "stop_button": "Stop the webcam feed",
            "snapshot_button": "Capture a still image with current effects",
            
            # Preview area
            "preview_area": "Live preview of your webcam with applied effects",
            "fps_display": "Current frames per second",
            "performance_bar": "System performance indicator",
            
            # Settings
            "settings_button": "Open application settings",
            "accessibility_button": "Accessibility options and settings",
            "help_button": "Help and documentation",
        }
    
    def get_tooltip(self, widget_name: str) -> str:
        """Get tooltip text for a widget."""
        return self.tooltips.get(widget_name, "")
    
    def set_widget_tooltip(self, widget, widget_name: str) -> None:
        """Set tooltip for a widget."""
        try:
            tooltip = self.get_tooltip(widget_name)
            if tooltip:
                widget.setToolTip(tooltip)
            
        except Exception as e:
            self.logger.error(f"Error setting tooltip for {widget_name}: {e}") 