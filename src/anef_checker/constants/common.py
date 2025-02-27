"""Common constants shared between modules."""

from __future__ import annotations

from enum import Enum


class LanguageEnum(str, Enum):
    """List of supported languages."""

    EN = 'en'
    FR = 'fr'
    ES = 'es'
