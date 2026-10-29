"""Synthetic offline tests for RPC probe guardrails; no network calls."""

import unittest
from unittest.mock import patch

from research_tools.replay_rpc_probe import ALLOWED_METHODS, MAX_READS, ProbeClient
from research_tools.replay_drpc_probe import header_valid, hex_word


class ProbeTests(unittest.TestCase):
    def test_no_state_changing_method_is_allowlisted(self):
        for method in ("eth_sendTransaction", "eth_sendRawTransaction", "personal_unlockAccount",
                       "anvil_setStorageAt", "anvil_impersonateAccount", "evm_mine"):
            self.assertNotIn(method, ALLOWED_METHODS)
            with self.assertRaises(ValueError):
                ProbeClient().call(method, [])

    @patch("research_tools.replay_rpc_probe.curl_json")
    def test_hard_budget_counts_each_read_and_no_retry(self, transport):
        transport.return_value = {"http_status": 403, "body": None}
        client = ProbeClient()
        for _ in range(MAX_READS):
            self.assertIsNone(client.call("eth_chainId", []))
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            client.call("eth_chainId", [])
        self.assertEqual(transport.call_count, MAX_READS)
        self.assertEqual(len(client.records), MAX_READS)

    @patch("research_tools.replay_rpc_probe.curl_json")
    def test_wrong_response_id_is_not_success(self, transport):
        transport.return_value = {"http_status": 200, "body": {"id": 999, "result": "0x1"}}
        self.assertIsNone(ProbeClient().call("eth_chainId", []))

    @patch("research_tools.replay_rpc_probe.curl_json")
    def test_rpc_error_is_preserved_and_not_success(self, transport):
        transport.return_value = {"http_status": 200,
                                  "body": {"id": 1, "error": {"code": -32000, "message": "missing trie"}}}
        client = ProbeClient()
        self.assertIsNone(client.call("eth_getCode", []))
        self.assertEqual(client.records[0]["body"]["error"]["code"], -32000)

    @patch("research_tools.replay_rpc_probe.curl_json", side_effect=OSError)
    def test_transport_failure_consumes_budget_and_does_not_retry(self, transport):
        client = ProbeClient()
        self.assertIsNone(client.call("eth_chainId", []))
        self.assertEqual(len(client.records), 1)
        self.assertEqual(transport.call_count, 1)

    @patch("research_tools.replay_rpc_probe.curl_json")
    def test_separate_eight_read_budget_is_enforced(self, transport):
        transport.return_value = {"http_status": 403, "body": None}
        client = ProbeClient(endpoint="https://eth.drpc.org", max_reads=8)
        for _ in range(8):
            client.call("eth_chainId", [])
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            client.call("eth_chainId", [])
        self.assertEqual(transport.call_count, 8)

    def test_unapproved_endpoint_or_budget_rejected(self):
        for arguments in ({"endpoint": "https://example.com/private-token"},
                          {"max_reads": 13}, {"max_reads": True}):
            with self.assertRaises(ValueError):
                ProbeClient(**arguments)

    def test_empty_or_substituted_headers_and_state_rejected(self):
        self.assertFalse(header_valid(None, 1))
        self.assertFalse(header_valid({"number": "0x2", "timestamp": "0x1",
                                      "hash": "0x" + "1" * 64}, 1))
        header = {"number": "0x1", "timestamp": "0x1", "hash": "0x" + "1" * 64}
        self.assertTrue(header_valid(header, 1))
        self.assertFalse(header_valid(header, 1, "0x" + "2" * 64))
        self.assertFalse(hex_word("0x"))
        self.assertFalse(hex_word("0x" + "z" * 64))


if __name__ == "__main__":
    unittest.main()
