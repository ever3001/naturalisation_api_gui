"""Data models for ANEF.

This module provides Pydantic models to define:
- Status entries and databases for request tracking.
- Web configuration settings for API interactions.

"""

from __future__ import annotations

from typing import (
    List,
    Optional,
    Type,
)

from loguru import logger
from pydantic import (
    BaseModel,
    field_validator,
)

from anef_checker.constants.anef_enums import (
    APICodeEnum,
    ServiceEnum,
)
from anef_checker.constants.common import (
    LanguageEnum,
)


class CommentEntry(BaseModel):
    """Represents a comment entry with a language and description."""

    language: LanguageEnum
    comment: str


class StatusEntry(BaseModel):
    """Represents a status entry in the ANEF tracking system."""

    index: Optional[str] = None
    stage: Optional[str] = None
    service: Optional[ServiceEnum] = None
    api_code: APICodeEnum
    comments: Optional[List[CommentEntry]] = None

    @field_validator('api_code', mode='before')
    @classmethod
    def normalize_api_code(cls: Type[StatusEntry], value: str | APICodeEnum) -> APICodeEnum:
        """Normalize the API code to an enum value."""
        if isinstance(value, str):
            try:
                return APICodeEnum[value.upper()]  # Convert to uppercase and match enum key
            except KeyError:
                logger.error(f'Invalid API code: {value}')
                return APICodeEnum.UNKNOWN
        return value


class StatusDatabase(BaseModel):
    """Database model containing all possible status entries."""

    statuses: List[StatusEntry]
