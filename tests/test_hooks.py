"""
Tests for hook.py: MQTT webhooks (lights, TV, amp) and GitHub webhook.

MQTT clients are instantiated inside route handlers, so they are patched
per-test via `patch('spudoolicom.hook.paho.Client')`.
"""
import pytest
from unittest.mock import MagicMock, patch


def _paho_mock():
    """Return (mock_class, mock_client_instance) for paho patching."""
    mock_client = MagicMock()
    mock_class = MagicMock(return_value=mock_client)
    return mock_class, mock_client


# ── /hook (smoke test) ────────────────────────────────────────────────────────


def test_hook_root_returns_200(client):
    rv = client.post("/hook")
    assert rv.status_code == 200


# ── /hook/lights ──────────────────────────────────────────────────────────────


def test_lights_livingroom_on(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post(
            "/hook/lights", json={"device": "livingroomlights", "state": "on"}
        )
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/lights/livingroom", "on")


def test_lights_livingroom_off(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post(
            "/hook/lights", json={"device": "livingroomlights", "state": "off"}
        )
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/lights/livingroom", "off")


def test_lights_alllights_on(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post(
            "/hook/lights", json={"device": "alllights", "state": "on"}
        )
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/lights/all", "on")


def test_lights_outside_off(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post(
            "/hook/lights", json={"device": "outside", "state": "off"}
        )
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/lights/outside", "off")


def test_lights_kitchen_on(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post(
            "/hook/lights", json={"device": "kitchenlights", "state": "on"}
        )
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/lights/kitchen", "on")


# ── /hook/tv ──────────────────────────────────────────────────────────────────


def test_tv_on(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post("/hook/tv", json={"device": "tv", "state": "on"})
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/av/tv", "on")


def test_tv_off(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post("/hook/tv", json={"device": "tv", "state": "off"})
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/av/tv", "off")


# ── /hook/amp ─────────────────────────────────────────────────────────────────


def test_amp_on(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post("/hook/amp", json={"device": "amp", "state": "on"})
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/av/amp", "on")


def test_amp_zone2_on(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post("/hook/amp", json={"device": "zone2", "state": "on"})
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/av/zone2", "on")


def test_amp_zone3_off(client):
    mock_class, mock_client = _paho_mock()
    with patch("spudoolicom.hook.paho.Client", mock_class):
        rv = client.post("/hook/amp", json={"device": "zone3", "state": "off"})
    assert rv.status_code == 200
    mock_client.publish.assert_called_once_with("house/av/zone3", "off")


# ── /hook/github ──────────────────────────────────────────────────────────────


def test_github_ping(client):
    rv = client.post(
        "/hook/github",
        json={},
        headers={"X-GitHub-Event": "ping"},
    )
    assert rv.status_code == 200
    # hook.py returns json.dumps(...) as a plain string — force JSON parse
    import json
    data = json.loads(rv.data)
    assert data["msg"] == "Hi!"


def test_github_wrong_event_type(client):
    rv = client.post(
        "/hook/github",
        json={},
        headers={"X-GitHub-Event": "pull_request"},
    )
    assert rv.status_code == 200
    import json
    data = json.loads(rv.data)
    assert "wrong event type" in data["msg"]


def test_github_push_inserts_into_db(client, mock_db):
    _, mock_conn = mock_db
    payload = {
        "repository": {"name": "myrepo"},
        "head_commit": {
            "message": "Fix nasty bug",
            "url": "https://github.com/dave/myrepo/commit/abc123",
            "id": "abc123deadbeef",
        },
    }
    rv = client.post(
        "/hook/github",
        json=payload,
        headers={"X-GitHub-Event": "push"},
    )
    assert rv.status_code == 200
    assert b"OK" in rv.data
    mock_conn.commit.assert_called_once()
