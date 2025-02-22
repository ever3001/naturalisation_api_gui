"""Database controller module for managing status descriptions.

This module provides functionality to:
- Load status data from a JSON file.
- Retrieve the database file path.
- Fetch status descriptions in different languages.

Expected JSON structure:
{
    "statuses": [
        {
            "api_code": "STATUS_CODE",
            "comments": {
                "fr": "Description en français",
                "en": "Description in English",
                "es": "Descripción en español"
            }
        }
    ]
}
"""

from __future__ import annotations

import importlib.resources
import json
from pathlib import Path

from anef_checker.constants.anef_enums import (
    APICodeEnum,
    LanguageEnum,
)
from anef_checker.models.anef_database import (
    StatusDatabase,
    StatusEntry,
)


def load_status_database(file_path: Path) -> StatusDatabase:
    """Load the status database from a JSON file.

    Args:
    ----
        file_path (Path): Path to the JSON database file.

    Returns:
    -------
        StatusDatabase: Parsed database object containing statuses.

    Raises:
    ------
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    if not file_path.exists():
        raise FileNotFoundError(f'File {file_path} not found')

    with file_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    return StatusDatabase(**data)


def get_database_path() -> Path:
    """Retrieve the path to the packaged JSON database file."""
    try:
        # First try the development path using importlib.resources
        return Path(str(importlib.resources.files('anef_checker.database') / 'status_data.json'))
    except ModuleNotFoundError:
        import sys

        base_path = (
            Path(sys._MEIPASS)  # type: ignore[attr-defined] # noqa: SLF001
            if getattr(sys, 'frozen', False)
            else Path(__file__).parent
        )
        return base_path / 'database' / 'status_data.json'


def get_status_description(
    api_code: APICodeEnum,
    lang: LanguageEnum,
    status_db: StatusDatabase | None = None,
) -> str:
    """Fetch the description of a given status code in the requested language.

    Args:
    ----
        api_code (APICodeEnum): The status code to look up.
        lang (LanguageEnum): The language in which to retrieve the description.
        status_db (StatusDatabase, optional): Preloaded database instance. If None,
            loads from default file location.

    Returns:
    -------
        str: The description in the specified language or a fallback message if not found.
    """
    status_db = status_db or load_default_status_database()
    status = find_status(api_code, status_db)

    if status:
        comment = find_comment(status, lang)
        if comment:
            return comment

    return ''


def load_default_status_database() -> StatusDatabase:
    """Load the default status database."""
    return load_status_database(get_database_path())


def find_status(api_code: APICodeEnum, status_db: StatusDatabase) -> StatusEntry | None:
    """Find the status object for a given API code."""
    return next((s for s in status_db.statuses if s.api_code == api_code), None)


def find_comment(status: StatusEntry, lang: LanguageEnum) -> str | None:
    """Find the comment in the requested language for a given status."""
    if not status.comments:
        return None
    return next((c.comment for c in status.comments if c.language == lang), None)


def get_fallback_message(lang: LanguageEnum) -> str:
    """Return a fallback message if the status description is not found."""
    fallback_messages = {
        LanguageEnum.FR: 'Description non trouvé',
        LanguageEnum.ES: 'Descripción no encontrada',
    }
    return fallback_messages.get(lang, 'Description not found')
