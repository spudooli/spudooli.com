# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

This is a Flask application. Run it with:

```bash
flask --app spudoolicom run
# or in debug mode:
flask --app spudoolicom run --debug
```

The app is deployed at `/var/www/spudooli/` on the server.

## Dependencies

Install system and Python dependencies:

```bash
sudo apt install libmysqlclient-dev redis
pip3 install flask flask-caching flask_mysqldb mysql-connector-python paho-mqtt rrdtool pyserial exifread typesense flask-wtf redis requests werkzeug
```

## Architecture

This is a personal "lifelogging" / home automation website (`spudooli.com`). The app package is `spudoolicom/` — a single Flask app with no blueprints (except `auth`). All modules are imported in `__init__.py` and register routes directly on the `app` instance.

**Data stores:**
- **MySQL** (`spudooli` database, configured in `db.py`) — primary storage for photoblog posts, comments, location tracking, activity feed, budget/bank data, contact messages
- **Redis** (localhost:6379) — real-time sensor values (temperatures, power usage, bank balance, weather forecasts, car battery/range, fridge door counter)
- **Typesense** (localhost:8108) — full-text search index for photoblog posts

**Key modules and their routes:**

| Module | Routes |
|--------|--------|
| `main.py` | `/`, `/rss`, `/status`, `/about`, `/now`, `/contactus`, `/power` |
| `photoblog.py` | `/photoblog`, `/photoblog/<id>`, `/photoblog/archive`, `/photoblog-map` |
| `recently.py` | `/recently/<date>` — daily activity feed (LastFM scrobbles, Swarm checkins, Mastodon posts, budget transactions) |
| `house.py` | `/house` — home sensor dashboard (temps, humidity, fridge door, EV range) |
| `charts.py` | `/house/charts/<where>` — RRDtool-generated chart images from `static/charts/` |
| `weather.py` | `/weather` — weather forecast from Redis |
| `webcam.py` | `/webcam/camera/<camera>` — kitchen/mancave/driveway webcam views; LED control endpoints |
| `hook.py` | `/hook/lights`, `/hook/tv`, `/hook/amp` — MQTT publishers for home automation; `/hook/github` — stores GitHub push events in `recently` table |
| `track.py` | `/track/<who>` — OwnTracks-compatible GPS receiver, publishes to MQTT and saves static map tiles |
| `search.py` | `/search` — Typesense search over photoblog |
| `admin.py` | `/admin/*` — login-protected photoblog post creation/editing |
| `auth.py` | `/auth/login`, `/auth/logout` — session-based auth via `users` MySQL table |
| `money.py` | Budget/bank balance routes |
| `photos.py` | Photo album routes |
| `alice.py`, `sarah.py` | Per-person location/tracking pages |
| `bmwi3.py` | BMW i3 EV data page |
| `location.py` | Location display routes |
| `projects.py` | Projects page |

**MQTT broker** at `192.168.1.2:1883` is used by `hook.py` and `track.py` to publish home automation commands and location updates.

**Local tile server** at `http://localhost:8080` (TileServer GL / osm-bright style) generates static map PNGs for location tracking.

**Photo files** are stored at `/var/www/spudooli/spudoolicom/static/photoblog/` (not in the repo).

## Config

`spudoolicom/config.py` sets Flask config keys including `SECRET_KEY`, `UPLOAD_PATH`, Cloudflare Turnstile keys, and `RECAPTCHA_*` settings. MySQL credentials are hardcoded in `db.py`.

## Testing

```bash
python3 -m pytest tests/
```

Key fixture notes (important for adding new tests):
- Use `client` fixture (not `app` — conflicts with pytest-flask)
- `auth_client` yields `(client, mock_conn)` with `user_id=1` in session
- Redis, Typesense, and RotatingFileHandler are patched at module level in `conftest.py`
- `/var/www/` file paths are proxied to mocks; all other paths hit the real filesystem

Known bugs documented as `xfail` in the suite (intentionally not yet fixed):
- `main.py`: `bankbalance.split('.')[0]` crashes if Redis returns None
- `house.py`: string concat with Redis None crashes
- `weather.py`: UnboundLocalError on unrecognised forecast word
- `recently.py`: date/string comparison always false
- `auth.py`: `url_for('index')` fails (endpoint is named `main`)
- `photoblog.py`: unconditional `open()` → FileNotFoundError if image missing

## Search Index Management

Scripts in `bin/` manage the Typesense index:
- `bin/search-create.py` — creates the collection schema
- `bin/website-typesense.py` — indexes photoblog posts
- `bin/search-test.py` — test queries
