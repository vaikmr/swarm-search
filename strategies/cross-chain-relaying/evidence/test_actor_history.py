"""All fixtures in this file are synthetic and are not market observations."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "history", Path(__file__).with_name("probe_actor_history.py")
)
history = importlib.util.module_from_spec(spec)
spec.loader.exec_module(history)


def word(value):
    if isinstance(value, str):
        return value.removeprefix("0x").rjust(64, "0")
    return f"{value:064x}"


def refund_log(amount=123, deferred=0):
    data = [0, 192, history.TOKENS["USDC"], 256, deferred, history.ACTOR,
            1, amount, 1, history.ACTOR]
    return {
        "address": history.POOL,
        "topics": [history.REFUND, "0xa", "0x1", "0x2"],
        "data": "0x" + "".join(word(x) for x in data),
        "transactionHash": "synthetic", "logIndex": "0x0", "blockNumber": "0x1",
    }


class HistoryTests(unittest.TestCase):
    def test_pagination_covers_exact_nonoverlapping_window(self):
        pages = history.ranges(history.OPEN_BLOCK + 1, history.CLOSE_BLOCK)
        self.assertEqual(len(pages), 61)
        self.assertEqual(sum(hi - lo + 1 for lo, hi in pages), 604800)
        self.assertEqual(pages[0][0], history.OPEN_BLOCK + 1)
        self.assertEqual(pages[-1][1], history.CLOSE_BLOCK)
        self.assertTrue(all(a[1] + 1 == b[0] for a, b in zip(pages, pages[1:])))

    def test_refund_allocation_is_not_certified_cash(self):
        row = history.decode_refund(refund_log())
        self.assertEqual(row["allocated_amount_raw"], "123")
        self.assertFalse(row["cash_receipt_independently_verified"])
        row = history.decode_refund(refund_log(deferred=1))
        self.assertTrue(row["any_batch_refunds_deferred"])

    def test_bad_offsets_and_flags_are_rejected(self):
        log = refund_log()
        w = history.words(log["data"])
        for index, value in [(1, 1), (1, 100000), (4, 2), (6, 1001)]:
            changed = w.copy()
            changed[index] = word(value)
            log["data"] = "0x" + "".join(changed)
            with self.assertRaises(ValueError):
                history.decode_refund(log)

    def test_wrong_chain_or_actor_layout_is_rejected(self):
        log = refund_log()
        log["topics"][1] = "0x1"
        with self.assertRaises(ValueError):
            history.decode_refund(log)
        with self.assertRaises(ValueError):
            history.evm_address("f" * 64)

    def test_failed_receipt_does_not_confirm_refund(self):
        self.assertEqual(history.confirmed_transfers({"status": "0x0"}), [])

    def test_confirm_only_pool_to_actor_transfer(self):
        transfer = {
            "address": history.TOKENS["USDC"], "logIndex": "0x2",
            "topics": [history.TRANSFER, history.address_word(history.POOL),
                       history.address_word(history.ACTOR)],
            "data": "0x" + word(123),
        }
        receipt = {"status": "0x1", "transactionHash": "synthetic", "logs": [transfer]}
        self.assertEqual(history.confirmed_transfers(receipt)[0]["amount_raw"], "123")
        transfer["topics"][1] = history.address_word(history.ACTOR)
        self.assertEqual(history.confirmed_transfers(receipt), [])

    def test_probe_rejects_nonread_methods_before_network(self):
        with tempfile.TemporaryDirectory() as directory:
            probe = history.PublicProbe(directory)
            with self.assertRaises(ValueError):
                probe.request("bad", "not-a-read-method", [])
            with self.assertRaises(ValueError):
                probe.request("bad-call", "eth_call", [{"data": "0xdeadbeef"}])
            self.assertEqual(probe.calls, 0)

    def test_current_fill_layout_uses_updated_not_quoted_amount(self):
        data = [history.TOKENS["USDC"], history.TOKENS["USDC"],
                100, 99, 1, 0, 0, 0, 0, 0, 0, 0, 0, 98, 0]
        log = {
            "address": history.POOL,
            "topics": [history.FILL, "0x1", "0x2", history.address_word(history.ACTOR)],
            "data": "0x" + "".join(word(x) for x in data),
            "transactionHash": "synthetic", "logIndex": "0x0", "blockNumber": "0x1",
        }
        row = history.decode_fill(log)
        self.assertEqual(row["original_output_amount_raw"], "99")
        self.assertEqual(row["actual_output_amount_raw"], "98")


if __name__ == "__main__":
    unittest.main()
