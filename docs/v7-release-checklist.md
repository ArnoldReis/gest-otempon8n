# V7.0 — Release checklist for an operations copilot

This is a **public, synthetic engineering reference**. No customer records, private endpoints, production workflow exports, credentials or company-specific configuration belong in this repository.

## Release goals

- A consolidated read-only operational dashboard.
- A chat assistant that answers using a versioned data snapshot and cites verifiable sources when item-specific claims are made.
- An explicit distinction between task tracker time and automatic session time.
- Reconciled metrics for task creation, delivery and reopening **only where verified transition events exist**.
- Resilient presentation during partial upstream outages: unavailable does not mean zero.

## Source reliability

| State | Interface behavior |
| --- | --- |
| Healthy | Show numeric measure and capture timestamp |
| Partial | Show measure only with coverage caveat, or unknown if missing data invalidate it |
| Error | Show em dash / unavailable; never fabricate a zero |
| No history | Show incomplete / awaiting verified events |
| Stale snapshot | Indicate capture age; do not claim live monitoring |

## Reporting period contracts

- **Week**: rolling last 7 days from the snapshot instant.
- **Month**: current calendar month beginning at 00:00 in the business reporting timezone.
- Event deduplication is per task and transition type in each window.
- Backlog/current open tasks are a *snapshot*, **not** historical created or completed totals.
- Historic coverage is necessarily partial when event recording started later than the requested reporting period.
- A task disappearing from an alert list is not evidence that it was completed or corrected.

## Time-tracking contracts

- Tracker API rows and automatic session rows are separate sources. Never sum them into a single productivity measure.
- For the automatic capture workflow, distinguish captured, reviewed/confirmed, pending, suspect and open time.
- For business decisions, attribute time to work items by exact task IDs only; an unlinked time entry is not evidence of completion.
- Avoid individual productivity rankings based on hours.

## Chat acceptance

1. Open the panel with a session token.
2. Send a short greeting.
3. Ask an item-specific question requiring an exact source link.
4. Ask a follow-up requiring conversation context.
5. Ask for indicators covering multiple categories in one question.
6. Verify the model clearly says when data are missing, stale or partial.
7. Force an invalid/expired token and confirm inference does not run.
8. Simulate a network failure; do not automatically send a duplicate inference.
9. Verify the client handles JSON responses in the same view without navigation.
10. Verify session renewal, an expired session and an unsuccessful renewal.
11. Repeat with a desktop browser and a mobile viewport — server tests alone **do not** certify browser experience.

## Operational gates

- Validate source health and last-capture timestamps after each rollout.
- Verify non-admin reading cannot trigger administrative data collection.
- Check that background refresh cadence does not overlap with expensive inference.
- Preserve the last known-good published workflow version for rollback.
- Monitor execution failures and AI budget control; non-atomic counters are approximate under concurrency.
- Keep browser network response metadata minimal and disable sensitive caching.

## Explicit security boundary

The decision to defer external identity provisioning does **not** make a public webhook private. Chat session tokens and CORS headers are not user authentication; do not distribute internal dashboard links as if only authorized readers can view them. This item remains an explicit release limitation rather than an implemented security feature.

## Completion definition

A version is **operationally stable** only once source contracts, chat server tests, browser tests and data-partial scenarios pass. A successful backend response alone cannot certify UI/UX. Mark remaining tests as pending when they cannot be observed.
