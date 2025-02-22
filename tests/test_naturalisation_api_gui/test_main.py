"""Test for main entry point for the anef_checker package."""

from __future__ import annotations

from anef_checker.constants.anef_enums import LanguageEnum


def test_dummy():
    assert LanguageEnum.FR.value == 'fr'
