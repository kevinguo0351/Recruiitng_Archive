# Local recruiting tracker

This read-only local dashboard exposes a small JSON API over the SQLite archive and serves a
responsive status table. It does not upload data or implement authentication, so bind it to
the default loopback address unless an authentication layer is added.

## Requirements

- Python 3.11 or newer
- No third-party packages (`requirements.txt` documents this explicitly)

## Run

From the repository root:

```powershell
python web/app.py --seed
```

Open <http://127.0.0.1:8000>. Migrations apply automatically. On later runs, omit `--seed`
because seeding transactionally refuses to modify a database containing any domain record.

Environment variable names and empty placeholders are listed in `examples/env.example`.

## API

- `GET /api/health`
- `GET /api/summary`
- `GET /api/applications`
- `GET /api/applications?status=ready`

## Test

```powershell
python -m unittest discover -s web/tests -v
```

Tests create a temporary database, apply every migration, load only synthetic records, and
check querying, filtering, summary counts, and foreign-key enforcement.
