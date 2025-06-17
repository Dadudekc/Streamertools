import logging
import subprocess
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
import av
from pathlib import Path
import cv2

class BaseDeviceManager(ABC):
    """Abstract base class for device management."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._devices: List[Dict[str, str]] = []
        self.refresh_devices()
    
    @abstractmethod
    def enumerate_devices(self) -> List[Dict[str, str]]:
        """Enumerate available devices."""
        pass
    
    @abstractmethod
    def get_device_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """Get detailed information about a specific device."""
        pass
    
    def refresh_devices(self) -> None:
        """Refresh the list of available devices."""
        self._devices = self.enumerate_devices()
        self.logger.info(f"Found {len(self._devices)} devices")
    
    def get_devices(self) -> List[Dict[str, str]]:
        """Get the list of available devices."""
        return self._devices.copy()

class WindowsDeviceManager(BaseDeviceManager):
    """Windows-specific device manager using DirectShow."""
    
    def __init__(self):
        super().__init__()
    
    def enumerate_devices(self) -> List[Dict[str, str]]:
        """Enumerate DirectShow devices on Windows."""
        devices = []
        cmd = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
        
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("[dshow") and '"' in line:
                    start_idx = line.find('"')
                    end_idx = line.rfind('"')
                    if start_idx != -1 and end_idx != -1:
                        device_name = line[start_idx + 1:end_idx]
                        device_id = f"video={device_name}"
                        devices.append({
                            "id": device_id,
                            "name": device_name,
                            "type": "video"
                        })
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error enumerating devices: {e}")
        
        return devices
    
    def get_device_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """Get information about a specific DirectShow device."""
        if not device_id:
            return None
            
        for device in self._devices:
            if device["id"] == device_id:
                return device
        return None

    def validate_device(self, device: str) -> bool:
        """Validate if a video device is available and accessible on Windows."""
        try:
            if not device:
                return False
                
            # Check if device exists in our list
            device_info = self.get_device_info(device)
            if not device_info:
                return False
                
            # Try to open the device with av
            try:
                container = av.open(device, format="dshow")
                container.close()
                return True
            except av.AVError:
                return False
                
        except Exception as e:
            self.logger.error(f"Error validating device: {e}")
            return False

class DeviceManagerFactory:
    """Factory for creating platform-specific device managers."""
    
    @staticmethod
    def create() -> BaseDeviceManager:
        """Create a platform-specific device manager."""
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            return WindowsDeviceManager()
        else:
            raise NotImplementedError(f"Device manager not implemented for {system}") 