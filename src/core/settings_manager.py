"""
Settings Manager Module

Handles application settings persistence using QSettings.
"""
from typing import Any, Dict, Optional
from PyQt6.QtCore import QSettings
from pathlib import Path
import json


class SettingsManager:
    """
    Manages application settings and preferences.
    
    Uses Qt's QSettings for persistent storage across sessions.
    Settings are stored in platform-specific locations:
    - macOS: ~/Library/Preferences/com.qaqc.application.plist
    - Windows: Registry
    - Linux: ~/.config/QAQC/application.conf
    """
    
    def __init__(self, organization: str = "QAQC", application: str = "Analysis Application"):
        """Initialize settings manager."""
        self.settings = QSettings(organization, application)
        self._defaults = self._get_default_settings()
        
    def _get_default_settings(self) -> Dict[str, Any]:
        """Define default settings for the application."""
        return {
            # Appearance
            "appearance/theme": "light",  # light, dark, auto
            "appearance/font_size": "medium",  # small, medium, large, xlarge
            "appearance/color_scheme": "geological",  # geological, professional, high_contrast
            "appearance/compact_mode": False,
            
            # Data & Files
            "data/input_dir": str(Path.home() / "Documents"),
            "data/output_dir": str(Path.home() / "Documents" / "QAQC_Output"),
            "data/autosave_enabled": False,
            "data/autosave_interval": 10,  # minutes
            "data/recent_files_limit": 10,
            "data/file_encoding": "utf-8",
            
            # Analysis Defaults
            "analysis/auto_run": False,
            "analysis/crm_database": "crm_database.yaml",
            "analysis/confidence_level": 0.95,
            "analysis/decimal_places": 3,
            "analysis/missing_data": "skip",  # skip, replace_zero, flag
            
            # Visualization
            "visualization/default_dpi": 300,
            "visualization/plot_style": "seaborn-v0_8",
            "visualization/colorblind_friendly": False,
            "visualization/show_gridlines": True,
            "visualization/export_format": "png",
            
            # Performance
            "performance/thread_count": 4,
            "performance/memory_limit_mb": 2048,
            "performance/cache_size_mb": 256,
            "performance/logging_level": "INFO",
            
            # Advanced
            "advanced/developer_mode": False,
            "advanced/check_updates": True,
            "advanced/send_analytics": False,
        }
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a setting value.
        
        Args:
            key: Setting key (e.g., "appearance/theme")
            default: Default value if setting doesn't exist
            
        Returns:
            Setting value or default
        """
        # Use provided default, or fall back to defaults dict
        if default is None:
            default = self._defaults.get(key)
            
        value = self.settings.value(key, default)
        
        # Handle boolean conversion (QSettings returns strings for booleans)
        if isinstance(default, bool):
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes')
            return bool(value)
            
        # Handle int conversion
        if isinstance(default, int):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
                
        # Handle float conversion
        if isinstance(default, float):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value.
        
        Args:
            key: Setting key (e.g., "appearance/theme")
            value: Value to set
        """
        self.settings.setValue(key, value)
        self.settings.sync()  # Ensure immediate write
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        self.settings.clear()
        for key, value in self._defaults.items():
            self.settings.setValue(key, value)
        self.settings.sync()
    
    def export_settings(self, filepath: str) -> None:
        """
        Export settings to a JSON file.
        
        Args:
            filepath: Path to export file
        """
        settings_dict = {}
        for key in self.settings.allKeys():
            settings_dict[key] = self.settings.value(key)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=2)
    
    def import_settings(self, filepath: str) -> None:
        """
        Import settings from a JSON file.
        
        Args:
            filepath: Path to import file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            settings_dict = json.load(f)
            
        for key, value in settings_dict.items():
            self.settings.setValue(key, value)
        self.settings.sync()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all current settings as a dictionary."""
        settings_dict = {}
        for key in self._defaults.keys():
            settings_dict[key] = self.get(key)
        return settings_dict
    
    def get_font_size_px(self) -> int:
        """Get font size in pixels based on current setting."""
        size_map = {
            "small": 9,
            "medium": 11,
            "large": 13,
            "xlarge": 15
        }
        return size_map.get(self.get("appearance/font_size"), 11)
