# Contributing

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

## Code of Conduct

Everyone participating in this project and in particular in our
issue tracker, pull requests, and chat, is expected to treat
other people with respect and more generally to follow the guidelines
articulated in the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

You can contribute in many ways:

## Report Bugs

Report bugs at [GitHub](https://github.com/ever3001/anef_checker/issues)

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

## Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

## Write Documentation

This PyPackage could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

## Getting started with development

Ready to contribute? Here\'s how to set up `anef_checker` for local development.
Please note this documentation assumes you already have `uv` and `git` installed and ready to go.

### Setup

#### (1) Fork the repository

Within GitHub, navigate to the [anef_checker](https://github.com/ever3001/anef_checker) repository and fork the repository.

#### (2) Clone the repository and enter into it

```bash
git clone git@github.com:<your_username>/anef_checker
cd anef_checker
```

#### (3) Install and activate the environment

```bash
uv sync --all-groups
```

#### (4) Install pre-commit to run linters/formatters at commit time

```bash
uv run pre-commit install
```

#### (5) Create a branch for local development

```bash
git checkout -b name-of-your-bugfix-or-feature
```

### Creating and Running tests

Don't forget to add test cases for your added functionality to the `tests` directory.

When you're done making changes, check that your changes pass the formatting tests.

```bash
uv run pre-commit run --all-files
```

Now, validate that all unit tests are passing:

```bash
uv run pytest
```

#### Using `tox`

You can also use [`tox`](https://tox.wiki/en/latest/) to run tests and other commands.
`tox` handles setting up test environments for you.

```bash
# Run tests
uv run tox run -e py

# Run tests using some specific Python version
uv run tox run -e py311

```

## Core developer guidelines

Core developers should follow these rules when processing pull requests:

- The pull request should include tests.
- Always wait for tests to pass before merging PRs.
- Use "[Squash and merge](https://github.com/blog/2141-squash-your-commits)"
  to merge PRs.
- Delete branches for merged PRs (by core devs pushing to the main repo).
- Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to commit.
