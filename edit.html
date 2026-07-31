# PromptForge

> A local-first prompt manager for ChatGPT, Claude, Gemini, and any AI workflow.

[![CI](https://github.com/kaanabak/ai-prompt-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/kaanabak/ai-prompt-studio/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blueviolet)](CONTRIBUTING.md)

Create reusable prompts, organize them with tags, quickly find what you
need, and keep your data on your own computer. No account, no API key, no
cloud database — everything lives in one JSON file you control.

## Quick start

**Requires Python 3.9+.**

### macOS / Linux

```bash
git clone https://github.com/kaanabak/ai-prompt-studio.git
cd ai-prompt-studio
./run.sh
```

### Windows

Download or clone the repo, then double-click `run.bat` (or run it from a
terminal). It creates a virtual environment, installs Flask, starts
PromptForge in the background, and opens it in your browser.

### Docker (any OS)

```bash
docker build -t promptforge .
docker run --rm -p 5000:5000 -v promptforge-data:/app/data promptforge
```

Then open <http://127.0.0.1:5000>. Your prompts persist in the
`promptforge-data` volume between runs.

### Manual setup (any OS)

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Features

- Generate prompts from a topic, audience, and tone
- Save, tag, search, and favorite prompts
- Edit prompts after saving
- One-click copy to clipboard
- Download a local JSON backup, and re-import it later (or on another machine)
- No account, API key, or cloud database required — your data never leaves your computer

## Configuration

PromptForge reads a few optional environment variables:

| Variable                  | Default          | Purpose                                  |
| -------------------------- | ---------------- | ----------------------------------------- |
| `PROMPTFORGE_HOST`         | `127.0.0.1`       | Interface to bind to                      |
| `PROMPTFORGE_PORT`         | `5000`            | Port to listen on                         |
| `PROMPTFORGE_DATA_DIR`     | app directory     | Where `prompts.json` is stored            |
| `PROMPTFORGE_DEBUG`        | off               | Enable Flask debug mode (`1`/`true`)      |
| `PROMPTFORGE_SECRET_KEY`   | dev key           | Session signing key (set this in Docker/production-like deployments) |

## Project layout

```
app.py              Flask app and routes
templates/           Jinja2 templates
static/style.css     Styling
tests/test_app.py    Test suite (pytest)
run.sh / run.bat      One-click launchers for macOS/Linux and Windows
Dockerfile            Container build
```

## Development

```bash
pip install -r requirements-dev.txt
pytest          # run the test suite
ruff check .     # lint
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, and
[CHANGELOG.md](CHANGELOG.md) for release history.

## Security

PromptForge binds to `127.0.0.1` by default and is meant to run locally on
your own machine. It has no authentication — if you expose it beyond
localhost (e.g. via Docker with a public port, or by setting
`PROMPTFORGE_HOST=0.0.0.0`), put it behind your own authentication and set a
real `PROMPTFORGE_SECRET_KEY`. Please report security issues privately by
opening a GitHub security advisory rather than a public issue.

## License

[MIT](LICENSE) — free to use, modify, and distribute.

## Contributing

Issues and pull requests are welcome! Please read
[CONTRIBUTING.md](CONTRIBUTING.md) and our
[Code of Conduct](CODE_OF_CONDUCT.md) first.
