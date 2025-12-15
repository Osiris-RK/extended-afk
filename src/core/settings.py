"""Settings persistence manager"""
import json
import os
import logging

logger = logging.getLogger(__name__)


class AppSettings:
    """Manages application settings with JSON persistence"""

    def __init__(self):
        """Initialize settings manager"""
        # Use APPDATA for settings directory
        self.settings_dir = os.path.join(os.getenv('APPDATA'), 'extended-afk')
        self.settings_file = os.path.join(self.settings_dir, 'settings.json')

        # Default settings
        self.defaults = {
            'version': '1.0',
            'keys': ['l', 't', 'f1'],
            'min_interval_minutes': 10,
            'max_interval_minutes': 14,
            'press_twice': True
        }

        # Load settings from file or use defaults
        self.settings = self.load()

    def load(self):
        """
        Load settings from JSON file.

        Returns:
            dict: Settings dictionary
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    settings = {**self.defaults, **loaded}
                    self._validate(settings)
                    logger.info(f"Settings loaded from {self.settings_file}")
                    return settings
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")
                logger.info("Using default settings")
                return self.defaults.copy()
        else:
            logger.info("Settings file not found, using defaults")
            return self.defaults.copy()

    def save(self):
        """Save current settings to JSON file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.settings_dir, exist_ok=True)

            # Write settings to file
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)

            logger.info(f"Settings saved to {self.settings_file}")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def _validate(self, settings):
        """
        Validate settings values.

        Args:
            settings: Settings dictionary to validate

        Raises:
            ValueError: If settings are invalid
        """
        # Validate keys list
        if not isinstance(settings.get('keys'), list):
            raise ValueError("Keys must be a list")

        # Validate intervals
        min_int = settings.get('min_interval_minutes')
        max_int = settings.get('max_interval_minutes')

        if not isinstance(min_int, (int, float)) or min_int <= 0:
            raise ValueError("min_interval_minutes must be a positive number")

        if not isinstance(max_int, (int, float)) or max_int <= 0:
            raise ValueError("max_interval_minutes must be a positive number")

        if min_int > max_int:
            raise ValueError("min_interval cannot be greater than max_interval")

        # Validate press_twice
        if not isinstance(settings.get('press_twice'), bool):
            raise ValueError("press_twice must be a boolean")

    def get(self, key, default=None):
        """
        Get a setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)

    def set(self, key, value):
        """
        Set a setting value and save.

        Args:
            key: Setting key
            value: New value
        """
        self.settings[key] = value
        self.save()

    def get_all(self):
        """
        Get all settings.

        Returns:
            dict: All settings
        """
        return self.settings.copy()
