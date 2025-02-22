"""Module for displaying the About dialog."""

from __future__ import annotations

import importlib.metadata

import flet as ft  # type: ignore[import-untyped]

APP_VERSION = importlib.metadata.version('anef_checker')


def get_about_content_markdown() -> ft.Markdown:  # type: ignore[no-any-unimported]
    """Generate Markdown content for the About dialog."""
    return ft.Markdown(
        f'''# ANEF Checker {APP_VERSION}

A simple Checker to see the naturalisation process
''',
    )


def show_about(e: ft.ControlEvent, page: ft.Page) -> None:  # type: ignore[no-any-unimported] # noqa: ARG001
    """Display the About dialog with version information."""

    def handle_close(e) -> None:  # type: ignore[no-untyped-def] # noqa: ARG001, ANN001
        """Close the given dialog by clearing the overlay."""
        page.close(about_dialog)

    about_dialog = ft.AlertDialog(
        title=ft.Text('About'),
        content=get_about_content_markdown(),
        actions=[
            ft.TextButton('OK', on_click=handle_close),
        ],
    )
    # Append the dialog to the overlay instead of using the deprecated page.dialog.
    page.overlay.append(about_dialog)
    about_dialog.open = True
    page.update()
