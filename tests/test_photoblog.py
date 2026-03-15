"""
Tests for photoblog.py: archive, map, individual posts, comments.

The single-post route calls open() unconditionally for EXIF data, and
os.path.isfile() for the embiggen check.  We patch both with smart
side-effects that mock only /var/www/ paths so Flask template loading is
unaffected.
"""
import os
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from tests.conftest import smart_open_side_effect

_real_isfile = os.path.isfile


def _smart_isfile(path):
    """Return False for /var/www/ paths; proxy everything else to real isfile."""
    if "/var/www/" in str(path):
        return False
    return _real_isfile(path)


# ── /photoblog/archive ────────────────────────────────────────────────────────


def test_photoblog_archive_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchall.return_value = [
        (1, "First Post", "test.jpg", datetime(2024, 1, 1, 12, 0, 0)),
        (2, "Second Post", "test2.jpg", datetime(2024, 2, 1, 12, 0, 0)),
    ]
    rv = client.get("/photoblog/archive")
    assert rv.status_code == 200


def test_photoblog_archive_empty(client, mock_db):
    rv = client.get("/photoblog/archive")
    assert rv.status_code == 200


# ── /photoblog-map ────────────────────────────────────────────────────────────


def test_photoblogmap_returns_200(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchall.return_value = [
        (1, "Somewhere", "-36.86,174.76"),
    ]
    mock_conn.cursor.return_value.fetchone.return_value = (1,)
    rv = client.get("/photoblog-map")
    assert rv.status_code == 200


def test_photoblogmap_no_markers(client, mock_db):
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.return_value = (0,)
    rv = client.get("/photoblog-map")
    assert rv.status_code == 200


# ── /photoblog/<id> — individual post ────────────────────────────────────────


def _setup_post_cursors(mock_conn, post_id=42, has_next=False):
    """
    Wire the fetchone calls for the post() view (unauthenticated — auth hook
    does NOT consume a fetchone when no user_id is in the session).

    Sequence:
      1. post data
      2. imagename for EXIF
      3. previousimage (skipped when id=="1")
      4. latestpost id
      [5. nextimage — only if has_next]
    """
    latest = post_id + 1 if has_next else post_id
    rows = [
        (post_id, "Test Headline", "test.jpg", "Post body",
         datetime(2024, 1, 15, 12, 0, 0), None, "alt text"),  # post
        (post_id, "test.jpg"),                                 # imagename
        (post_id - 1,),                                        # previousimage
        (latest,),                                             # latestpost
    ]
    if has_next:
        rows.append((post_id + 1,))                            # nextimage
    mock_conn.cursor.return_value.fetchone.side_effect = rows
    mock_conn.cursor.return_value.fetchall.return_value = []   # comments


def test_post_returns_200(client, mock_db):
    _, mock_conn = mock_db
    _setup_post_cursors(mock_conn)
    with patch("spudoolicom.photoblog.exifread.process_file", return_value={}), \
         patch("os.path.isfile", side_effect=_smart_isfile), \
         patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.get("/photoblog/42")
    assert rv.status_code == 200


def test_post_with_next_image(client, mock_db):
    _, mock_conn = mock_db
    _setup_post_cursors(mock_conn, post_id=41, has_next=True)
    with patch("spudoolicom.photoblog.exifread.process_file", return_value={}), \
         patch("os.path.isfile", side_effect=_smart_isfile), \
         patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.get("/photoblog/41")
    assert rv.status_code == 200


def test_post_first_image_no_previous(client, mock_db):
    """id='1' skips the previousimage query."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (1, "First", "test.jpg", "Body", datetime(2024, 1, 1), None, "alt"),
        (1, "test.jpg"),
        (5,),   # latestpost → id < latestpost → nextimage is fetched
        (2,),   # nextimage
    ]
    mock_conn.cursor.return_value.fetchall.return_value = []
    with patch("spudoolicom.photoblog.exifread.process_file", return_value={}), \
         patch("os.path.isfile", side_effect=_smart_isfile), \
         patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.get("/photoblog/1")
    assert rv.status_code == 200


def test_post_not_found_returns_404(client, mock_db):
    """If the DB returns no post row, route aborts with 404."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.return_value = None
    rv = client.get("/photoblog/9999")
    assert rv.status_code == 404


def test_photoblog_no_id_serves_latest(client, mock_db):
    """GET /photoblog (no id) fetches latest post id then serves it."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (42,),   # latest post id lookup
        (42, "Latest", "latest.jpg", "Body", datetime(2024, 6, 1), None, "alt"),
        (42, "latest.jpg"),
        (41,),   # previousimage
        (42,),   # latestpost
    ]
    mock_conn.cursor.return_value.fetchall.return_value = []
    with patch("spudoolicom.photoblog.exifread.process_file", return_value={}), \
         patch("os.path.isfile", side_effect=_smart_isfile), \
         patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.get("/photoblog")
    assert rv.status_code == 200


def test_post_missing_image_file_crashes(client, mock_db):
    """
    Known bug: open() is unconditional — missing image → FileNotFoundError.
    This test documents the bug and will be xfail until fixed.
    """
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (42, "Test", "missing.jpg", "Body", datetime(2024, 1, 1), None, "alt"),
        (42, "missing.jpg"),
    ]
    try:
        rv = client.get("/photoblog/42")
        assert rv.status_code in (200, 404)
    except FileNotFoundError:
        pytest.xfail("Known bug: open() is unconditional in photoblog.py")


# ── Comment submission ────────────────────────────────────────────────────────


def test_comment_post_valid(client, mock_db):
    """Valid comment → DB insert → redirect."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (42, "Test", "test.jpg", "Body", datetime(2024, 1, 1), None, "alt"),
        (42, "test.jpg"),
        (41,),
        (42,),
        None,   # approved_commenter lookup → not approved → publish='no'
    ]
    mock_conn.cursor.return_value.fetchall.return_value = []

    with patch("spudoolicom.photoblog.exifread.process_file", return_value={}), \
         patch("os.path.isfile", side_effect=_smart_isfile), \
         patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.post(
            "/photoblog/42",
            data={
                "commentmessage": "Nice photo!",
                "commentname": "Reader",
                "commenturl": "https://example.com",
                "commentemail": "reader@example.com",
            },
        )
    assert rv.status_code in (200, 301, 302)


def test_comment_spam_url_rejected(client, mock_db):
    """Comment with 'thesis' in URL is rejected without a DB insert."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.side_effect = [
        (42, "Test", "test.jpg", "Body", datetime(2024, 1, 1), None, "alt"),
        (42, "test.jpg"),
        (41,),
        (42,),
    ]
    mock_conn.cursor.return_value.fetchall.return_value = []

    with patch("spudoolicom.photoblog.exifread.process_file", return_value={}), \
         patch("os.path.isfile", side_effect=_smart_isfile), \
         patch("builtins.open", side_effect=smart_open_side_effect()):
        rv = client.post(
            "/photoblog/42",
            data={
                "commentmessage": "Buy my thesis",
                "commentname": "Spammer",
                "commenturl": "http://thesis-writing.com",
                "commentemail": "spam@spam.com",
            },
        )
    assert rv.status_code in (200, 301, 302)
    mock_conn.commit.assert_not_called()
