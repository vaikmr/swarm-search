import json
from pathlib import Path
import tempfile
import time
import unittest
from research_tools.paper_observer import (
    append_record, collect_once, executable_quote, mark_to_market,
    load_records, normalize_hl_book, observation_gate,
)
from research_tools.yield_data import DataError, iso_now


def payload():
    return {"coin": "BTC", "time": int(time.time()*1000),
            "levels": [[{"px": "99", "sz": "1"}],
                       [{"px": "101", "sz": "1"}, {"px": "102", "sz": "2"}]]}


class PaperTests(unittest.TestCase):
    def test_worst_price_not_optimistic_vwap(self):
        book = normalize_hl_book(payload())
        quote = executable_quote(book, "buy", 2, time.time(), 5, 10, 10, 200)
        self.assertAlmostEqual(quote["estimated_price"], 102*1.001)
        self.assertAlmostEqual(quote["fee_usd"], 2*102*1.001*.001)

    def test_missing_depth_or_stale_fails(self):
        book = normalize_hl_book(payload())
        for qty, now in [(4, time.time()), (1, time.time()+20)]:
            with self.assertRaises(DataError):
                executable_quote(book, "buy", qty, now, 5, 10, 10, 200)
        book["source_time_s"] = None
        with self.assertRaises(DataError):
            executable_quote(book, "buy", 1, time.time(), 5, 10, 10, 200)

    def test_crossed_or_unsorted_fails(self):
        for data in [dict(payload(), levels=[[{"px": "103", "sz": "1"}],
                                             [{"px": "102", "sz": "1"}]]),
                     dict(payload(), levels=[[{"px": "99", "sz": "1"}],
                                             [{"px": "102", "sz": "1"},
                                              {"px": "101", "sz": "1"}]])]:
            with self.assertRaises(DataError):
                normalize_hl_book(data)

    def test_default_observer_never_fills(self):
        class Stub:
            def book(self, coin):
                return {"payload": payload()}
            def coinbase_btc_book(self):
                return {"payload": {"bids": [["99", "1", 1]], "asks": [["101", "1", 1]]}}
        row = collect_once(Stub())
        self.assertEqual(row["decision"], "REJECT_NO_PAPER_FILL")
        self.assertEqual(row["simulated_fills"], [])
        self.assertIn("spot_book_missing_source_timestamp", row["rejection_reasons"])

    def test_failure_is_recorded_not_zero_return(self):
        class Stub:
            def book(self, coin):
                raise TimeoutError("body must not appear")
            def coinbase_btc_book(self):
                raise OSError("body must not appear")
        row = collect_once(Stub())
        self.assertEqual(len(row["failures"]), 2)
        self.assertNotIn("body must not appear", json.dumps(row))

    def test_append_chain_and_wall_clock_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"test.jsonl"
            row = {"finished_at": iso_now(), "strategy_version": None,
                   "simulated_fills": [], "failures": []}
            a = append_record(path, row)
            b = append_record(path, row)
            self.assertEqual(b["previous_record_sha256"], a["record_sha256"])
            self.assertEqual(len(load_records(path)), 2)
            self.assertFalse(observation_gate([a])["eligible_for_T3_review"])
            self.assertIn("less_than_seven_elapsed_days", observation_gate([a])["reasons"])
            path.write_text(path.read_text().replace('"simulated_fills": []',
                                                    '"simulated_fills": [{}]', 1))
            with self.assertRaises(DataError):
                load_records(path)

    def test_mtm_uses_bid_for_long_ask_for_short(self):
        self.assertAlmostEqual(mark_to_market(1, 1, 99, 101, 3, 1, 2), 0)


if __name__ == "__main__":
    unittest.main()
