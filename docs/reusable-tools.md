# Reusable recruiting tools

These assets were rebuilt from a local recruiting workflow after removing personal records, resumes, company-specific application content, absolute paths, and credentials.

## Contents

- `skills/job-application-tailor/`: reusable Codex skill and research rules.
- `templates/`: blank research notes plus synthetic profile and tracker examples.
- `scripts/scaffold_application.py`: additive company and role folder creation. Existing notes are not overwritten.
- `scripts/build_ats_resume.py`: one-column PDF resume renderer driven by verified JSON.
- `scripts/build_tracker.py`: JSON-to-Markdown and Excel tracker generator.
- `tests/test_recruiting_tools.py`: scaffold, tracker, validation, and one-page PDF checks.

## Install and run

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts/scaffold_application.py C:\secure\applications "Example Company" "2027 Analyst"
.venv\Scripts\python scripts/build_ats_resume.py templates/applicant-profile.example.json build/example-resume.pdf
.venv\Scripts\python scripts/build_tracker.py templates/applications.example.json --xlsx build/tracker.xlsx --markdown build/tracker.md
.venv\Scripts\python -m unittest discover -s tests -v
```

The examples use synthetic identities and `example.test` URLs. Copy them outside source control before inserting applicant facts. Final application packages and generated resumes contain personal information and should remain local.

## Validation boundary

The renderer checks its input shape and the tests verify the synthetic output is a one-page PDF. A human must still inspect every real resume for accuracy, clipping, line wrapping, and layout. The tracker is a recordkeeping tool; it does not submit applications or infer whether an application succeeded.

Before committing, run `python scripts/check_sensitive_content.py`. Add one or more `--forbid "literal"` arguments for project-specific candidate names or identifiers that the generic patterns cannot know.
