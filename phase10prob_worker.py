import os
import sqlite3
from datetime import datetime, timezone
import time

import phase10config
import phase10probability
import phase10typelogic

MC_SERVICE_TRIALS = phase10config.CONFIG["MC_SERVICE_TRIALS"]
DB_PATH = os.path.join(os.path.dirname(__file__), "phase10_probs.sqlite")


def get_db_connection():
    return sqlite3.connect(DB_PATH)

def db_get_phase_record(phase_key_str):
    """
    Return (probability, trials) for a given phase_key string,
    or (None, None) if not present.
    """
    conn = get_db_connection()
    try:
        cur = conn.execute(
            "SELECT probability, trials "
            "FROM phase_probability "
            "WHERE phase_key = ?",
            (phase_key_str,)
        )
        row = cur.fetchone()
        if row is None:
            return None, None
        return row[0], row[1]
    finally:
        conn.close()

def db_insert_placeholder(selection):
    """
    Ensure a placeholder row exists for this phase with:
      probability = 0.0, trials = 0
    Also ensures phase_part rows exist.

    This just reuses insert_phase_if_missing, which already
    does exactly that.
    """
    insert_phase_if_missing(selection)

def db_upsert_phase(selection, probability, trials):
    """
    Ensure a row exists for this phase, then set its
    probability and trials to the given values.

    We do NOT touch phase_part here; insert_phase_if_missing
    already handled that on generation.
    """
    phase_key_tuple = phase10probability._phase_key(selection)
    phase_key_str = repr(phase_key_tuple)

    conn = get_db_connection()
    try:
        # Make sure the phase row exists
        conn.execute(
            """
            INSERT OR IGNORE INTO phase_probability
                (phase_key, probability, trials, last_updated)
            VALUES (?, ?, ?, ?)
            """,
            (phase_key_str, 0.0, 0, datetime.now(timezone.utc).isoformat())
        )

        # Now update it with the new quick-MC values
        conn.execute(
            """
            UPDATE phase_probability
               SET probability = ?,
                   trials      = ?,
                   last_updated = ?
             WHERE phase_key   = ?
            """,
            (probability, trials, datetime.now(timezone.utc).isoformat(), phase_key_str)
        )

        conn.commit()
    finally:
        conn.close()

def fetch_phases_needing_work(conn):
    """
    Get phases where trials < MC_SERVICE_TRIALS.
    Returns list of (phase_key_str, probability, trials).
    """
    cur = conn.execute(
        "SELECT phase_key, probability, trials "
        "FROM phase_probability "
        "WHERE trials < ?",
        (MC_SERVICE_TRIALS,)
    )
    return cur.fetchall()


def load_phase_parts(conn, phase_key_str):
    """
    Rebuild a selection (list of PhasePart) from phase_part table.
    """
    cur = conn.execute(
        "SELECT part_index, part_str, part_type "
        "FROM phase_part "
        "WHERE phase_key = ? "
        "ORDER BY part_index",
        (phase_key_str,)
    )
    rows = cur.fetchall()

    selection = []
    for part_index, part_str, part_type in rows:
        p = phase10typelogic.PhasePart()
        p.str = part_str
        p.type = part_type
        selection.append(p)
    return selection


def update_phase_probability(conn, phase_key_str, probability, trials):
    conn.execute(
        """
        UPDATE phase_probability
           SET probability = ?,
               trials      = ?,
               last_updated = ?
         WHERE phase_key   = ?
        """,
        (probability, trials, datetime.now(timezone.utc).isoformat(), phase_key_str)
    )
    conn.commit()

def insert_phase_if_missing(selection):
    phase_key_tuple = phase10probability._phase_key(selection)
    phase_key_str = repr(phase_key_tuple)

    conn = get_db_connection()
    try:
        cur = conn.execute(
            "SELECT 1 FROM phase_probability WHERE phase_key = ?",
            (phase_key_str,)
        )
        row = cur.fetchone()
        if row is not None:
            return  # already present

        now = datetime.now(timezone.utc).isoformat()

        conn.execute(
            "INSERT INTO phase_probability (phase_key, probability, trials, last_updated) "
            "VALUES (?, ?, ?, ?)",
            (phase_key_str, 0.0, 0, now)
        )

        conn.execute(
            "DELETE FROM phase_part WHERE phase_key = ?",
            (phase_key_str,)
        )

        for idx, part in enumerate(selection):
            conn.execute(
                "INSERT INTO phase_part (phase_key, part_index, part_str, part_type) "
                "VALUES (?, ?, ?, ?)",
                (
                    phase_key_str,
                    idx,
                    getattr(part, "str", ""),
                    getattr(part, "type", None),
                )
            )

        conn.commit()
    finally:
        conn.close()

def run_once():
    conn = get_db_connection()
    try:
        rows = fetch_phases_needing_work(conn)
        if not rows:
            # print("No phases needing work.")
            return

        print(f"Found {len(rows)} phase(s) needing work.")
        for phase_key_str, old_prob, old_trials in rows:
            print(f"Processing phase_key={phase_key_str}, old_trials={old_trials}")
            selection = load_phase_parts(conn, phase_key_str)
            if not selection:
                print("  No parts found; skipping.")
                continue

            prob = phase10probability.estimate_phase_prob_mc(
                selection,
                trials=MC_SERVICE_TRIALS,
                seed=1337,
            )

            update_phase_probability(conn, phase_key_str, prob, MC_SERVICE_TRIALS)
            print(f"  Updated prob={prob:.6f}, trials={MC_SERVICE_TRIALS}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        MC_SERVICE_TRIALS = phase10config.CONFIG["MC_SERVICE_TRIALS"]
        run_once()
        worker_interval = phase10config.CONFIG["MC_WORKER_INTERVAL_SECONDS"]
        time.sleep(worker_interval)