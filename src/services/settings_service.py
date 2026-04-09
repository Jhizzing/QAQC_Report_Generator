"""
Settings Service — platform-independent settings management.

Replaces the PyQt6-coupled SettingsManager with a plain JSON file backend.
Settings are stored at ~/.logiqore/settings.json.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsService:
    """Manages application settings via a JSON file. No Qt dependency."""

    DEFAULT_SETTINGS_DIR = Path.home() / ".logiqore"
    DEFAULT_SETTINGS_FILE = DEFAULT_SETTINGS_DIR / "settings.json"

    def __init__(self, settings_path: Optional[str] = None) -> None:
        self._path = Path(settings_path) if settings_path else self.DEFAULT_SETTINGS_FILE
        self._defaults = self._get_defaults()
        self._settings: Dict[str, Any] = {}
        self._load()

    def _get_defaults(self) -> Dict[str, Any]:
        return {
            # Data & Files
            "data.input_dir": str(Path.home() / "Documents"),
            "data.output_dir": str(Path.home() / "Documents" / "LogiQore_Output"),
            "data.recent_files_limit": 10,

            # Analysis Defaults
            "analysis.ldl": 0.03,
            "analysis.rpd_limit": 20.0,
            "analysis.warning_sd": 2.0,
            "analysis.fail_sd": 3.0,
            "analysis.crm_database": "crm_database.yaml",

            # Visualization
            "viz.default_dpi": 300,
            "viz.export_format": "png",

            # App
            "app.theme": "dark",
            "app.check_updates": True,
        }

    def _load(self) -> None:
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as f:
                self._settings = json.load(f)
        else:
            self._settings = {}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._settings, f, indent=2)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a setting. Falls back to built-in defaults, then to `default`."""
        if key in self._settings:
            return self._settings[key]
        if key in self._defaults:
            return self._defaults[key]
        return default

    def set(self, key: str, value: Any) -> None:
        """Set a setting and persist to disk."""
        self._settings[key] = value
        self._save()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._settings = {}
        self._save()

    def get_all(self) -> Dict[str, Any]:
        """Return merged defaults + user overrides."""
        merged = dict(self._defaults)
        merged.update(self._settings)
        return merged

    def export_settings(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.get_all(), f, indent=2)

    def import_settings(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            self._settings = json.load(f)
        self._save()
