"""GUI for the anef_checker package."""

from __future__ import annotations

import os
from pathlib import Path

import flet as ft  # type: ignore[import-untyped]
from loguru import logger

from anef_checker.cli.cli import (
    check_status_core,
    setup_logging,
)
from anef_checker.constants.anef_enums import LanguageEnum
from anef_checker.controllers.anef_status_checker import BASE_URL
from anef_checker.gui.about import show_about


def check_status(e: ft.ControlEvent) -> None:  # type: ignore[no-any-unimported]
    """Check naturalization status using provided credentials."""
    e.page.update()
    username_field = e.page.controls[0].content.controls[2]
    password_field = e.page.controls[0].content.controls[4]
    url_field = e.page.controls[0].content.controls[6]
    language_dropdown = e.page.controls[0].content.controls[8]
    progress_bar = e.page.controls[0].content.controls[12]
    status_text = e.page.controls[0].content.controls[13]
    error_text = e.page.controls[0].content.controls[15]
    # Reset status displays
    status_text.value = ''
    error_text.visible = False
    progress_bar.visible = True
    e.page.update()

    try:
        logger.debug(
            f'username={username_field.value}, password={password_field.value},'
            f'url={url_field.value}, language={language_dropdown.value}',
        )
        result = check_status_core(
            username=username_field.value,
            password=password_field.value,
            url=url_field.value,
            language=LanguageEnum(language_dropdown.value),
        )
        if result.success:
            status_text.value = f'API Code:\n{result.api_code.name}\n\n' f'Description:\n{result.description}'  # type: ignore[union-attr]
        else:
            error_text.visible = True
            error_text.value = result.error_message
        progress_bar.visible = False
        e.page.update()
    except Exception as exception:  # noqa: BLE001
        error_text.visible = True
        error_text.value = f'An error occurred: {str(exception)}'
        progress_bar.visible = False
        e.page.update()


def start_app(page: ft.Page) -> None:  # type: ignore[no-any-unimported]
    """Run the main function for the GUI."""
    # Configure the page
    page.title = 'Naturalization Status Checker'
    page.window_width = 768
    page.window_height = 1024
    page.window_resizable = False
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # Add an AppBar with a top menu: Help > About.
    # Instead of a text child, we use an icon for the Help menu.
    page.appbar = ft.AppBar(
        title=ft.Text(''),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text='About', on_click=lambda e: show_about(e, page)),
                ],
                icon=ft.Icons.HELP,  # Use a help icon to represent the menu
            ),
        ],
    )

    # Create form controls
    username_field = ft.TextField(label='Username', value=os.getenv('ANEF_WEB_USERNAME', ''), width=400, text_size=16)
    password_field = ft.TextField(
        label='Password',
        value=os.getenv('ANEF_WEB_PASSWORD', ''),
        password=True,
        can_reveal_password=True,
        width=400,
        text_size=16,
    )
    url_field = ft.TextField(label='ANEF URL', value=os.getenv('ANEF_WEB_URL', BASE_URL), width=400, text_size=16)

    language_dropdown = ft.Dropdown(
        label='Result Language Description',
        width=400,
        options=[
            ft.dropdown.Option(key='fr', text='Français'),
            ft.dropdown.Option(key='en', text='English'),
            ft.dropdown.Option(key='es', text='Español'),
        ],
        value='fr',
    )

    check_button = ft.ElevatedButton(
        text='Check Status',
        width=300,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor={'hovered': ft.Colors.BLUE_700, '': ft.Colors.BLUE},
        ),
        on_click=check_status,
    )

    # Initialize controls as instance variables
    status_text = ft.Text(size=16, selectable=True, color=ft.Colors.PRIMARY, text_align=ft.TextAlign.CENTER)
    progress_bar = ft.ProgressBar(visible=False, width=400)
    error_text = ft.Text(color=ft.Colors.RED_400, size=14, visible=False, text_align=ft.TextAlign.CENTER)

    # Layout the page
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text('Naturalization Status Checker', size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    username_field,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    password_field,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    url_field,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    language_dropdown,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    check_button,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    progress_bar,
                    status_text,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    error_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            border_radius=5,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.BLACK12),
        ),
    )


def main() -> None:
    """Launch the Flet application."""
    setup_logging()
    ft.app(target=start_app, assets_dir=Path(__file__).parent / 'assets')


if __name__ == '__main__':
    main()
