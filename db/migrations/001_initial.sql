PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    website_url TEXT,
    sponsorship_status TEXT NOT NULL DEFAULT 'unknown'
        CHECK (sponsorship_status IN ('confirmed', 'possible', 'unknown', 'unlikely', 'none')),
    sponsorship_evidence TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    external_job_id TEXT,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    job_url TEXT NOT NULL,
    track TEXT NOT NULL,
    experience_min_years INTEGER NOT NULL DEFAULT 0 CHECK (experience_min_years >= 0),
    experience_max_years INTEGER CHECK (
        experience_max_years IS NULL OR experience_max_years >= experience_min_years
    ),
    graduation_window TEXT,
    jd_snapshot_path TEXT,
    discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (company_id, job_url)
);

CREATE TABLE candidates (
    id INTEGER PRIMARY KEY,
    public_alias TEXT NOT NULL UNIQUE,
    graduation_date TEXT,
    earliest_start_date TEXT,
    requires_future_sponsorship INTEGER NOT NULL DEFAULT 0
        CHECK (requires_future_sponsorship IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'researching'
        CHECK (status IN (
            'researching', 'ready', 'needs_action', 'submitted',
            'interviewing', 'offer', 'rejected', 'withdrawn', 'skipped'
        )),
    match_score INTEGER CHECK (match_score BETWEEN 0 AND 100),
    sponsorship_confidence TEXT NOT NULL DEFAULT 'unknown'
        CHECK (sponsorship_confidence IN ('high', 'medium', 'low', 'unknown')),
    tailored_resume_path TEXT,
    notes TEXT,
    submitted_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (candidate_id, job_id)
);

CREATE TABLE application_events (
    id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    from_status TEXT,
    to_status TEXT,
    note TEXT,
    occurred_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_sources (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL CHECK (source_type IN ('official_jd', 'company', 'review', 'visa', 'other')),
    source_url TEXT NOT NULL,
    title TEXT,
    captured_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (job_id, source_url)
);
