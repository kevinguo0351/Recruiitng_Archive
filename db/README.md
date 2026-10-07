# Database

The tracker uses SQLite. Migrations are ordered SQL files in `migrations/`; the web
application records applied files in `schema_migrations`. The schema separates reusable
employer and job research from candidate-specific application activity.

## Relationships

- A `company` has many `jobs`.
- A `candidate` has many `applications`; each application belongs to one job.
- An `application` has many immutable `application_events` for workflow history.
- A `job` has many `research_sources` for provenance.
- `application_summary` is a read-only view used by the dashboard API.

## Create a local demo database

From the repository root:

```powershell
python web/app.py --seed
```

The default output is `var/recruiting.db`, which is intentionally ignored and must never
be committed when it contains real applicant information. Override it with the
`RECRUITING_DB_PATH` environment variable.

The seed file contains fictional records and `.invalid` URLs. It is safe for tests and demos.
