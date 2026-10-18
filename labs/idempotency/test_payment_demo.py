"""Run: python -m unittest discover -s labs/idempotency -v"""
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from payment_demo import connect, create_intent, initialize


class IdempotencyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.temp.name) / "payment.db")
        with connect(self.db) as con:
            initialize(con)

    def tearDown(self):
        self.temp.cleanup()

    def test_identical_request_reuses_intent_and_outbox(self):
        with connect(self.db) as con:
            first = create_intent(con, "c1", "k1", 50000)
            second = create_intent(con, "c1", "k1", 50000)
            self.assertFalse(first["reused"])
            self.assertTrue(second["reused"])
            self.assertEqual(first["paymentId"], second["paymentId"])
            self.assertEqual(con.execute("SELECT COUNT(*) FROM outbox").fetchone()[0], 1)

    def test_changed_amount_same_key_rejected(self):
        with connect(self.db) as con:
            create_intent(con, "c1", "k1", 50000)
            with self.assertRaises(ValueError):
                create_intent(con, "c1", "k1", 75000)
            self.assertEqual(con.execute("SELECT COUNT(*) FROM payment_intents").fetchone()[0], 1)

    def test_scope_is_per_client(self):
        with connect(self.db) as con:
            first = create_intent(con, "c1", "k1", 50000)
            second = create_intent(con, "c2", "k1", 50000)
            self.assertNotEqual(first["paymentId"], second["paymentId"])

    def test_simultaneous_requests_create_only_one_intent(self):
        def invoke(_):
            with connect(self.db) as con:
                return create_intent(con, "c1", "k1", 50000)
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(invoke, range(12)))
        self.assertEqual(len({result["paymentId"] for result in results}), 1)
        with connect(self.db) as con:
            self.assertEqual(con.execute("SELECT COUNT(*) FROM payment_intents").fetchone()[0], 1)
            self.assertEqual(con.execute("SELECT COUNT(*) FROM outbox").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
