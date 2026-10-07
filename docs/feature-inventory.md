# Previous recruiting project feature inventory

This inventory describes transferable capabilities. Candidate records, resumes,
private conversations, credentials, and application databases are excluded.

## Completed

| Capability | Transferable asset | Validation | Known limitation |
|---|---|---|---|
| Twice-daily workflow specification | `automation/recruiting-job-search.yaml`, `automation/prompt.md` | Timing reconstructed from observed runs at 00:00 and 05:00 America/Denver | Definition only; repository state does not prove an automation is active |
| Schedule recreation guide | `automation/README.md` | Includes timezone, inputs, dependencies, environment names, dry-run procedure, and activation boundary | Client UI and automation API can change |
| Job screening policy | `automation/prompt.md` | Covers graduation/start eligibility, experience level, sponsorship, duplicate prevention, and status reporting | Public sponsorship evidence may be inconclusive |
| Truthful ATS tailoring policy | `automation/prompt.md` | Explicitly limits changes to verified facts and keyword-aligned wording | Tailored output still requires visual and factual review |
| Submission audit rule | `automation/prompt.md` | Requires visible success before `submitted` status | Some employer sites send confirmation only by email |
| Normalized archive database | `db/migrations/`, `db/seed_synthetic.sql` | Migrations, synthetic seed, two-row summary, and SQLite integrity check passed | No private-data importer |
| Local tracker website | `web/` | Five unit tests and Python compilation passed | Read-only, loopback-only, no authentication |
| Application package scaffold | `scripts/scaffold_application.py`, `templates/` | Additive behavior tested; existing files preserved | Research still requires verified sources |
| ATS PDF builder | `scripts/build_ats_resume.py` | Synthetic resume generated as one page | Real outputs still require factual and visual review |
| Excel and Markdown tracker builder | `scripts/build_tracker.py` | Synthetic outputs and invalid-row rejection tested | Does not submit applications |
| Sensitive-content gate | `scripts/check_sensitive_content.py` | Generic scan and two unit tests passed; project-specific forbidden terms also scanned | Pattern based; staged diff still requires human review |

## Partial

| Capability | Current state | Next integration work |
|---|---|---|
| Browser-based application submission | Policy and pause conditions are documented | Reconcile with the existing program's browser adapter and authentication flow |
| Spreadsheet and Markdown progress tracking | Input/output contract is documented | Map fields to the existing recruiting program's canonical data model |
| Employer and job research archive | Expected output and evidence rules are documented | Reuse the repository's storage abstraction and add retention/deduplication rules |
| Tailored resume packages | Prompt contract is documented | Connect the reusable tailoring skill and add deterministic render checks |

## Planned

| Capability | Recommended implementation |
|---|---|
| Automated regression tests | Test deduplication, eligibility windows, sponsorship exclusions, PII redaction, and submitted-status transitions |
| Schedule observability | Add run IDs, duration, error category, last successful run, and stale-run alerts |
| Secure export/import | Export schemas, code, and redacted metadata separately from encrypted candidate data |

## Excluded private assets

The archive intentionally excludes resumes, candidate contact details,
work-authorization documents, account credentials, tokens, private chat history,
live application workbooks, and database files containing personal information.
Those originals remain local.

For a secure migration, export private data outside Git into an encrypted archive,
verify its manifest and checksum, transfer it through an approved private channel,
and decrypt it only into the paths named by `RECRUITING_PRIVATE_DATA_DIR` and
`RECRUITING_STATE_DIR`. Commit only synthetic fixtures and redacted metadata.
