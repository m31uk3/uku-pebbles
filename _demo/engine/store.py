"""
Storage layer — SQLite with JSON1 extension for JSONB-like queries.

Mirrors the Postgres schema from the spec but uses SQLite for zero-dependency demo.
"""

import json
import sqlite3
import os
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Optional

from .pebble import Pebble, ContextElements, LocationData, ConsentSnapshot, BookReference


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pebbles.db")


def get_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db(db_path: str = DB_PATH):
    conn = get_db(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS pebbles (
            uku_id           TEXT PRIMARY KEY,
            file_path        TEXT,
            yaml_data        TEXT NOT NULL,   -- JSON blob of all YAML frontmatter
            body_text        TEXT,
            indexed_at       TEXT DEFAULT (datetime('now')),

            -- Implicit behavioral signals
            access_count     INTEGER DEFAULT 0,
            update_count     INTEGER DEFAULT 0,
            reference_count  INTEGER DEFAULT 0,
            last_accessed_at TEXT,
            last_updated_at  TEXT,

            -- Agent-computed effective weight
            effective_weight REAL
        );

        CREATE TABLE IF NOT EXISTS sharing (
            uku_id       TEXT NOT NULL,
            shared_with  TEXT NOT NULL,  -- person or group identifier
            share_type   TEXT NOT NULL,  -- 'person' or 'group' or 'org'
            shared_at    TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (uku_id, shared_with)
        );
    """)
    conn.commit()
    conn.close()


def store_pebble(pebble: Pebble, db_path: str = DB_PATH):
    """Insert or replace a pebble in the index."""
    conn = get_db(db_path)
    yaml_dict = pebble.to_yaml_dict()
    conn.execute(
        """INSERT OR REPLACE INTO pebbles
           (uku_id, yaml_data, body_text, effective_weight)
           VALUES (?, ?, ?, ?)""",
        (
            pebble.uku_id,
            json.dumps(yaml_dict),
            pebble.body,
            pebble.weight,
        ),
    )

    # Store sharing records
    for person in pebble.shared_with:
        conn.execute(
            "INSERT OR IGNORE INTO sharing (uku_id, shared_with, share_type) VALUES (?, ?, 'person')",
            (pebble.uku_id, person),
        )
    for group in pebble.shared_with_groups:
        conn.execute(
            "INSERT OR IGNORE INTO sharing (uku_id, shared_with, share_type) VALUES (?, ?, 'group')",
            (pebble.uku_id, group),
        )

    conn.commit()
    conn.close()


def get_pebble(uku_id: str, db_path: str = DB_PATH) -> Optional[dict]:
    """Retrieve a single pebble and increment access count."""
    conn = get_db(db_path)
    row = conn.execute("SELECT * FROM pebbles WHERE uku_id = ?", (uku_id,)).fetchone()
    if not row:
        conn.close()
        return None

    conn.execute(
        "UPDATE pebbles SET access_count = access_count + 1, last_accessed_at = ? WHERE uku_id = ?",
        (datetime.now(timezone.utc).isoformat(), uku_id),
    )
    conn.commit()

    result = _row_to_dict(row)
    conn.close()
    return result


def get_all_pebbles(db_path: str = DB_PATH) -> list[dict]:
    conn = get_db(db_path)
    rows = conn.execute("SELECT * FROM pebbles ORDER BY json_extract(yaml_data, '$.created_at') DESC").fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def search_pebbles(filters: dict, db_path: str = DB_PATH) -> list[dict]:
    """
    Search pebbles by YAML attribute filters.

    filters is a dict of JSON paths → values, e.g.:
      {"$.location.name": "Blue Bottle Coffee", "$.tags": "stoicism"}

    Supports:
      - Exact match on scalar values
      - Substring match (LIKE) for string values
      - Array containment for tags
      - Date range with $.created_at__gte / $.created_at__lte
    """
    conn = get_db(db_path)
    conditions = []
    params = []

    for path, value in filters.items():
        if path.endswith("__gte"):
            real_path = path.replace("__gte", "")
            # Use string comparison for dates, numeric for weights
            if isinstance(value, (int, float)):
                conditions.append(f"CAST(json_extract(yaml_data, ?) AS REAL) >= ?")
            else:
                conditions.append(f"json_extract(yaml_data, ?) >= ?")
            params.extend([real_path, value])
        elif path.endswith("__lte"):
            real_path = path.replace("__lte", "")
            if isinstance(value, (int, float)):
                conditions.append(f"CAST(json_extract(yaml_data, ?) AS REAL) <= ?")
            else:
                conditions.append(f"json_extract(yaml_data, ?) <= ?")
            params.extend([real_path, value])
        elif path == "$.tags":
            # Check if value is in the tags array
            conditions.append(f"EXISTS (SELECT 1 FROM json_each(json_extract(yaml_data, '$.tags')) WHERE value LIKE ?)")
            params.append(f"%{value}%")
        elif path == "$.people":
            conditions.append(f"EXISTS (SELECT 1 FROM json_each(json_extract(yaml_data, '$.people')) WHERE value LIKE ?)")
            params.append(f"%{value}%")
        elif isinstance(value, str):
            conditions.append(f"json_extract(yaml_data, ?) LIKE ?")
            params.extend([path, f"%{value}%"])
        else:
            conditions.append(f"json_extract(yaml_data, ?) = ?")
            params.extend([path, value])

    where = " AND ".join(conditions) if conditions else "1=1"
    query = f"SELECT * FROM pebbles WHERE {where} ORDER BY json_extract(yaml_data, '$.created_at') DESC"

    rows = conn.execute(query, params).fetchall()

    # If strict AND returns nothing, try relaxed OR matching (ranked by match count)
    if not rows and len(conditions) > 1:
        or_where = " OR ".join(f"({c})" for c in conditions)
        score_expr = " + ".join(f"(CASE WHEN {c} THEN 1 ELSE 0 END)" for c in conditions)
        # Each condition uses its own params, so we need params twice: once for WHERE, once for ORDER BY
        relaxed_query = f"""
            SELECT *
            FROM pebbles
            WHERE {or_where}
            ORDER BY ({score_expr}) DESC, json_extract(yaml_data, '$.created_at') DESC
        """
        rows = conn.execute(relaxed_query, params + params).fetchall()

    conn.close()
    return [_row_to_dict(r) for r in rows]


def find_red_strings(uku_id: str, db_path: str = DB_PATH) -> list[dict]:
    """
    Find all pebbles connected to the given pebble via red strings
    (any matching YAML key-value pair).

    Returns list of {pebble: dict, connections: [{"path": ..., "value": ...}]}
    """
    source = get_pebble(uku_id, db_path)
    if not source:
        return []

    all_pebbles = get_all_pebbles(db_path)
    source_yaml = source["yaml_data"]
    results = []

    for other in all_pebbles:
        if other["uku_id"] == uku_id:
            continue

        connections = _find_matching_attrs(source_yaml, other["yaml_data"])
        if connections:
            # Update reference count
            conn = get_db(db_path)
            conn.execute(
                "UPDATE pebbles SET reference_count = reference_count + 1 WHERE uku_id = ?",
                (other["uku_id"],),
            )
            conn.commit()
            conn.close()

            results.append({
                "pebble": other,
                "connections": connections,
                "strength": len(connections),
            })

    results.sort(key=lambda x: x["strength"], reverse=True)
    return results


def _find_matching_attrs(a: dict, b: dict, prefix: str = "") -> list[dict]:
    """Recursively find matching key-value pairs between two YAML dicts."""
    matches = []
    skip_keys = {"uku_id", "created_at", "content_hash", "status"}

    for key in a:
        if key in skip_keys:
            continue
        path = f"{prefix}.{key}" if prefix else key

        if key not in b:
            continue

        val_a = a[key]
        val_b = b[key]

        if isinstance(val_a, dict) and isinstance(val_b, dict):
            matches.extend(_find_matching_attrs(val_a, val_b, path))
        elif isinstance(val_a, list) and isinstance(val_b, list):
            shared = set(str(x) for x in val_a) & set(str(x) for x in val_b)
            for s in shared:
                matches.append({"path": path, "value": s})
        elif val_a == val_b and val_a is not None:
            matches.append({"path": path, "value": str(val_a)})

    return matches


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["yaml_data"] = json.loads(d["yaml_data"])
    d["uku_id"] = d["yaml_data"].get("uku_id", d.get("uku_id"))
    return d
