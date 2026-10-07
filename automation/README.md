# Scheduled workflow definition

This directory preserves the recurring recruiting workflow in a transferable,
sanitized form. It contains a **task definition**, not an active schedule.
Committing these files does not start a timer, grant browser access, or authorize
job submissions.

## Timing

The archived cadence is twice daily at **00:00 and 05:00 America/Denver**. The
timezone is intentionally named instead of stored as a fixed UTC offset so the
runtime can apply daylight-saving changes. The observed October cadence was
06:00 and 11:00 UTC while Denver was on MDT.

## Files

- `recruiting-job-search.yaml` contains timing, input contracts, dependencies,
  environment-variable names, and safety rules.
- `prompt.md` is the sanitized prompt replayed by each scheduled run.

## Recreate the schedule

1. Create private directories outside the repository for candidate inputs,
   mutable state, and generated application packages.
2. Set the environment variables listed in the YAML file. Do not put their
   values in Git.
3. Add a candidate profile and base resume to the private data directory. The
   profile should define role priorities, graduation/start windows, location,
   work-authorization answers, sponsorship needs, compensation policy, and
   whether autonomous submission is permitted.
4. Initialize the progress workbook and activity log in the state directory.
5. In a Codex client that supports recurring automations, create two daily local
   schedules in the `America/Denver` timezone: one at 00:00 and one at 05:00.
   Use the contents of `prompt.md` as the task prompt and provide the configured
   local workspace as its execution context.
6. Run once manually with submission disabled. Confirm that private values do
   not appear in Git output and that state updates are idempotent.
7. Enable the schedules only after the operator reviews the candidate profile,
   authorization policy, browser access, and output locations.

An active schedule must be inspected and managed in the Codex client where it
was created. This repository cannot determine whether the original automation
is active, paused, changed, or deleted.
