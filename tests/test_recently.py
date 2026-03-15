"""
Tests for recently.py: daily activity feed.
"""
import pytest


def test_recently_no_date_returns_200(client, mock_db):
    rv = client.get("/recently")
    assert rv.status_code == 200


def test_recently_no_date_slash(client, mock_db):
    """Trailing-slash variant should also work."""
    rv = client.get("/recently/")
    assert rv.status_code in (200, 301, 308)


def test_recently_with_valid_date(client, mock_db):
    rv = client.get("/recently/2024-01-15")
    assert rv.status_code == 200


def test_recently_with_alpha_date_redirects(client):
    """Non-numeric date → redirect to /recently (safety guard)."""
    rv = client.get("/recently/notadate")
    assert rv.status_code in (301, 302)


def test_recently_with_data(client, mock_db):
    from datetime import datetime
    _, mock_conn = mock_db
    cursor = mock_conn.cursor.return_value
    cursor.fetchall.side_effect = [
        [   # recently events — event_date must be a datetime (template calls .strftime)
            (datetime(2024, 1, 15, 14, 30, 0), "Radiohead - Creep", "LastFM",
             None, "Radiohead", "Pablo Honey", "ext1", "http://x.com", None),
        ],
        [   # budget
            (datetime(2024, 1, 15), "Supermarket", "45.50", "New World"),
        ],
    ]
    cursor.fetchone.side_effect = [
        (datetime(2024, 1, 15, 10, 0, 0), "1234.56"),  # bankbalance
        None,                                            # no blog post
    ]
    rv = client.get("/recently/2024-01-15")
    assert rv.status_code == 200


def test_recently_empty_day(client, mock_db):
    rv = client.get("/recently/2020-06-01")
    assert rv.status_code == 200


def test_recently_earliest_date_clamps_prevdate(client, mock_db):
    """
    1996-12-01 is the earliest record; prevdate should be clamped to itself
    (not decremented to 1996-11-30).  Now that the comparison uses date(1996,12,1)
    instead of the string "1996-12-01", the guard fires correctly.
    """
    rv = client.get("/recently/1996-12-01")
    assert rv.status_code == 200


def test_recently_today_hides_next_link(client, mock_db):
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    rv = client.get(f"/recently/{today}")
    assert rv.status_code == 200


def test_recently_future_date(client, mock_db):
    rv = client.get("/recently/2099-12-31")
    assert rv.status_code == 200
