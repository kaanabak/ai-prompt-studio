# Contributing to PromptForge

Thanks for taking the time to contribute! PromptForge is intentionally
small — a single-file Flask app with no database and no external
services — and contributions that keep that spirit are especially
welcome.

## Getting set up

```bash
git clone https://github.com/kaanabak/ai-prompt-studio.git
cd ai-prompt-studio
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python app.py                  # http://127.0.0.1:5000
```

Or just run `./run.sh` (macOS/Linux) or `run.bat` (Windows) — both set up
the virtual environment for you automatically.

## Running tests and linting

```bash
pytest
ruff check .
```

Please add or update tests for any behavior change in `app.py`.

## Making a change

1. Fork the repo and create a branch from `main`.
2. Make your change, keeping it focused — small, reviewable PRs merge faster.
3. Run `pytest` and `ruff check .` and make sure both pass.
4. Update `README.md` if you changed user-facing behavior, and add an entry
   to `CHANGELOG.md`.
5. Open a pull request describing the change and, for UI changes, include a
   screenshot or short clip if you can.

## Reporting bugs / requesting features

Please use the issue templates under **Issues → New issue**. Include your
OS, Python version, and steps to reproduce for bugs.

## Code style

- Python 3.9+ compatible, type-hinted where practical.
- Keep the app dependency-free beyond Flask if at all possible — that's a
  core project goal, not an oversight.
- Templates are intentionally compact (minimal whitespace); please match the
  existing style rather than reformatting unrelated lines in your diff.

## Code of Conduct

By participating in this project you agree to abide by the
[Code of Conduct](CODE_OF_CONDUCT.md).
