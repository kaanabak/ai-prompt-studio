"""PromptForge — a local-first prompt manager.

A tiny Flask application with zero external services: everything is
stored in a single JSON file on disk. See README.md for setup and
CONTRIBUTING.md if you'd like to help improve it.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, flash, redirect, render_template, request, send_file, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("PROMPTFORGE_SECRET_KEY", "dev-only-not-secret")

DATA_DIR = Path(os.environ.get("PROMPTFORGE_DATA_DIR", app.root_path)) / "data"
DATA = DATA_DIR / "prompts.json"
MAX_PROMPTS = 500


def prompts() -> list[dict]:
    """Load all saved prompts, tolerating a missing or corrupt data file."""
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    # Defensive filtering: ignore malformed entries instead of crashing routes.
    return [item for item in data if isinstance(item, dict) and item.get("id") and item.get("title")]


def save(items: list[dict]) -> None:
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(items[:MAX_PROMPTS], ensure_ascii=False, indent=2), encoding="utf-8")


def find(items: list[dict], prompt_id: str) -> dict | None:
    return next((item for item in items if item["id"] == prompt_id), None)


def tags(value: str) -> list[str]:
    return list(dict.fromkeys(x.strip().lower()[:32] for x in value.split(",") if x.strip()))[:8]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


@app.get("/")
def home():
    items = prompts()
    return render_template("index.html", count=len(items), recent=items[:3])


@app.route("/generator", methods=["GET", "POST"])
def generator():
    result = ""
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()[:180]
        audience = request.form.get("audience", "a general audience").strip()[:100]
        tone = request.form.get("tone", "clear and helpful").strip()[:100]
        if topic:
            result = (
                f"Help {audience} with {topic} in a {tone} tone. "
                "First, briefly confirm the goal and assumptions. "
                "Then provide an actionable, step-by-step answer. "
                "If information is missing, ask no more than three clear questions. "
                "Never invent facts."
            )
    return render_template("generator.html", result=result)


@app.post("/prompts")
def create_prompt():
    title = request.form.get("title", "").strip()[:120]
    body = request.form.get("body", "").strip()[:8000]
    if title and body:
        items = prompts()
        items.insert(
            0,
            {
                "id": uuid4().hex,
                "title": title,
                "body": body,
                "tags": tags(request.form.get("tags", "")),
                "favorite": False,
                "created_at": now(),
                "updated_at": now(),
            },
        )
        save(items)
        flash("Prompt saved.", "success")
    else:
        flash("Title and prompt body are required.", "error")
    return redirect(url_for("library"))


@app.get("/prompts")
def library():
    query = request.args.get("q", "").casefold().strip()
    tag = request.args.get("tag", "").casefold().strip()
    only_favorites = request.args.get("favorites") == "1"
    items = prompts()
    if query:
        items = [x for x in items if query in x["title"].casefold() or query in x["body"].casefold()]
    if tag:
        items = [x for x in items if tag in x.get("tags", [])]
    if only_favorites:
        items = [x for x in items if x.get("favorite")]
    all_tags = sorted({t for item in prompts() for t in item.get("tags", [])})
    return render_template(
        "prompts.html",
        prompts=items,
        tags=all_tags,
        query=query,
        active_tag=tag,
        only_favorites=only_favorites,
    )


@app.get("/prompts/<prompt_id>/edit")
def edit_prompt(prompt_id: str):
    item = find(prompts(), prompt_id)
    if item is None:
        abort(404)
    return render_template("edit.html", prompt=item)


@app.post("/prompts/<prompt_id>/edit")
def update_prompt(prompt_id: str):
    items = prompts()
    item = find(items, prompt_id)
    if item is None:
        abort(404)
    title = request.form.get("title", "").strip()[:120]
    body = request.form.get("body", "").strip()[:8000]
    if not (title and body):
        flash("Title and prompt body are required.", "error")
        return redirect(url_for("edit_prompt", prompt_id=prompt_id))
    item["title"] = title
    item["body"] = body
    item["tags"] = tags(request.form.get("tags", ""))
    item["updated_at"] = now()
    save(items)
    flash("Prompt updated.", "success")
    return redirect(url_for("library"))


@app.post("/prompts/<prompt_id>/favorite")
def favorite(prompt_id: str):
    items = prompts()
    item = find(items, prompt_id)
    if item is None:
        abort(404)
    item["favorite"] = not item.get("favorite", False)
    save(items)
    return redirect(request.referrer or url_for("library"))


@app.post("/prompts/<prompt_id>/delete")
def delete(prompt_id: str):
    items = prompts()
    updated = [item for item in items if item["id"] != prompt_id]
    if len(updated) == len(items):
        abort(404)
    save(updated)
    flash("Prompt deleted.", "success")
    return redirect(url_for("library"))


@app.get("/export")
def export():
    if not DATA.exists():
        save([])
    return send_file(DATA, as_attachment=True, download_name="promptforge-backup.json")


@app.post("/import")
def import_backup():
    uploaded = request.files.get("backup")
    if uploaded is None or not uploaded.filename:
        flash("Choose a PromptForge JSON backup file first.", "error")
        return redirect(url_for("library"))
    try:
        incoming = json.loads(uploaded.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        flash("That file isn't valid PromptForge JSON.", "error")
        return redirect(url_for("library"))
    if not isinstance(incoming, list):
        flash("That file isn't valid PromptForge JSON.", "error")
        return redirect(url_for("library"))

    existing = prompts()
    existing_ids = {item["id"] for item in existing}
    added = 0
    for entry in incoming:
        if not isinstance(entry, dict) or not entry.get("title") or not entry.get("body"):
            continue
        entry_id = entry.get("id") or uuid4().hex
        if entry_id in existing_ids:
            continue
        existing.append(
            {
                "id": entry_id,
                "title": str(entry["title"])[:120],
                "body": str(entry["body"])[:8000],
                "tags": entry.get("tags", [])[:8] if isinstance(entry.get("tags"), list) else [],
                "favorite": bool(entry.get("favorite", False)),
                "created_at": entry.get("created_at") or now(),
                "updated_at": entry.get("updated_at") or now(),
            }
        )
        existing_ids.add(entry_id)
        added += 1
    save(existing)
    flash(f"Imported {added} prompt(s).", "success")
    return redirect(url_for("library"))


@app.get("/health")
def health():
    return {"status": "online", "app": "PromptForge"}


def main() -> None:
    """Entry point used by `promptforge` console script and `python app.py`."""
    host = os.environ.get("PROMPTFORGE_HOST", "127.0.0.1")
    port = int(os.environ.get("PROMPTFORGE_PORT", "5000"))
    debug = os.environ.get("PROMPTFORGE_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
