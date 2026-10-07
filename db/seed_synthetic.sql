-- Synthetic demonstration data only. Names and URLs are intentionally fictional.
INSERT INTO companies (id, name, website_url, sponsorship_status, sponsorship_evidence) VALUES
    (1, 'Example Analytics', 'https://example.invalid/analytics', 'possible', 'Synthetic policy example; verify before applying.'),
    (2, 'Demo Advisory Group', 'https://example.invalid/advisory', 'unknown', 'No synthetic evidence available.');

INSERT INTO jobs (
    id, company_id, external_job_id, title, location, job_url, track,
    experience_min_years, experience_max_years, graduation_window, jd_snapshot_path
) VALUES
    (1, 1, 'DEMO-001', 'Associate Product Analyst', 'New York, NY',
     'https://example.invalid/jobs/demo-001', 'Product', 0, 2, 'Spring 2027',
     'examples/synthetic-job-description.md'),
    (2, 2, 'DEMO-002', 'Graduate Strategy Analyst', 'Chicago, IL',
     'https://example.invalid/jobs/demo-002', 'Strategy', 0, 1, '2027 graduates', NULL);

INSERT INTO candidates (
    id, public_alias, graduation_date, earliest_start_date, requires_future_sponsorship
) VALUES
    (1, 'Synthetic Candidate', '2027-04-30', '2027-05-20', 1);

INSERT INTO applications (
    id, candidate_id, job_id, status, match_score, sponsorship_confidence, notes
) VALUES
    (1, 1, 1, 'ready', 88, 'medium', 'Synthetic record for interface testing.'),
    (2, 1, 2, 'researching', 76, 'unknown', 'Synthetic record; sponsorship requires research.');

INSERT INTO application_events (
    application_id, event_type, from_status, to_status, note, occurred_at
) VALUES
    (1, 'status_change', 'researching', 'ready', 'Synthetic workflow event.', '2026-10-01T10:00:00Z'),
    (2, 'created', NULL, 'researching', 'Synthetic workflow event.', '2026-10-02T10:00:00Z');

INSERT INTO research_sources (job_id, source_type, source_url, title) VALUES
    (1, 'official_jd', 'https://example.invalid/jobs/demo-001', 'Synthetic official job description'),
    (1, 'visa', 'https://example.invalid/policy', 'Synthetic sponsorship policy');
