"""Package entry point for the MeTuber application.

This thin wrapper allows the project to be executed with either

    python -m MeTuber

or after installation via the console-script defined in setup.py:

    metuber

It simply delegates to the main() function provided by the existing
`webcam_filter_pyqt5.py` module so that we avoid duplicating startup
logic and keep a single authoritative entry point.
"""

from importlib import import_module
from types import ModuleType
from typing import NoReturn


def _get_webcam_module() -> ModuleType:
    """Import the webcam GUI module lazily to avoid heavy imports at start-up."""
    return import_module("MeTuber.webcam_filter_pyqt5")


def main() -> NoReturn:  # pragma: no cover – thin wrapper
    """Run the MeTuber QT application."""
    webcam_module = _get_webcam_module()
    if hasattr(webcam_module, "main"):
        webcam_module.main()  # type: ignore[func-returns-value]
    else:
        raise RuntimeError("Expected 'main' function in MeTuber.webcam_filter_pyqt5")


if __name__ == "__main__":
    main() 