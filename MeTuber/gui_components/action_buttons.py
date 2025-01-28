# File: gui_components/action_buttons.py

from PyQt5.QtWidgets import QHBoxLayout, QPushButton


class ActionButtons:
    """
    A GUI component for creating Start, Stop, and Snapshot buttons.
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.start_button = QPushButton("Start Virtual Camera")
        self.stop_button = QPushButton("Stop")
        self.snapshot_button = QPushButton("Take Snapshot")

    def create(self, start_callback, stop_callback, snapshot_callback):
        """
        Creates the layout for action buttons and binds them to callbacks.
        """
        layout = QHBoxLayout()

        # Connect callbacks to button clicks
        self.start_button.clicked.connect(start_callback)
        self.stop_button.clicked.connect(stop_callback)
        self.snapshot_button.clicked.connect(snapshot_callback)

        # Enable all buttons for testing
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.snapshot_button.setEnabled(True)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.snapshot_button)
        return layout
