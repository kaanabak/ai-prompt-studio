# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `run.sh` launcher for macOS and Linux (parity with `run.bat`).
- `Dockerfile` and `.dockerignore` for running PromptForge in a container.
- Edit prompt feature (`/prompts/<id>/edit`).
- Import a JSON backup to merge prompts back into the library (`/import`).
- "Favorites only" filter in the library view.
- User feedback via flash messages (save/update/delete/import confirmations).
- `PROMPTFORGE_HOST`, `PROMPTFORGE_PORT`, `PROMPTFORGE_DATA_DIR`,
  `PROMPTFORGE_DEBUG`, and `PROMPTFORGE_SECRET_KEY` environment variables.
- Test suite (`tests/test_app.py`, 18 tests) and CI workflow.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, GitHub issue/PR templates.

### Changed

- `prompts()` now filters out malformed entries instead of raising a
  `KeyError` in the middle of a request.
- `favorite()` redirects back to the referring page instead of always to
  the library.

### Fixed

- Missing `LICENSE` file (README badge referenced MIT but none was present).

## [0.1.0] - initial release

- Generate, save, tag, search, favorite, delete, and export prompts.
- Windows one-click launcher (`run.bat`).
