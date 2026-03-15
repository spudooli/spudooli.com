"""
Shared fixtures for the spudooli.com test suite.

Key challenge: three modules (main, house, weather) create module-level Redis
clients at import time, and search.py creates a Typesense client at import time.
These are patched at MODULE LEVEL before any test-triggered imports happen.

NOTE: The fixture that yields a test client is named `client` (not `app`) to
avoid conflicting with pytest-flask's built-in `app` fixture hook.
"""
import builtins
import pytest
from unittest.mock import MagicMock, patch, mock_open


# ── Module-level patches ─────────────────────────────────────────────────────
# Must be active BEFORE spudoolicom is first imported (which happens when the
# first test fixture calls `from spudoolicom import app`).

_sentinel_redis = MagicMock()
_sentinel_redis.get.return_value = "20"

_redis_patch = patch("redis.from_url", return_value=_sentinel_redis)
_redis_patch.start()

_mock_typesense_client = MagicMock()
_typesense_patch = patch("typesense.Client", return_value=_mock_typesense_client)
_typesense_patch.start()

# spudoolicom/__init__.py creates a RotatingFileHandler at import time when
# app.debug is False.  In a test environment /tmp/spud.log may not be writable.
_log_patch = patch("logging.handlers.RotatingFileHandler", MagicMock())
_log_patch.start()

# ─────────────────────────────────────────────────────────────────────────────


def make_cursor(fetchone=None, fetchall=None):
    """Helper: a mock DB cursor with preset return values."""
    c = MagicMock()
    c.fetchone.return_value = fetchone
    c.fetchall.return_value = fetchall if fetchall is not None else []
    return c


def smart_open_side_effect():
    """
    Returns a side_effect for builtins.open that:
    - Mocks any path under /var/www/ or /tmp/ (image files, log files, etc.)
    - Proxies everything else to the real open (so Flask template loading works)
    """
    _real_open = builtins.open

    def _smart(path, *args, **kwargs):
        if "/var/www/" in str(path) or "/tmp/" in str(path):
            m = MagicMock()
            m.__enter__ = lambda s: s
            m.__exit__ = MagicMock(return_value=False)
            m.read.return_value = b""
            m.write = MagicMock()
            m.readlines.return_value = []
            return m
        return _real_open(path, *args, **kwargs)

    return _smart


def _inject_redis(monkeypatch, mock_r):
    import spudoolicom.main
    import spudoolicom.house
    import spudoolicom.weather
    monkeypatch.setattr(spudoolicom.main, "r", mock_r)
    monkeypatch.setattr(spudoolicom.house, "r", mock_r)
    monkeypatch.setattr(spudoolicom.weather, "r", mock_r)


@pytest.fixture
def mock_redis():
    """Per-test Redis mock (fresh MagicMock for each test)."""
    r = MagicMock()
    r.get.return_value = "20"
    return r


@pytest.fixture
def mock_db():
    """Patches spudoolicom.db.mysql for the duration of one test."""
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = make_cursor()
    with patch("spudoolicom.db.mysql") as mock_mysql:
        mock_mysql.connection = mock_conn
        yield mock_mysql, mock_conn


@pytest.fixture
def client(mock_db, mock_redis, monkeypatch):
    """Unauthenticated Flask test client with all external services mocked."""
    from spudoolicom import app as flask_app

    _inject_redis(monkeypatch, mock_redis)

    flask_app.config.update(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "RECAPTCHA_TESTING": True,
            "SECRET_KEY": "test-secret",
        }
    )
    with flask_app.test_client() as c:
        with flask_app.app_context():
            yield c


@pytest.fixture
def auth_client(mock_db, mock_redis, monkeypatch):
    """Authenticated Flask test client (session user_id=1, g.user set)."""
    from werkzeug.security import generate_password_hash
    from spudoolicom import app as flask_app

    _inject_redis(monkeypatch, mock_redis)

    flask_app.config.update(
        {"TESTING": True, "WTF_CSRF_ENABLED": False, "SECRET_KEY": "test-secret"}
    )

    _, mock_conn = mock_db
    # The before_app_request hook in auth.py calls cursor().fetchone() when
    # user_id is in the session. Provide the user row as the default.
    user_row = (1, "dave", generate_password_hash("pw"))
    mock_conn.cursor.return_value = make_cursor(fetchone=user_row)

    with flask_app.test_client() as c:
        with c.session_transaction() as sess:
            sess["user_id"] = 1
        with flask_app.app_context():
            yield c, mock_conn
