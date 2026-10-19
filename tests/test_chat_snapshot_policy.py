"""Synthetic regression tests: an empty alert list is not an empty snapshot."""
import unittest
from reference.chat_policy import evaluate_question


def snapshot(**changes):
    report = {
        "generated_at": "2026-01-01T09:00:00Z",
        "all_items": [],
        "tempo_ti": {"ok": True, "summary": {"total_ms": 0}},
    }
    report.update(changes)
    return {"verified": True, "report": report}


class ChatSnapshotPolicyTests(unittest.TestCase):
    def test_empty_alert_list_still_allows_time_question(self):
        self.assertEqual(
            (True, "accepted"),
            evaluate_question(snapshot(), "Quantas horas foram rastreadas?"),
        )

    def test_empty_alert_list_still_allows_executive_question(self):
        data = snapshot(all_items=[], executive={"counts": {"urgent": 0}})
        self.assertEqual((True, "accepted"), evaluate_question(data, "Como está a gestão hoje?"))

    def test_delivery_only_snapshot_is_usable(self):
        data = snapshot(all_items=None, tempo_ti=None, delivery={"week": {"created": 0}})
        self.assertEqual((True, "accepted"), evaluate_question(data, "Houve entregas nesta semana?"))

    def test_snapshot_can_have_nonempty_alerts(self):
        data = snapshot(all_items=[{"id": "issue-demo"}])
        self.assertEqual((True, "accepted"), evaluate_question(data, "Quais são as prioridades?"))

    def test_missing_snapshot_is_not_represented_as_zero_alerts(self):
        self.assertEqual((False, "missing_snapshot"), evaluate_question(None, "Quais são as prioridades?"))

    def test_unverified_snapshot_is_rejected(self):
        data = snapshot()
        data["verified"] = False
        self.assertEqual((False, "missing_snapshot"), evaluate_question(data, "Quais são as prioridades?"))

    def test_missing_capture_timestamp_is_rejected(self):
        self.assertEqual(
            (False, "missing_snapshot"),
            evaluate_question(snapshot(generated_at=None), "Como está a gestão hoje?"),
        )

    def test_unstructured_capture_is_rejected(self):
        data = snapshot(all_items=None, tempo_ti=None)
        self.assertEqual((False, "missing_snapshot"), evaluate_question(data, "Como está a gestão hoje?"))

    def test_question_length_limits(self):
        data = snapshot()
        for question in ["", "olá", "x" * 221]:
            with self.subTest(size=len(question)):
                self.assertEqual((False, "invalid_question"), evaluate_question(data, question))


if __name__ == "__main__":
    unittest.main()
