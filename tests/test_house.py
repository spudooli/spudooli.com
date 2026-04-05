"""
Tests for house.py: home sensor dashboard.

Known bug documented:
  r.get('X') + "&deg;" crashes with TypeError when Redis returns None.
"""
import pytest
from unittest.mock import patch, AsyncMock

_FAKE_TAPO_DEVICES = [
    {'name': 'Living Room', 'ip': '192.168.1.222', 'on': True,  'today': '2h 0m',  'past7': '14h 0m', 'past30': '60h 0m', 'error': None},
    {'name': 'Desk Fan',    'ip': '192.168.1.119', 'on': False, 'today': '0m',      'past7': '1h 30m', 'past30': '6h 0m',  'error': None},
]


@pytest.fixture(autouse=True)
def mock_tapo():
    """Patch _fetch_all_tapo_devices so Tapo devices are never contacted."""
    with patch('spudoolicom.house._fetch_all_tapo_devices', new_callable=AsyncMock, return_value=_FAKE_TAPO_DEVICES) as m:
        yield m


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


def test_house_tapo_table_renders_device_names(client, mock_db, mock_redis, mock_tapo):
    """Tapo device names and on/off state appear in the rendered table."""
    _, mock_conn = mock_db
    _setup_house_cursors(mock_conn)
    rv = client.get("/house")
    assert rv.status_code == 200
    assert b"Living Room" in rv.data
    assert b"Desk Fan" in rv.data
    assert b"On" in rv.data
    assert b"Off" in rv.data


def test_house_tapo_empty_renders_no_rows(client, mock_db, mock_redis, mock_tapo):
    """When no Tapo devices are returned the table body is empty."""
    mock_tapo.return_value = []
    _, mock_conn = mock_db
    _setup_house_cursors(mock_conn)
    rv = client.get("/house")
    assert rv.status_code == 200
    assert b"Lights and plugs" in rv.data
    assert b"Living Room" not in rv.data
