"""Command-line interface for checking naturalization status with separated business logic."""

from __future__ import annotations

import os
import sys
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

import typer
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel
from typing_extensions import Annotated

from anef_checker.constants.anef_enums import (
    APICodeEnum,
    LanguageEnum,
)
from anef_checker.controllers.anef_status_checker import (
    BASE_URL,
    ANEFCredentials,
    check_naturalization_status,
)
from anef_checker.controllers.database import get_status_description

load_dotenv()

app = typer.Typer(help='CLI tool for checking naturalization status.')


class StatusCheckResult(BaseModel):
    """Pydantic class to hold the status check result."""

    success: bool
    api_code: Optional[APICodeEnum] = None
    description: Optional[str] = None
    error_message: Optional[str] = None


def setup_logging() -> None:
    """Set logging for the CLI."""
    logger.remove()
    logger.add(sys.stderr, level='INFO')


def setup_logging_verbose() -> None:
    """Set verbose logging for the CLI."""
    logger.remove()
    logger.add(sys.stderr, level='DEBUG')


def validate_credentials(
    username: Optional[str],
    password: Optional[str],
    url: Optional[str],
) -> Tuple[bool, Optional[ANEFCredentials], Optional[str]]:
    """Validate the provided credentials.

    Returns
    -------
        Tuple containing:
        - Boolean indicating if validation was successful
        - ANEFCredentials object if validation successful, None otherwise
        - Error message if validation failed, None otherwise
    """
    if not username or not password:
        return False, None, 'Username and password must be provided.'

    return True, ANEFCredentials(username=username, password=password, base_url=url or BASE_URL), None


def process_status_result(result: Dict[str, Any], language: LanguageEnum) -> StatusCheckResult:
    """Process the raw status check result and return a structured response."""
    if not result or not result.get('statut'):
        return StatusCheckResult(success=False, error_message='Status not found in response.')

    try:
        api_code = APICodeEnum[result['statut']]
        status_description = get_status_description(api_code=api_code, lang=language)
        if not status_description:
            status_description = api_code.value

        return StatusCheckResult(success=True, api_code=api_code, description=status_description)
    except ValueError:
        return StatusCheckResult(success=False, error_message=f"Unknown status code: {result.get('statut')}")


def check_status_core(
    username: Optional[str],
    password: Optional[str],
    url: Optional[str],
    language: LanguageEnum = LanguageEnum.FR,
) -> StatusCheckResult:
    """Check naturalization status using provided credentials.

    Core function to check naturalization status.
    Can be used by both CLI and GUI interfaces.
    """
    # Validate credentials
    is_valid, credentials, error = validate_credentials(username, password, url)
    if not is_valid:
        return StatusCheckResult(success=False, error_message=error)
    if not credentials:
        return StatusCheckResult(success=False, error_message='Missing required credentials.')

    # Check status
    try:
        result = check_naturalization_status(credentials)
        if not result:
            return StatusCheckResult(success=False, error_message='No response received from server.')
    except RuntimeError as e:
        return StatusCheckResult(success=False, error_message=f'Error checking status: {str(e)}')

    # Process result
    return process_status_result(result, language)


@app.command('check')
def check_status(
    username: Annotated[Optional[str], typer.Option('-n', '--username', help='ANEF web username.')] = os.getenv(
        'ANEF_WEB_USERNAME',
    ),
    password: Annotated[
        Optional[str],
        typer.Option('-p', '--password', help='ANEF web password.', hide_input=True),
    ] = os.getenv(
        'ANEF_WEB_PASSWORD',
    ),
    url: Annotated[Optional[str], typer.Option('-u', '--url', help='ANEF web URL.')] = os.getenv(
        'ANEF_WEB_URL',
        BASE_URL,
    ),
    language: Annotated[
        LanguageEnum,
        typer.Option('-l', '--language', help='Language for status description.'),
    ] = LanguageEnum.FR,
    verbose: Annotated[bool, typer.Option('-v', '--verbose', help='Enable verbose logging.')] = False,  # noqa: FBT002
) -> None:
    """Check naturalization status using provided credentials."""
    if verbose:
        setup_logging_verbose()
    else:
        setup_logging()
    logger.info(f'Checking naturalization status for {username}...')

    result = check_status_core(username, password, url, language)

    if not result.success:
        logger.error(result.error_message)
        raise typer.Exit(code=1)

    if result.api_code:
        logger.success(f'   API code: {result.api_code.name}')
    if result.description:
        logger.success(f'Description: {result.description}')


if __name__ == '__main__':
    app()
