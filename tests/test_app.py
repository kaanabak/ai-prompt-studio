import importlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMPTFORGE_DATA_DIR", str(tmp_path))
    import app as app_module

    importlib.reload(app_module)
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as c:
        yield c, app_module


def _create(client, title="Test Prompt", body="Do the thing.", tags="a, b"):
    return client.post("/prompts", data={"title": title, "body": body, "tags": tags}, follow_redirects=True)


def test_home_page_loads(client):
    c, _ = client
    resp = c.get("/")
    assert resp.status_code == 200


def test_generator_builds_prompt(client):
    c, _ = client
    resp = c.post(
        "/generator",
        data={"topic": "writing emails", "audience": "sales reps", "tone": "friendly"},
    )
    assert resp.status_code == 200
    assert b"writing emails" in resp.data


def test_generator_requires_topic(client):
    c, _ = client
    resp = c.post("/generator", data={"topic": "", "audience": "x", "tone": "y"})
    assert resp.status_code == 200


def test_create_and_list_prompt(client):
    c, mod = client
    _create(c)
    items = mod.prompts()
    assert len(items) == 1
    assert items[0]["title"] == "Test Prompt"
    assert items[0]["tags"] == ["a", "b"]

    resp = c.get("/prompts")
    assert b"Test Prompt" in resp.data


def test_create_requires_title_and_body(client):
    c, mod = client
    _create(c, title="", body="")
    assert mod.prompts() == []


def test_search_filters_by_query(client):
    c, mod = client
    _create(c, title="Email helper", body="Draft emails")
    _create(c, title="Blog helper", body="Draft blog posts")
    resp = c.get("/prompts?q=email")
    assert b"Email helper" in resp.data
    assert b"Blog helper" not in resp.data


def test_filter_by_tag(client):
    c, mod = client
    _create(c, title="Marketing prompt", tags="marketing")
    _create(c, title="Code prompt", tags="dev")
    resp = c.get("/prompts?tag=marketing")
    assert b"Marketing prompt" in resp.data
    assert b"Code prompt" not in resp.data


def test_favorite_toggle(client):
    c, mod = client
    _create(c)
    pid = mod.prompts()[0]["id"]
    c.post(f"/prompts/{pid}/favorite")
    assert mod.prompts()[0]["favorite"] is True
    c.post(f"/prompts/{pid}/favorite")
    assert mod.prompts()[0]["favorite"] is False


def test_favorite_missing_prompt_404(client):
    c, _ = client
    resp = c.post("/prompts/does-not-exist/favorite")
    assert resp.status_code == 404


def test_edit_prompt(client):
    c, mod = client
    _create(c, title="Original", body="Original body")
    pid = mod.prompts()[0]["id"]

    resp = c.get(f"/prompts/{pid}/edit")
    assert resp.status_code == 200
    assert b"Original" in resp.data

    c.post(f"/prompts/{pid}/edit", data={"title": "Updated", "body": "Updated body", "tags": "x"})
    items = mod.prompts()
    assert items[0]["title"] == "Updated"
    assert items[0]["body"] == "Updated body"


def test_edit_missing_prompt_404(client):
    c, _ = client
    assert c.get("/prompts/nope/edit").status_code == 404


def test_delete_prompt(client):
    c, mod = client
    _create(c)
    pid = mod.prompts()[0]["id"]
    c.post(f"/prompts/{pid}/delete")
    assert mod.prompts() == []


def test_delete_missing_prompt_404(client):
    c, _ = client
    assert c.post("/prompts/nope/delete").status_code == 404


def test_export_returns_json(client):
    c, mod = client
    _create(c)
    resp = c.get("/export")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert len(data) == 1


def test_import_merges_backup(client, tmp_path):
    c, mod = client
    backup = [
        {"id": "abc123", "title": "Imported prompt", "body": "Imported body", "tags": ["x"], "favorite": True}
    ]
    backup_file = tmp_path / "backup.json"
    backup_file.write_text(json.dumps(backup), encoding="utf-8")

    with open(backup_file, "rb") as fh:
        resp = c.post(
            "/import",
            data={"backup": (fh, "backup.json")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
    assert resp.status_code == 200
    items = mod.prompts()
    assert len(items) == 1
    assert items[0]["title"] == "Imported prompt"


def test_import_rejects_invalid_json(client, tmp_path):
    c, mod = client
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not json", encoding="utf-8")
    with open(bad_file, "rb") as fh:
        c.post(
            "/import",
            data={"backup": (fh, "bad.json")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
    assert mod.prompts() == []


def test_health_endpoint(client):
    c, _ = client
    resp = c.get("/health")
    assert resp.get_json() == {"status": "online", "app": "PromptForge"}


def test_prompt_list_survives_corrupt_data_file(client):
    c, mod = client
    mod.DATA.parent.mkdir(parents=True, exist_ok=True)
    mod.DATA.write_text("{not valid json", encoding="utf-8")
    resp = c.get("/prompts")
    assert resp.status_code == 200
