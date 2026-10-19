"""Public-safe regression tests for the JSON transport contract.

Only synthetic content; no production tokens, endpoints or customer records.
"""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "chat-transport-response.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)


def make_response(kind="answer"):
    return {
        "channel": "ti-copiloto-json-v2",
        "request_id": "1234567890abcdef1234567890abcdef",
        "kind": kind,
        "answer": "Resumo fictício de teste. Nenhum dado real foi consultado.",
        "sources": [
            {
                "id": "task:synthetic-001",
                "title": "Tarefa sintética",
                "url": "https://example.org/fake/task",
            }
        ],
        "model_ok": kind == "answer",
    }


class TestChatTransportContract(unittest.TestCase):
    def assert_valid(self, payload):
        VALIDATOR.validate(payload)

    def assert_invalid(self, payload):
        self.assertTrue(list(VALIDATOR.iter_errors(payload)))

    def test_answer_includes_nonce_and_sources(self):
        self.assert_valid(make_response())

    def test_auth_error_is_structured_json(self):
        payload = make_response("auth")
        payload["sources"] = []
        payload["model_ok"] = False
        self.assert_valid(payload)

    def test_heartbeat_reply_uses_refresh_kind(self):
        payload = make_response("refresh")
        payload["sources"] = []
        self.assert_valid(payload)

    def test_all_error_states_accepted(self):
        for kind in ("error", "limit"):
            with self.subTest(kind=kind):
                self.assert_valid(make_response(kind))

    def test_wrong_channel_is_rejected(self):
        payload = make_response()
        payload["channel"] = "legacy-iframe-v1"
        self.assert_invalid(payload)

    def test_request_id_is_required_and_must_be_valid(self):
        payload = make_response()
        del payload["request_id"]
        self.assert_invalid(payload)
        payload["request_id"] = "short"
        self.assert_invalid(payload)

    def test_sources_must_use_https(self):
        payload = make_response()
        payload["sources"][0]["url"] = "http://example.org/test"
        self.assert_invalid(payload)

    def test_answer_cannot_exceed_limit(self):
        payload = make_response()
        payload["answer"] = "x" * 2401
        self.assert_invalid(payload)

    def test_unexpected_fields_rejected(self):
        payload = make_response()
        payload["access_token"] = "never include bearer tokens in responses"
        self.assert_invalid(payload)


if __name__ == "__main__":
    unittest.main()
