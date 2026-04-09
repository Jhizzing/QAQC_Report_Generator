"""
Settings Manager Module — backwards-compatible wrapper.

Delegates to SettingsService (JSON-based, no Qt dependency).
This module exists so that existing imports continue to work.
"""

from services.settings_service import SettingsService


class SettingsManager:
    """
    Manages application settings and preferences.

    Previously used PyQt6 QSettings. Now delegates to SettingsService
    which stores settings in ~/.logiqore/settings.json.
    """

    def __init__(self, organization: str = "LogiQore", application: str = "Reporter"):
        self._service = SettingsService()

    def get(self, key: str, default=None):
        # Convert old slash-style keys to dot-style
        return self._service.get(key.replace("/", "."), default)

    def set(self, key: str, value) -> None:
        self._service.set(key.replace("/", "."), value)

    def reset_to_defaults(self) -> None:
        self._service.reset_to_defaults()

    def export_settings(self, filepath: str) -> None:
        self._service.export_settings(filepath)

    def import_settings(self, filepath: str) -> None:
        self._service.import_settings(filepath)

    def get_all_settings(self):
        return self._service.get_all()
