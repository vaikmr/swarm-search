"""Synthetic offline-audit tests; no market observations or networking."""

import ast
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).with_name("audit_saved_history.py")
spec = importlib.util.spec_from_file_location("offline", path)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def word(value):
    return value.to_bytes(32, "big")


class OfflineAuditTests(unittest.TestCase):
    def test_raw_hash_and_byte_count_are_both_checked(self):
        data = b'{"result": 1}'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "raw.json"
            path.write_bytes(data)
            entry = {"name": "synthetic", "response_sha256": audit.sha(data),
                     "response_bytes": len(data)}
            checked, body = audit.check_file(path, entry)
            self.assertTrue(checked["sha256_matches"] and checked["bytes_match"])
            self.assertEqual(body["result"], 1)
            entry["response_bytes"] += 1
            self.assertFalse(audit.check_file(path, entry)[0]["bytes_match"])
            entry["response_sha256"] = "incorrect"
            self.assertFalse(audit.check_file(path, entry)[0]["sha256_matches"])

    def test_page_gaps_overlaps_oversize_are_not_complete(self):
        self.assertTrue(audit.check_coverage([(1, 5), (6, 10)], 1, 10))
        for pages in [[(1, 4), (6, 10)], [(1, 6), (6, 10)], [(1, 10001)], []]:
            self.assertFalse(audit.check_coverage(pages, 1, 10))

    def test_independent_refund_decoder_does_not_credit_other_address(self):
        actor = "0x" + "a" * 40
        other = int("b" * 40, 16)
        data = b"".join(word(x) for x in [
            0, 192, 1, 288, 0, 2, 2, 12, 34, 2, other, int(actor, 16),
        ])
        token, amount, deferred = audit.refund_allocation({"data": "0x" + data.hex()}, actor)
        self.assertEqual(token, "0x" + "0" * 39 + "1")
        self.assertEqual(amount, 34)
        self.assertFalse(deferred)

    def test_byte_decoder_rejects_bad_offsets_and_addresses(self):
        with self.assertRaises(ValueError):
            audit.uint_at(b"\0" * 32, 1)
        with self.assertRaises(ValueError):
            audit.uint_at(b"\0" * 32, 32)
        with self.assertRaises(ValueError):
            audit.address_at(b"\xff" * 32, 0)

    def test_canonical_object_hash_is_not_raw_http_hash(self):
        obj = {"b": 2, "a": 1}
        self.assertEqual(audit.fingerprint(obj), audit.fingerprint({"a": 1, "b": 2}))
        self.assertNotEqual(audit.fingerprint(obj), audit.sha(json.dumps(obj).encode()))

    def test_imports_have_no_network_or_process_execution(self):
        imports = set()
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split(".")[0])
        self.assertEqual(imports, {"argparse", "collections", "hashlib", "json", "pathlib"})


if __name__ == "__main__":
    unittest.main()
