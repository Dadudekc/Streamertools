from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox, QPushButton


class DeviceSelector:
    """
    A GUI component for selecting input devices.
    """
    def __init__(self, parent, devices, default_device):
        self.parent = parent
        self.devices = devices
        self.default_device = default_device

    def create(self):
        """
        Creates the layout for the device selector combo box.
        """
        layout = QHBoxLayout()
        label = QLabel("Select Device:")
        self.device_combo = QComboBox()
        self.device_combo.addItems(self.devices)
        self.device_combo.setCurrentText(self.default_device)
        self.device_combo.setEditable(True)  # Allow custom input
        layout.addWidget(label)
        layout.addWidget(self.device_combo)
        return layout


class ActionButtons:
    """
    A GUI component for creating Start, Stop, and Snapshot buttons.
    """
    def __init__(self, parent):
        self.parent = parent

    def create(self, start_callback, stop_callback, snapshot_callback):
        """
        Creates the layout for action buttons and binds them to callbacks.
        """
        layout = QHBoxLayout()

        self.start_button = QPushButton("Start Virtual Camera")
        self.start_button.clicked.connect(start_callback)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(stop_callback)

        self.snapshot_button = QPushButton("Take Snapshot")
        self.snapshot_button.clicked.connect(snapshot_callback)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.snapshot_button)

        return layout
