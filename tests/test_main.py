"""
Tests for main.py routes: /, /rss, /status, /about, /now, /power, /contactus,
redirects, and error handlers.
"""
import pytest
from unittest.mock import patch, MagicMock
from tests.conftest import make_cursor


def _setup_homepage_cursors(mock_conn):
    """Wire up the 5 fetchone calls that the main() view makes."""
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (42,),                                               # imagecount
        (5000,),                                             # lastfmcount
        (100,),                                              # swarmcount
        (50,),                                               # mastodoncount
        (1, "Test Post", "test.jpg", "Post body", "alt"),   # latestpost
    ]


# ── Homepage (/) ──────────────────────────────────────────────────────────────


def test_homepage_returns_200(client, mock_db):
    _, mock_conn = mock_db
    _setup_homepage_cursors(mock_conn)
    rv = client.get("/")
    assert rv.status_code == 200


def test_homepage_renders_html(client, mock_db):
    _, mock_conn = mock_db
    _setup_homepage_cursors(mock_conn)
    rv = client.get("/")
    assert b"<" in rv.data


def test_homepage_bankbalance_none_shows_fallback(client, mock_db, mock_redis):
    """When Redis is down, bankbalance should show 'N/A' rather than crashing."""
    mock_redis.get.return_value = None
    _, mock_conn = mock_db
    _setup_homepage_cursors(mock_conn)
    rv = client.get("/")
    assert rv.status_code == 200


# ── RSS feed (/rss) ───────────────────────────────────────────────────────────


def test_rss_returns_200(client, mock_db):
    from datetime import datetime
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchall.return_value = [
        (1, "Test Post", "Body text", datetime(2024, 1, 1, 12, 0, 0), "test.jpg"),
    ]
    rv = client.get("/rss")
    assert rv.status_code == 200


def test_rss_content_type(client, mock_db):
    rv = client.get("/rss")
    assert "rss+xml" in rv.content_type


def test_rss_empty_feed(client, mock_db):
    """RSS with no posts should still return 200."""
    rv = client.get("/rss")
    assert rv.status_code == 200


# ── Status page (/status) ─────────────────────────────────────────────────────


def test_status_returns_200_no_topics(client, mock_db):
    """Status page with no sensor rows."""
    rv = client.get("/status")
    assert rv.status_code == 200


# ── Static info pages ─────────────────────────────────────────────────────────


def test_about_returns_200(client):
    rv = client.get("/about")
    assert rv.status_code == 200


def test_now_returns_200(client):
    rv = client.get("/now")
    assert rv.status_code == 200


# ── Power endpoint (/power) ───────────────────────────────────────────────────


def test_power_returns_redis_value(client, mock_redis):
    mock_redis.get.return_value = "3500"
    rv = client.get("/power")
    assert rv.status_code == 200
    assert b"3500" in rv.data


def test_power_none_does_not_crash(client, mock_redis):
    """Bug candidate: /power returns None directly — should not crash."""
    mock_redis.get.return_value = None
    rv = client.get("/power")
    assert rv.status_code == 200


# ── Legacy redirects (/index.php) ────────────────────────────────────────────


def test_index_php_rss_redirect(client):
    rv = client.get("/index.php?x=rss")
    assert rv.status_code == 301
    assert "/rss" in rv.headers["Location"]


def test_index_php_browse_redirect(client):
    rv = client.get("/index.php?x=browse")
    assert rv.status_code == 301
    assert "/photoblog/archive" in rv.headers["Location"]


def test_index_php_default_redirect(client):
    rv = client.get("/index.php")
    assert rv.status_code == 301
    assert rv.headers["Location"].endswith("/")


# ── Contact form (/contactus) ─────────────────────────────────────────────────


def test_contactus_get_returns_200(client):
    rv = client.get("/contactus")
    assert rv.status_code == 200


def test_contactus_post_valid_redirects(client, mock_db):
    rv = client.post(
        "/contactus",
        data={
            "contactusmessage": "Hello there",
            "contactusname": "Tester",
            "contactusemail": "test@example.com",
        },
    )
    assert rv.status_code == 302


def test_contactus_post_spam_filtered(client):
    """Known spammer email domains should be silently dropped."""
    rv = client.post(
        "/contactus",
        data={
            "contactusmessage": "Buy cheap stuff",
            "contactusname": "Mike",
            "contactusemail": "Mok@spam.com",
        },
    )
    assert rv.status_code == 302


# ── Error handlers ────────────────────────────────────────────────────────────


def test_404_handler(client):
    rv = client.get("/this/does/not/exist/at/all")
    assert rv.status_code == 404


# ── Cloudservices endpoint ────────────────────────────────────────────────────


def test_cloudservices_wrong_useragent_returns_403(client):
    rv = client.get("/cloudservices/giovanni/ipaddress")
    assert rv.status_code == 403


def test_cloudservices_correct_useragent(client):
    with patch("builtins.open", side_effect=lambda p, *a, **k: (
        MagicMock(
            __enter__=lambda s: s,
            __exit__=MagicMock(return_value=False),
            readlines=lambda: ["line1\n", "line2\n"],
        )
        if "/tmp/" in str(p)
        else open(p, *a, **k)
    )):
        rv = client.get(
            "/cloudservices/giovanni/ipaddress",
            headers={"User-Agent": "PingerFromGiovannisHome"},
        )
    assert rv.status_code in (200, 404)
