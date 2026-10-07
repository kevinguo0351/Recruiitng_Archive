CREATE INDEX idx_jobs_company ON jobs(company_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_application_events_application ON application_events(application_id, occurred_at);

CREATE VIEW application_summary AS
SELECT
    a.id AS application_id,
    c.public_alias AS candidate,
    co.name AS company,
    j.title,
    j.location,
    j.track,
    j.job_url,
    a.status,
    a.match_score,
    co.sponsorship_status,
    a.sponsorship_confidence,
    a.updated_at
FROM applications a
JOIN candidates c ON c.id = a.candidate_id
JOIN jobs j ON j.id = a.job_id
JOIN companies co ON co.id = j.company_id;
