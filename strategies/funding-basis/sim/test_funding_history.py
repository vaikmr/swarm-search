import io
import json
import unittest
from unittest.mock import patch
from fetch_funding_history import collect


class FundingCollectionTests(unittest.TestCase):
    def test_pagination_and_empty_termination(self):
        responses = [
            [{"coin": "ETH", "time": 10, "fundingRate": "0.001"}],
            [{"coin": "ETH", "time": 20, "fundingRate": "-0.001"}],
            [],
        ]
        with patch("urllib.request.urlopen", side_effect=[io.BytesIO(json.dumps(r).encode()) for r in responses]) as opening, patch("time.sleep"):
            rows, pages = collect("ETH", 1, 25)
        self.assertEqual([r["time"] for r in rows], [10, 20])
        self.assertEqual(len(pages), 3)
        self.assertEqual(json.loads(opening.call_args_list[1].args[0].data)["startTime"], 11)

    def test_wrong_coin_fails_closed(self):
        response = [{"coin": "BTC", "time": 10, "fundingRate": "0.001"}]
        with patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps(response).encode())), self.assertRaises(ValueError):
            collect("ETH", 1, 25)

    def test_repeated_page_does_not_loop_forever(self):
        response = [{"coin": "ETH", "time": 10, "fundingRate": "0.001"}]
        with patch("urllib.request.urlopen", side_effect=[io.BytesIO(json.dumps(response).encode()) for _ in range(2)]), patch("time.sleep"), self.assertRaises(ValueError):
            collect("ETH", 1, 25)


if __name__ == "__main__":
    unittest.main()
