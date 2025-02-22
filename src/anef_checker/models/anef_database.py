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

from pydantic import (
    BaseModel,
    field_validator,
)

from anef_checker.constants.anef_enums import (
    APICodeEnum,
    LanguageEnum,
    ServiceEnum,
    StageEnum,
)


class CommentEntry(BaseModel):
    """Represents a comment entry with a language and description."""

    language: LanguageEnum
    comment: str


class StatusEntry(BaseModel):
    """Represents a status entry in the ANEF tracking system."""

    index: Optional[str] = None
    stage: StageEnum
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
                raise ValueError(f'Invalid API code: {value}') from None  # Raise an error if no match found
        return value


class StatusDatabase(BaseModel):
    """Database model containing all possible status entries."""

    statuses: List[StatusEntry]
