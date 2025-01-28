# File: gui_components/style_tab_manager.py

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal

class StyleTabManager(QTabWidget):
    """
    A GUI component that manages style selection with categorization using tabs.
    """
    style_changed = pyqtSignal(str)  # Signal emits the style name

    def __init__(self, parent, style_categories, style_instances, settings):
        super().__init__(parent)
        self.style_categories = style_categories
        self.style_instances = style_instances
        self.settings = settings
        self.current_style = settings.get("style", "Original")
        self.init_tabs()

    def init_tabs(self):
        for category, styles in self.style_categories.items():
            tab = QWidget()
            layout = QVBoxLayout()
            list_widget = QListWidget()
            for style_name in styles:
                item = QListWidgetItem(style_name)
                list_widget.addItem(item)
                if style_name == self.current_style:
                    list_widget.setCurrentItem(item)
            list_widget.itemClicked.connect(self.on_item_clicked)
            layout.addWidget(list_widget)
            tab.setLayout(layout)
            self.addTab(tab, category)

    def on_item_clicked(self, item):
        self.current_style = item.text()
        self.style_changed.emit(self.current_style)  # Emit the style name

    def get_current_style(self):
        return self.current_style
