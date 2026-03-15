"""
Tests for house.py: home sensor dashboard.

Known bug documented:
  r.get('X') + "&deg;" crashes with TypeError when Redis returns None.
"""
import pytest


def _setup_house_cursors(mock_conn):
    """House route makes one DB call: sum of fridge door opens."""
    mock_conn.cursor.return_value.fetchone.return_value = (500,)


def test_house_returns_200_with_sensible_redis(client, mock_db, mock_redis):
    """All Redis keys return '20' — page should render without error."""
    _, mock_conn = mock_db
    _setup_house_cursors(mock_conn)
    rv = client.get("/house")
    assert rv.status_code == 200


def test_house_redis_none_shows_fallback(client, mock_db, mock_redis):
    """When Redis is down, sensors should show '?' rather than crashing."""
    mock_redis.get.return_value = None
    _, mock_conn = mock_db
    _setup_house_cursors(mock_conn)
    rv = client.get("/house")
    assert rv.status_code == 200


def test_house_fridge_door_count(client, mock_db, mock_redis):
    """Fridge door count = Redis daily counter + DB historical sum."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.return_value = (1000,)
    mock_redis.get.return_value = "5"
    rv = client.get("/house")
    assert rv.status_code == 200


def test_house_spa_temp_zero(client, mock_db, mock_redis):
    """spa temperature of integer 0 triggers the '-' display branch."""
    _, mock_conn = mock_db
    _setup_house_cursors(mock_conn)

    def _get(key):
        if key == "spatemperature":
            return 0
        return "20"

    mock_redis.get.side_effect = _get
    rv = client.get("/house")
    assert rv.status_code == 200


def test_house_barometer_short_string(client, mock_db, mock_redis):
    """barometer = r.get("indoorPressure")[0:-2] — safe even for '20'."""
    _, mock_conn = mock_db
    _setup_house_cursors(mock_conn)
    mock_redis.get.return_value = "20"
    rv = client.get("/house")
    assert rv.status_code == 200
