"""Contract tests for entirely synthetic portfolio data."""
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {p.name.removesuffix(".schema.json"): json.loads(p.read_text("utf-8")) for p in (ROOT/"schemas").glob("*.schema.json")}
REGISTRY = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in SCHEMAS.values())

def errors_for(name, obj):
    return list(Draft202012Validator(SCHEMAS[name], registry=REGISTRY).iter_errors(obj))

class Contracts(unittest.TestCase):
    def test_all_schemas_are_valid(self):
        self.assertGreaterEqual(len(SCHEMAS), 10)
        for name, s in SCHEMAS.items():
            with self.subTest(name=name): Draft202012Validator.check_schema(s)

    def test_each_synthetic_example_matches_its_schema(self):
        for path in (ROOT/"examples").glob("*.sample.json"):
            name = path.name.removesuffix(".sample.json")
            with self.subTest(name=name):
                self.assertEqual([], errors_for(name, json.loads(path.read_text("utf-8"))))

    def test_exact_task_identity_is_required_for_correlation(self):
        t = json.loads((ROOT/"examples/task.sample.json").read_text("utf-8"))
        e = json.loads((ROOT/"examples/time-entry.sample.json").read_text("utf-8"))
        self.assertEqual(t["id"], e["task_id"])
        self.assertNotEqual(t["id"], "ticket-unrelated")

    def test_time_sources_remain_separate(self):
        report = json.loads((ROOT/"examples/snapshot.sample.json").read_text("utf-8"))
        self.assertEqual(report["time_reporting"]["clickup_tracked_ms"], 5400000)
        self.assertEqual(report["time_reporting"]["auto_confirmed_seconds"], 0)
        self.assertNotIn("combined_total_ms", report["time_reporting"])

    def test_sensitive_extra_fields_cannot_enter_public_contract(self):
        t = json.loads((ROOT/"examples/task.sample.json").read_text("utf-8"))
        t["raw_payload"] = {"token": "forbidden"}
        self.assertTrue(errors_for("task", t))

    def test_delivery_requires_verified_transition(self):
        sample = json.loads((ROOT/"examples/delivery-event.sample.json").read_text("utf-8"))
        self.assertEqual([], errors_for("delivery-event", sample))
        sample["valid_transition"] = False
        self.assertTrue(errors_for("delivery-event", sample))

    def test_no_runtime_secrets_or_exports_are_versioned(self):
        blocked_ext = {".sqlite", ".db", ".pem", ".key", ".log"}
        for path in ROOT.rglob("*"):
            if path.is_file(): self.assertNotIn(path.suffix, blocked_ext, str(path))

if __name__ == "__main__": unittest.main()

