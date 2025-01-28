from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class StyleTabManager(QTabWidget):
    """
    A GUI component that manages style selection tabs, organized by categories.
    """
    style_changed = pyqtSignal(str)  # Emit the selected style name as a signal

    def __init__(self, parent, style_categories, style_instances, settings):
        super().__init__(parent)
        self.style_categories = style_categories
        self.style_instances = style_instances
        self.settings = settings
        self.init_tabs()

    def init_tabs(self):
        """
        Initialize tabs for each category and populate with styles.
        """
        self.clear()  # Clear existing tabs to avoid duplicates during initialization
        for category, styles in self.style_categories.items():
            tab = QWidget()
            layout = QVBoxLayout()
            for style_name in styles:
                layout.addWidget(self.create_style_button(style_name))
            tab.setLayout(layout)
            self.addTab(tab, category)

    def create_style_button(self, style_name):
        """
        Create a button for a given style. When clicked, emits the style_changed signal.
        """
        button = QPushButton(style_name)
        button.setCheckable(True)
        button.setAutoExclusive(True)  # Only one button can be selected in the group

        # Set the default selected style
        if style_name == self.settings.get("style", "Original"):
            button.setChecked(True)

        # Connect button click to emit style name via style_changed signal
        button.clicked.connect(lambda: self.style_changed.emit(style_name))
        return button

    def get_current_style(self):
        """
        Retrieve the currently selected style name.
        """
        for i in range(self.count()):  # Iterate through tabs
            tab = self.widget(i)
            for button in tab.findChildren(QPushButton):  # Find buttons in the tab
                if button.isChecked():
                    return button.text()
        return "Original"  # Fallback if no style is selected
