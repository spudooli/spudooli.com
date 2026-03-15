"""
Tests for auth.py: login, logout, session management, login_required decorator.
"""
import pytest
from werkzeug.security import generate_password_hash
from tests.conftest import make_cursor


def _user_row(username="dave", password="pw"):
    return (1, username, generate_password_hash(password))


# ── GET /auth/login ───────────────────────────────────────────────────────────


def test_login_page_returns_200(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200


def test_login_page_renders_form(client):
    rv = client.get("/auth/login")
    assert b"form" in rv.data.lower()


# ── POST /auth/login ──────────────────────────────────────────────────────────


def test_login_correct_credentials_redirects(client, mock_db):
    """Correct username + password → redirect to admin checkin page."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.return_value = _user_row(password="pw")
    rv = client.post(
        "/auth/login", data={"username": "dave", "password": "pw"}
    )
    assert rv.status_code == 302
    assert "checkin" in rv.headers["Location"].lower()


def test_login_wrong_password_redirects_back(client, mock_db):
    """Wrong password → redirect back to login (not to admin)."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.return_value = _user_row(password="correct")
    rv = client.post(
        "/auth/login", data={"username": "dave", "password": "wrongpassword"}
    )
    assert rv.status_code == 302
    assert "login" in rv.headers["Location"].lower()


def test_login_unknown_user_redirects_back(client, mock_db):
    """Unknown username → redirect back to login."""
    _, mock_conn = mock_db
    mock_conn.cursor.return_value.fetchone.return_value = None
    rv = client.post(
        "/auth/login", data={"username": "nobody", "password": "pw"}
    )
    assert rv.status_code == 302
    assert "login" in rv.headers["Location"].lower()


# ── GET /auth/logout ──────────────────────────────────────────────────────────


def test_logout_clears_session_and_redirects(auth_client):
    """Logout clears the session and redirects to the homepage."""
    c, _ = auth_client
    rv = c.get("/auth/logout")
    assert rv.status_code == 302
    # After logout, admin pages redirect to login
    rv2 = c.get("/admin/posts")
    assert rv2.status_code == 302
    assert "login" in rv2.headers["Location"].lower()


# ── login_required decorator ──────────────────────────────────────────────────


def test_admin_requires_auth_unauthenticated(client):
    rv = client.get("/admin/posts")
    assert rv.status_code == 302
    assert "login" in rv.headers["Location"].lower()


def test_admin_create_requires_auth(client):
    rv = client.get("/admin/create")
    assert rv.status_code == 302
    assert "login" in rv.headers["Location"].lower()


def test_admin_comments_requires_auth(client):
    rv = client.get("/admin/comments")
    assert rv.status_code == 302
    assert "login" in rv.headers["Location"].lower()


def test_admin_checkin_requires_auth(client):
    rv = client.get("/admin/checkin")
    assert rv.status_code == 302
    assert "login" in rv.headers["Location"].lower()


# ── Authenticated access ──────────────────────────────────────────────────────


def test_admin_posts_accessible_when_authenticated(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/posts")
    assert rv.status_code == 200


def test_admin_checkin_accessible_when_authenticated(auth_client):
    c, _ = auth_client
    rv = c.get("/admin/checkin")
    assert rv.status_code == 200
