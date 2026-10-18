"""Educational idempotent payment-intent + transactional-outbox simulation.

No bank connection, settlement, MQ, or real money movement.
Python standard library only.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid


def connect(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path, timeout=10, isolation_level=None)
    con.row_factory = sqlite3.Row
    return con


def initialize(con: sqlite3.Connection) -> None:
    con.executescript("""
        CREATE TABLE IF NOT EXISTS payment_intents (
            payment_id TEXT PRIMARY KEY,
            client_id TEXT NOT NULL,
            idem_key TEXT NOT NULL,
            fingerprint TEXT NOT NULL,
            amount_minor INTEGER NOT NULL,
            currency TEXT NOT NULL,
            status TEXT NOT NULL,
            UNIQUE (client_id, idem_key)
        );
        CREATE TABLE IF NOT EXISTS outbox (
            event_id TEXT PRIMARY KEY,
            payment_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            published INTEGER NOT NULL DEFAULT 0
        );
    """)


def create_intent(con: sqlite3.Connection, client_id: str,
                  idem_key: str, amount_minor: int,
                  currency: str = "EUR") -> dict:
    """Return the same payment ID for an identical request.

    Reject reuse of the key with different payload.
    Store intent and outbox event in one local SQLite transaction.
    """
    if not client_id or not idem_key or amount_minor <= 0 or len(currency) != 3:
        raise ValueError("Invalid input")
    canonical = json.dumps(
        {"amountMinor": amount_minor, "currency": currency.upper()},
        sort_keys=True, separators=(",", ":"))
    fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    con.execute("BEGIN IMMEDIATE")
    try:
        previous = con.execute(
            "SELECT payment_id, fingerprint, status FROM payment_intents "
            "WHERE client_id=? AND idem_key=?",
            (client_id, idem_key)).fetchone()
        if previous is not None:
            if previous["fingerprint"] != fingerprint:
                raise ValueError("Conflict: same key, different payload")
            con.commit()
            return {"paymentId": previous["payment_id"],
                    "status": previous["status"], "reused": True}

        payment_id = "VIR-" + uuid.uuid4().hex[:16].upper()
        con.execute(
            "INSERT INTO payment_intents VALUES (?, ?, ?, ?, ?, ?, ?)",
            (payment_id, client_id, idem_key, fingerprint,
             amount_minor, currency.upper(), "RECEIVED"))
        event_id = "EVT-" + uuid.uuid4().hex[:16].upper()
        con.execute(
            "INSERT INTO outbox(event_id, payment_id, event_type, payload) "
            "VALUES (?, ?, ?, ?)",
            (event_id, payment_id, "PaymentRequested",
             json.dumps({"paymentId": payment_id,
                         "amountMinor": amount_minor,
                         "currency": currency.upper()})))
        con.commit()
        return {"paymentId": payment_id, "status": "RECEIVED", "reused": False}
    except BaseException:
        if con.in_transaction:
            con.rollback()
        raise


if __name__ == "__main__":
    con = connect(":memory:")
    initialize(con)
    print(create_intent(con, "CLIENT-1", "PAY-001", 50000))
    print(create_intent(con, "CLIENT-1", "PAY-001", 50000))
    print("intents:", con.execute("SELECT COUNT(*) FROM payment_intents").fetchone()[0])
    print("outbox:", con.execute("SELECT COUNT(*) FROM outbox").fetchone()[0])
