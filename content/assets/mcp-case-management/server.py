"""CasePal Lab 5 mock Case Management System MCP server.

The server exposes four synthetic case-management tools over MCP:
``create_case``, ``get_case``, ``update_case_status``, and ``list_open_cases``.
It is intentionally small, no-auth, and workshop-only. Use Foundry's MCP approval
settings so create/update calls require human confirmation before write.
"""
from __future__ import annotations

import datetime as dt
import os
import sqlite3
from pathlib import Path
from threading import Lock
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "casepal-case-management",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    stateless_http=True,
)

VALID_STATUSES = {"open", "awaiting_info", "escalated", "closed"}
START_SEQUENCE = 1188
_lock = Lock()
_memory_cases: dict[str, dict[str, Any]] = {}
_memory_next = START_SEQUENCE
_db_path = os.environ.get("MCP_PERSIST_PATH")


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _connect() -> sqlite3.Connection | None:
    if not _db_path:
        return None
    path = Path(_db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            priority TEXT NOT NULL,
            follow_up_owner TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT ''
        )"""
    )
    conn.commit()
    return conn


def _row_to_case(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "case_id": row["case_id"],
        "report_id": row["report_id"],
        "priority": row["priority"],
        "follow_up_owner": row["follow_up_owner"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "notes": [n for n in row["notes"].split("\n") if n],
    }


def _next_case_id(conn: sqlite3.Connection | None) -> str:
    global _memory_next
    if conn is None:
        case_id = f"CMS-2026-{_memory_next}"
        _memory_next += 1
        return case_id
    row = conn.execute("SELECT case_id FROM cases ORDER BY CAST(substr(case_id, 10) AS INTEGER) DESC LIMIT 1").fetchone()
    next_num = START_SEQUENCE if row is None else int(row["case_id"].rsplit("-", 1)[1]) + 1
    return f"CMS-2026-{next_num}"


@mcp.tool()
def create_case(report_id: str, priority: str, follow_up_owner: str) -> dict[str, str]:
    """Create a synthetic case-management record after reviewer approval."""
    if not report_id or not follow_up_owner:
        raise ValueError("report_id and follow_up_owner are required")
    with _lock:
        conn = _connect()
        created_at = _now_iso()
        case_id = _next_case_id(conn)
        record = {
            "case_id": case_id,
            "report_id": report_id,
            "priority": priority,
            "follow_up_owner": follow_up_owner,
            "status": "open",
            "created_at": created_at,
            "updated_at": created_at,
            "notes": [],
        }
        if conn is None:
            _memory_cases[case_id] = record
        else:
            conn.execute(
                "INSERT INTO cases(case_id, report_id, priority, follow_up_owner, status, created_at, updated_at, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (case_id, report_id, priority, follow_up_owner, "open", created_at, created_at, ""),
            )
            conn.commit()
            conn.close()
        return {"case_id": case_id, "created_at": created_at}


@mcp.tool()
def get_case(case_id: str) -> dict[str, Any]:
    """Read a synthetic case-management record by ID."""
    conn = _connect()
    if conn is None:
        if case_id not in _memory_cases:
            raise KeyError(f"Case not found: {case_id}")
        return _memory_cases[case_id]
    row = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
    conn.close()
    if row is None:
        raise KeyError(f"Case not found: {case_id}")
    return _row_to_case(row)


@mcp.tool()
def update_case_status(case_id: str, status: str, note: str) -> dict[str, Any]:
    """Transition a case to open, awaiting_info, escalated, or closed after approval."""
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")
    with _lock:
        record = get_case(case_id)
        updated_at = _now_iso()
        notes = list(record.get("notes", []))
        if note:
            notes.append(f"{updated_at} {status}: {note}")
        conn = _connect()
        if conn is None:
            record.update({"status": status, "updated_at": updated_at, "notes": notes})
            _memory_cases[case_id] = record
            return record
        conn.execute(
            "UPDATE cases SET status = ?, updated_at = ?, notes = ? WHERE case_id = ?",
            (status, updated_at, "\n".join(notes), case_id),
        )
        conn.commit()
        conn.close()
        return get_case(case_id)


@mcp.tool()
def list_open_cases(owner: str) -> list[dict[str, Any]]:
    """List open cases assigned to the specified follow-up owner."""
    conn = _connect()
    if conn is None:
        return [c for c in _memory_cases.values() if c["status"] == "open" and c["follow_up_owner"] == owner]
    rows = conn.execute(
        "SELECT * FROM cases WHERE status = 'open' AND follow_up_owner = ? ORDER BY created_at",
        (owner,),
    ).fetchall()
    conn.close()
    return [_row_to_case(r) for r in rows]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
