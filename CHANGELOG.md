# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-02-24

First official release

### Added

- **Command-line Interface (CLI)**: Allows users to check their naturalization status via terminal commands.
- **Graphical User Interface (GUI)**: A simple and interactive interface for checking the status.
- **Secure Credential Handling**: Uses environment variables to store login credentials securely.
- **Automated Dependency Management**: Uses `pyproject.toml` to manage dependencies, including Selenium, Pydantic, and Typer.
- **Testing and Linting**: Configured `pytest`, `tox`, `ruff`, `black`, and `mypy` for code quality and testing.
- **Continuous Integration (CI)**: Implemented GitHub Actions workflow for automated testing and linting.
- **Standalone Binary Build**: Supports packaging the tool using `pyinstaller`.
