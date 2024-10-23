from pathlib import Path
from typing import Any, Dict, Optional
import json


class Prefs:
    """
    A class to manage application preferences stored in a JSON file.

    Public methods:
        get(): Retrieve a preference value
        set(): Set a preference value
        update(): Update multiple preferences
        delete(): Remove a preference
        reset(): Reset to defaults
        data (property): Get a copy of all preferences

    Private methods (prefixed with _):
        _load_from_disk(): Internal file loading
        _save_to_disk(): Internal file saving
        _validate_key(): Key validation
    """

    def __init__(
            self,
            filepath: str,
            defaults: Dict[str, Any] = None,
            auto_save: bool = True
    ):
        """Initialize preferences manager."""
        self._filepath = Path(filepath)
        self._defaults = defaults or {}
        self._auto_save = auto_save
        self._data = self._defaults.copy()

        # Load existing preferences if any
        self._load_from_disk()


    def _validate_key(self, key: str) -> None:
        """
        Validate a preference key.

        Private method - internal use only.
        """
        if not isinstance(key, str):
            raise TypeError("Preference key must be a string")
        if not key:
            raise ValueError("Preference key cannot be empty")


    def _load_from_disk(self) -> None:
        """
        Load preferences from file.

        Private method - internal use only.
        """
        try:
            if self._filepath.exists():
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self._data.update(loaded_data)
        except json.JSONDecodeError as e:
            print(f"Error loading preferences: {e}")
        except Exception as e:
            print(f"Unexpected error loading preferences: {e}")


    def _save_to_disk(self) -> bool:
        """
        Save preferences to file.

        Private method - internal use only.
        """
        try:
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, sort_keys=True)
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False


    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a preference value.

        Public method - part of the stable API.
        """
        self._validate_key(key)
        return self._data.get(key, default or self._defaults.get(key))

    def set(self, key: str, value: Any) -> None:
        """
        Set a preference value.

        Public method - part of the stable API.
        """
        self._validate_key(key)
        self._data[key] = value
        if self._auto_save:
            self._save_to_disk()


    def update(self, values: Dict[str, Any]) -> None:
        """
        Update multiple preferences at once.

        Public method - part of the stable API.
        """
        for key in values:
            self._validate_key(key)
        self._data.update(values)
        if self._auto_save:
            self._save_to_disk()


    def delete(self, key: str) -> None:
        """
        Delete a preference.

        Public method - part of the stable API.
        """
        self._validate_key(key)
        if key in self._data:
            del self._data[key]
            if self._auto_save:
                self._save_to_disk()


    def reset(self) -> None:
        """
        Reset preferences to defaults.

        Public method - part of the stable API.
        """
        self._data = self._defaults.copy()
        if self._auto_save:
            self._save_to_disk()


    @property
    def data(self) -> Dict[str, Any]:
        """
        Get a copy of all preferences.

        This is a property decorator - it allows us to access this method
        like an attribute (prefs.data) instead of a method call (prefs.data()).
        The property decorator provides read-only access to the data,
        returning a copy to prevent direct modification of internal state.

        Example:
            prefs = Prefs("config.json")
            all_data = prefs.data  # Note: no parentheses needed
        """
        return self._data.copy()