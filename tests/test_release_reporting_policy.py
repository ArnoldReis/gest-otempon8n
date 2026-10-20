"""Synthetic release-policy regression tests: no live business data."""
import unittest
from collections import Counter
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")


def month_start(now):
    local = now.astimezone(TZ)
    return local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def verified_count(events, start, now, kind):
    eligible = [
        e for e in events
        if e["verified"] and e["type"] == kind and start <= e["occurred_at"] <= now
    ]
    return len({e["task_id"] for e in eligible})


def display_metric(source_state, value):
    if source_state != "ok" or value is None:
        return "—"
    return str(value)


class ReportingPolicyTests(unittest.TestCase):
    def test_calendar_month_not_rolling_thirty_days(self):
        now = datetime(2026, 10, 20, 12, tzinfo=TZ)
        self.assertEqual(month_start(now).date().isoformat(), "2026-10-01")
        self.assertNotEqual(month_start(now), now - timedelta(days=30))

    def test_month_boundary_preserves_reporting_timezone(self):
        now_utc = datetime(2026, 11, 1, 1, 0, tzinfo=timezone.utc)
        # Still October 31 at 22:00 in Sao Paulo
        self.assertEqual(month_start(now_utc).date().isoformat(), "2026-10-01")

    def test_month_delivery_verified_and_deduplicated(self):
        now = datetime(2026, 10, 20, 9, tzinfo=TZ)
        events = [
            {"task_id": "synthetic-A", "type": "delivered", "verified": True, "occurred_at": datetime(2026, 9, 29, tzinfo=TZ)},
            {"task_id": "synthetic-A", "type": "delivered", "verified": True, "occurred_at": datetime(2026, 10, 2, tzinfo=TZ)},
            {"task_id": "synthetic-A", "type": "delivered", "verified": True, "occurred_at": datetime(2026, 10, 3, tzinfo=TZ)},
            {"task_id": "synthetic-B", "type": "delivered", "verified": False, "occurred_at": datetime(2026, 10, 4, tzinfo=TZ)},
            {"task_id": "synthetic-C", "type": "created", "verified": True, "occurred_at": datetime(2026, 10, 5, tzinfo=TZ)},
        ]
        self.assertEqual(verified_count(events, month_start(now), now, "delivered"), 1)

    def test_error_source_is_not_zero(self):
        self.assertEqual(display_metric("error", 0), "—")
        self.assertEqual(display_metric("partial", 12), "—")
        self.assertEqual(display_metric("ok", 0), "0")

    def test_backlog_is_not_delivery_count(self):
        state = {"backlog_current": 22, "verified_deliveries": 3, "history_complete": False}
        self.assertNotEqual(state["backlog_current"], state["verified_deliveries"])
        self.assertFalse(state["history_complete"])


if __name__ == "__main__":
    unittest.main()
