# gui_components/action_buttons.py

from PyQt5.QtWidgets import QHBoxLayout, QPushButton

class ActionButtons:
    """
    A GUI component that provides start, stop, and snapshot buttons.
    """
    def __init__(self, parent):
        self.parent = parent

    def create(self, start_callback, stop_callback, snapshot_callback):
        layout = QHBoxLayout()

        self.start_button = QPushButton("Start Virtual Camera")
        self.start_button.clicked.connect(start_callback)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(True)  # Ensure button is enabled
        self.stop_button.clicked.connect(stop_callback)

        self.snapshot_button = QPushButton("Take Snapshot")
        self.snapshot_button.setEnabled(True)  # Enable for testing
        self.snapshot_button.clicked.connect(snapshot_callback)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.snapshot_button)

        return layout

