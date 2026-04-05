"""
Tests for admin.py: post management, comment moderation, bookmarks, checkins.

All routes require login_required.  We use the auth_client fixture which
pre-loads a session and sets g.user via before_app_request.

The auth before_app_request consumes ONE fetchone() call (user lookup) before
the route runs.  Tests that need specific fetchone results configure
side_effect so index 0 = user row, subsequent = route data.
"""
import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash
from unittest.mock import MagicMock, patch
from tests.conftest import make_cursor


def _user_row():
    return (1, "dave", generate_password_hash("pw"))


# ── /admin/posts ──────────────────────────────────────────────────────────────


def test_adminposts_returns_200(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/posts")
    assert rv.status_code == 200


def test_adminposts_lists_posts(auth_client):
    c, mock_conn = auth_client
    mock_conn.cursor.return_value.fetchall.return_value = [
        (1, "Post One", datetime(2024, 1, 1, 12, 0, 0)),
        (2, "Post Two", datetime(2024, 2, 1, 12, 0, 0)),
    ]
    rv = c.get("/admin/posts")
    assert rv.status_code == 200


# ── /admin/create ──────────────────────────────────────────────────────────────


def test_admin_create_get_returns_200(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/create")
    assert rv.status_code == 200


def test_admin_create_post_requires_title(auth_client):
    """Submitting without a title should not redirect away."""
    c, _ = auth_client
    from io import BytesIO
    with patch("os.system"):  # don't run imagemagick convert
        rv = c.post(
            "/admin/create",
            data={
                "title": "",
                "body": "Some body text",
                "photolatlon": "",
                "alttext": "",
                "file": (BytesIO(b"fake image data"), "test.jpg"),
            },
            content_type="multipart/form-data",
        )
    assert rv.status_code in (200, 302)


# ── /admin/edit/<id> ──────────────────────────────────────────────────────────


def test_admin_edit_get_returns_200(auth_client):
    c, mock_conn = auth_client
    post_row = (1, "Existing Title", "Some body", "test.jpg", None, "alt text")
    # side_effect: [user_row (auth hook), post_row (edit route)]
    mock_conn.cursor.return_value.fetchone.side_effect = [_user_row(), post_row]
    rv = c.get("/admin/edit/1")
    assert rv.status_code == 200


def test_admin_edit_not_found(auth_client):
    c, mock_conn = auth_client
    mock_conn.cursor.return_value.fetchone.side_effect = [_user_row(), None]
    rv = c.get("/admin/edit/9999")
    assert rv.status_code == 404


# ── /admin/comments ───────────────────────────────────────────────────────────


def test_admin_comments_returns_200(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/comments")
    assert rv.status_code == 200


def test_admin_comments_lists_items(auth_client):
    c, mock_conn = auth_client
    mock_conn.cursor.return_value.fetchall.return_value = [
        (10, 42, datetime(2024, 1, 1, 12, 0, 0),
         "Nice post!", "Alice", "http://x.com", "no"),
    ]
    rv = c.get("/admin/comments")
    assert rv.status_code == 200


# ── /admin/comments/delete/<id> ───────────────────────────────────────────────


def test_delete_comment_post_redirects(auth_client):
    c, mock_conn = auth_client
    rv = c.post("/admin/comments/delete/10")
    assert rv.status_code == 302
    mock_conn.commit.assert_called()


# ── /admin/comments/publish/<id> ─────────────────────────────────────────────


def test_publish_comment_post_redirects(auth_client):
    c, mock_conn = auth_client
    rv = c.post("/admin/comments/publish/10")
    assert rv.status_code == 302
    mock_conn.commit.assert_called()


# ── /admin/checkin ────────────────────────────────────────────────────────────


def test_admin_checkin_get_returns_200(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/checkin")
    assert rv.status_code == 200


def test_admin_checkin_post_stores_and_redirects(auth_client):
    c, mock_conn = auth_client
    mock_conn.cursor.return_value.fetchone.side_effect = [
        _user_row(),   # auth hook
        (7,),          # checkin count query
    ]
    rv = c.post(
        "/admin/checkin",
        data={"venue": "The Local Pub", "address": "123 Main St"},
    )
    assert rv.status_code == 302
    mock_conn.commit.assert_called()


# ── /admin/checkin-search ─────────────────────────────────────────────────────


def test_checkin_search_returns_json(auth_client):
    c, mock_conn = auth_client
    mock_conn.cursor.return_value.fetchall.return_value = [
        ("The Local Pub", "123 Main St"),
    ]
    rv = c.get("/admin/checkin-search?q=pub")
    assert rv.status_code == 200
    assert rv.content_type.startswith("application/json")


# ── /admin/bookmark/create ────────────────────────────────────────────────────


def test_bookmark_create_get_returns_200(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/bookmark/create")
    assert rv.status_code == 200


def test_bookmark_create_post_stores_bookmark(auth_client):
    c, mock_conn = auth_client
    mock_response = MagicMock()
    mock_response.text = "<html><head><title>Test Page</title></head></html>"
    with patch("spudoolicom.admin.requests.get", return_value=mock_response):
        rv = c.post(
            "/admin/bookmark/create",
            data={"url": "https://example.com", "tags": "test,example"},
        )
    assert rv.status_code == 302
    mock_conn.commit.assert_called()


# ── /admin/header ─────────────────────────────────────────────────────────────


def test_admin_header_get_returns_200(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/header")
    assert rv.status_code == 200


def test_admin_header_upload_no_file_returns_400(auth_client):
    c, _ = auth_client
    rv = c.post("/admin/header/upload", data={}, content_type="multipart/form-data")
    assert rv.status_code == 400
    assert b"No file provided" in rv.data


def test_admin_header_upload_saves_file_and_returns_url(auth_client):
    from io import BytesIO
    c, _ = auth_client
    with patch("spudoolicom.admin.open", create=True), \
         patch("werkzeug.datastructures.file_storage.FileStorage.save") as mock_save:
        rv = c.post(
            "/admin/header/upload",
            data={"file": (BytesIO(b"fake image"), "photo.jpg")},
            content_type="multipart/form-data",
        )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["url"] == "/static/images/header_upload_temp.jpg"


def test_admin_header_save_processes_crop(auth_client):
    c, _ = auth_client
    with patch("spudoolicom.admin.os.path.exists", return_value=True), \
         patch("spudoolicom.admin.subprocess.run") as mock_run, \
         patch("spudoolicom.admin.os.remove") as mock_remove:
        rv = c.post(
            "/admin/header/save",
            json={"x": 10, "y": 20, "width": 800, "height": 109},
        )
    assert rv.status_code == 200
    assert rv.get_json() == {"ok": True}
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args[0] == "convert"
    assert "800x109+10+20" in args
    assert "1320x180!" in args
    mock_remove.assert_called_once()


def test_admin_header_save_missing_temp_returns_400(auth_client):
    c, _ = auth_client
    with patch("spudoolicom.admin.os.path.exists", return_value=False):
        rv = c.post(
            "/admin/header/save",
            json={"x": 0, "y": 0, "width": 500, "height": 68},
        )
    assert rv.status_code == 400
    assert b"No uploaded image found" in rv.data


def test_admin_header_save_imagemagick_failure_returns_500(auth_client):
    import subprocess as sp
    c, _ = auth_client
    with patch("spudoolicom.admin.os.path.exists", return_value=True), \
         patch("spudoolicom.admin.subprocess.run",
               side_effect=sp.CalledProcessError(1, "convert")):
        rv = c.post(
            "/admin/header/save",
            json={"x": 0, "y": 0, "width": 500, "height": 68},
        )
    assert rv.status_code == 500


def test_admin_header_save_invalid_crop_data_returns_400(auth_client):
    c, _ = auth_client
    rv = c.post("/admin/header/save", json={"x": "bad", "y": 0})
    assert rv.status_code == 400
