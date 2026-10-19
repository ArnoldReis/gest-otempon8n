"""Reference-only chat gate for synthetic operational snapshots.

No production workflow, network calls, tokens or organization data are included.
The deployed n8n workflow remains the authoritative implementation.
"""
from typing import Any, Mapping


def evaluate_question(snapshot_row: Mapping[str, Any] | None, question: str) -> tuple[bool, str]:
    """Permit grounded queries even when the alert list is empty.

    The simulated backend must have identified the saved snapshot; a client
    cannot establish authenticity by declaring its own snapshot as trusted.
    """
    if not isinstance(question, str) or not 5 <= len(question.strip()) <= 220:
        return False, "invalid_question"
    if not isinstance(snapshot_row, Mapping) or snapshot_row.get("verified") is not True:
        return False, "missing_snapshot"

    report = snapshot_row.get("report")
    if not isinstance(report, Mapping):
        return False, "missing_snapshot"
    if not isinstance(report.get("generated_at"), str) or not report["generated_at"].strip():
        return False, "missing_snapshot"

    has_structured_data = (
        isinstance(report.get("all_items"), list)
        or isinstance(report.get("executive"), Mapping)
        or isinstance(report.get("tempo_ti"), Mapping)
        or isinstance(report.get("delivery"), Mapping)
    )
    if not has_structured_data:
        return False, "missing_snapshot"
    return True, "accepted"
