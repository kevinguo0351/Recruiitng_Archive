# Recruiting Archive

Sanitized, reusable assets from a local Codex recruiting workflow. The repository contains a job research and application archive pattern, an ATS tailoring skill, a small tracker website, database schema and migrations, and inactive schedule definitions.

No real candidate resume, contact details, immigration records, application answers, credentials, browser state, or private conversation history is stored here. See [`docs/previous-project-handoff.md`](docs/previous-project-handoff.md) for architecture, setup, validation, exclusions, and integration guidance.

## Quick start

```powershell
Copy-Item .env.example .env
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python web/app.py --seed
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python -m unittest discover -s web/tests -v
```

Open <http://127.0.0.1:8000>. The checked-in data is synthetic. Keep real candidate inputs under a local ignored `private/` directory.

## Repository context

This repository was originally created for Codex/Claude cloud environment handoff. The import preserves that purpose and adds a runnable, sanitized reference implementation.
