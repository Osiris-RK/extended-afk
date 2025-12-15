"""Resource path helper for PyInstaller"""
import sys
import os


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    When PyInstaller bundles the application, it extracts files to a temporary
    folder and stores the path in sys._MEIPASS.

    Args:
        relative_path: Path relative to the application root

    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Development mode - use current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
