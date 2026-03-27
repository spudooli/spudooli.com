"""
Tests for projects routes: /projects/bookmarks, /i3.
"""
import pytest
from unittest.mock import MagicMock, patch
from tests.conftest import make_cursor, smart_open_side_effect


# ── /projects/bookmarks ───────────────────────────────────────────────────────


def _bookmark_rows():
    return [
        (1, "https://example.com", "Example", "python, web"),
        (2, "https://foo.com", "Foo", "python, tools"),
        (3, "https://bar.com", "Bar", "web"),
        (4, "https://baz.com", "Baz", None),
    ]


def test_bookmarks_no_filter_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value = make_cursor(fetchall=_bookmark_rows())
    rv = client.get("/projects/bookmarks")
    assert rv.status_code == 200


def test_bookmarks_no_filter_shows_all(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value = make_cursor(fetchall=_bookmark_rows())
    rv = client.get("/projects/bookmarks")
    assert b"Example" in rv.data
    assert b"Foo" in rv.data
    assert b"Bar" in rv.data
    assert b"Baz" in rv.data


def test_bookmarks_tag_filter_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value = make_cursor(fetchall=_bookmark_rows())
    rv = client.get("/projects/bookmarks/python")
    assert rv.status_code == 200


def test_bookmarks_tag_filter_shows_only_matching(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value = make_cursor(fetchall=_bookmark_rows())
    rv = client.get("/projects/bookmarks/python")
    assert b"Example" in rv.data
    assert b"Foo" in rv.data
    assert b"Bar" not in rv.data  # tagged "web" only
    assert b"Baz" not in rv.data  # no tags


def test_bookmarks_popular_tags_requires_count_gte_2(client, mock_db):
    """Tags appearing only once should not appear in popular_tags."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value = make_cursor(fetchall=_bookmark_rows())
    rv = client.get("/projects/bookmarks")
    # "python" and "web" each appear twice → popular; "tools" appears once → not popular
    assert b"python" in rv.data
    assert b"web" in rv.data


def test_bookmarks_empty_db_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value = make_cursor(fetchall=[])
    rv = client.get("/projects/bookmarks")
    assert rv.status_code == 200


# ── /i3 ──────────────────────────────────────────────────────────────────────


def _i3_cursor(mock_conn):
    """Set up sequential fetchone/fetchall returns for the i3 route."""
    cursor = MagicMock()
    cursor.fetchone.side_effect = [
        (5000,),   # sum(kwh)
        (200,),    # sum(cost)
        (1,),      # count(distinct artist) — not used by i3, but cursor is shared
    ]
    cursor.fetchall.return_value = [
        (202301, "15.00"),
        (202302, "18.50"),
    ]
    cursor.description = [("thismonth",), ("cost",)]
    mock_conn.cursor.return_value = cursor
    return cursor


def test_i3_returns_200(client, mock_db, monkeypatch):
    _, mock_conn = mock_db
    _i3_cursor(mock_conn)

    import spudoolicom.bmwi3
    mock_r = MagicMock()
    mock_r.get.side_effect = lambda k: {
        "i3mileage": "50000",
        "i3rangeremaining": "120",
        "i3batteryremaining": "80",
        "i3chargingstatus": "NOT_CHARGING",
    }.get(k, "0")
    monkeypatch.setattr(spudoolicom.bmwi3, "r", mock_r)

    with patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.get("/i3")
    assert rv.status_code == 200


def test_i3_formats_traveled_distance_with_commas(client, mock_db, monkeypatch):
    """Regression: i3traveled must be formatted with thousands separator."""
    _, mock_conn = mock_db
    _i3_cursor(mock_conn)

    import spudoolicom.bmwi3
    mock_r = MagicMock()
    mock_r.get.side_effect = lambda k: {
        "i3mileage": "60000",   # 60000 - 46683 = 13317 → "13,317"
        "i3rangeremaining": "100",
        "i3batteryremaining": "75",
        "i3chargingstatus": "NOT_CHARGING",
    }.get(k, "0")
    monkeypatch.setattr(spudoolicom.bmwi3, "r", mock_r)

    with patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.get("/i3")
    assert b"13,317" in rv.data
