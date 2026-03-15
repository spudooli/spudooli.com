"""
Tests for miscellaneous routes: webcam, weather, charts, alice/sarah pages.
"""
import pytest
from unittest.mock import MagicMock, patch
from tests.conftest import make_cursor


# ── /webcam ───────────────────────────────────────────────────────────────────


def test_webcam_index_redirects_to_kitchen(client):
    rv = client.get("/webcam")
    assert rv.status_code == 301
    assert "kitchen" in rv.headers["Location"]


def test_webcam_kitchen_returns_200(client):
    rv = client.get("/webcam/camera/kitchen")
    assert rv.status_code == 200


def test_webcam_mancave_returns_200(client):
    rv = client.get("/webcam/camera/mancave")
    assert rv.status_code == 200


def test_webcam_driveway_returns_200(client):
    rv = client.get("/webcam/camera/driveway")
    assert rv.status_code == 200


def test_webcam_unknown_camera_redirects(client):
    rv = client.get("/webcam/camera/garage")
    assert rv.status_code == 301
    assert "kitchen" in rv.headers["Location"]


# ── /weather ─────────────────────────────────────────────────────────────────


def test_weather_returns_200_with_known_forecast(client, mock_redis):
    """
    weather.py uses if/if (not if/elif) for icon selection.  Unrecognised
    words leave saturdayicon/sundayicon undefined → UnboundLocalError.
    Set known forecast words to avoid triggering that bug here.
    """
    known_values = {
        "indoorPressure":       "1020hPa",
        "saturdayForecastWord": "Fine",
        "sundayForecastWord":   "Partly cloudy",
        "pressureDirection":    "stable",
        "todayForecast":        "Fine day",
        "tomorrowForecast":     "Mostly cloudy",
        "todayMax":             "24",
        "todayMin":             "14",
        "tomorrowMax":          "21",
        "tomorrowMin":          "12",
    }
    mock_redis.get.side_effect = lambda k: known_values.get(k, "20")
    rv = client.get("/weather")
    assert rv.status_code == 200


def test_weather_unrecognised_forecast_word_uses_fallback(client, mock_redis):
    """Unrecognised forecast word (default mock returns '20') → empty icon string, no crash."""
    rv = client.get("/weather")
    assert rv.status_code == 200


# ── /house/charts/<where> ─────────────────────────────────────────────────────


def test_charts_indoor_returns_200(client):
    rv = client.get("/house/charts/indoor")
    assert rv.status_code == 200


def test_charts_outdoor_returns_200(client):
    rv = client.get("/house/charts/outdoor")
    assert rv.status_code == 200


# ── /alice and /alice-in-europe ───────────────────────────────────────────────


def test_alice_uk_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (1, "2024-01-01 12:00:00", None, -36.86, 174.76, None, None),
        (42,),  # ping count
    ]
    # Patch list_files_by_creation_date directly to avoid touching os.listdir/stat
    with patch("spudoolicom.alice.list_files_by_creation_date", return_value=[]):
        rv = client.get("/alice")
    assert rv.status_code == 200


def test_alice_europe_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (1, "2024-01-01 12:00:00", None, 48.85, 2.35, None, None),
        (10,),
    ]
    with patch("spudoolicom.alice.list_files_by_creation_date", return_value=[]):
        rv = client.get("/alice-in-europe")
    assert rv.status_code == 200
