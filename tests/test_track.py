"""
Tests for track.py: OwnTracks-compatible GPS location endpoint.
"""
import pytest
import requests as _requests
from unittest.mock import MagicMock, patch


_LOCATION_PAYLOAD = {
    "_type": "location",
    "lat": -36.86,
    "lon": 174.76,
    "alt": 10,
}

_LOCATION_NO_ALT = {
    "_type": "location",
    "lat": -36.86,
    "lon": 174.76,
    "alt": None,
}


def _mock_track_externals():
    paho_patch = patch("spudoolicom.track.paho.Client")
    req_patch = patch(
        "spudoolicom.track.requests.get",
        side_effect=_requests.exceptions.RequestException("no tile server"),
    )
    return paho_patch, req_patch


# ── GET /track/<who> ──────────────────────────────────────────────────────────


def test_track_get_returns_200(client):
    rv = client.get("/track/dave")
    assert rv.status_code == 200
    assert b"it works" in rv.data


# ── POST /track/<who> ─────────────────────────────────────────────────────────


def test_track_post_dave_publishes_mqtt(client, mock_db):
    paho_patch, req_patch = _mock_track_externals()
    with paho_patch as mock_paho, req_patch:
        mock_mqtt = MagicMock()
        mock_paho.return_value = mock_mqtt
        rv = client.post("/track/dave", json=_LOCATION_PAYLOAD)

    assert rv.status_code == 200
    assert b"it works" in rv.data
    mock_mqtt.publish.assert_called_once_with(
        "house/location/dave", "-36.86:174.76"
    )


def test_track_post_dave_inserts_db(client, mock_db):
    _, mock_conn = mock_db
    paho_patch, req_patch = _mock_track_externals()
    with paho_patch as mock_paho, req_patch:
        mock_paho.return_value = MagicMock()
        client.post("/track/dave", json=_LOCATION_PAYLOAD)

    mock_conn.commit.assert_called_once()


def test_track_post_gabba(client, mock_db):
    paho_patch, req_patch = _mock_track_externals()
    with paho_patch as mock_paho, req_patch:
        mock_mqtt = MagicMock()
        mock_paho.return_value = mock_mqtt
        rv = client.post("/track/gabba", json=_LOCATION_PAYLOAD)

    assert rv.status_code == 200
    mock_mqtt.publish.assert_called_once_with(
        "house/location/gabba", "-36.86:174.76"
    )


def test_track_post_alice(client, mock_db):
    """alice does not download map tiles (only dave and gabba do)."""
    paho_patch, req_patch = _mock_track_externals()
    with paho_patch as mock_paho, req_patch:
        mock_mqtt = MagicMock()
        mock_paho.return_value = mock_mqtt
        rv = client.post("/track/alice", json=_LOCATION_PAYLOAD)

    assert rv.status_code == 200
    mock_mqtt.publish.assert_called_once_with(
        "house/location/alice", "-36.86:174.76"
    )


def test_track_post_null_alt(client, mock_db):
    """alt=None should default to 0 without crashing."""
    paho_patch, req_patch = _mock_track_externals()
    with paho_patch as mock_paho, req_patch:
        mock_paho.return_value = MagicMock()
        rv = client.post("/track/dave", json=_LOCATION_NO_ALT)

    assert rv.status_code == 200


def test_track_non_location_type(client):
    """Non-location _type payloads (e.g. 'lwt') should not crash."""
    rv = client.post("/track/dave", json={"_type": "lwt"})
    assert rv.status_code == 200
