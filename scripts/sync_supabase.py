#!/usr/bin/env python3
"""
Sync study progress to Supabase study_progress table.

Usage:
  python3 scripts/sync_supabase.py              # full sync (DSA + daily plans)
  python3 scripts/sync_supabase.py --status     # show current state
  python3 scripts/sync_supabase.py --dsa-only    # DSA tracker rows only
  python3 scripts/sync_supabase.py --plan DATE   # seed one daily plan
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# This repo is public. The key grants read/write access to study_progress, so it
# is supplied at runtime rather than committed.
#   export SUPABASE_URL="https://<project>.supabase.co/rest/v1"
#   export SUPABASE_KEY="sb_publishable_..."
SUPABASE_REST_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
TABLE = "study_progress"
USER = "sbaskar"


def require_credentials() -> None:
    missing = [n for n, v in (("SUPABASE_URL", SUPABASE_REST_URL),
                              ("SUPABASE_KEY", SUPABASE_KEY)) if not v]
    if missing:
        sys.exit(f"Missing environment variable(s): {', '.join(missing)}. "
                 "See scripts/README.md.")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_row(topic_id: str, doc_id: str, row_id: str, field: str, value) -> dict:
    key = f"{USER}::{topic_id}::{doc_id}::{row_id}::{field}"
    return {
        "id": key,
        "user_id": USER,
        "topic_id": topic_id,
        "doc_id": doc_id,
        "row_id": row_id,
        "field": field,
        "value": value,
        "updated_at": now_iso(),
    }


def dsa_solved(row_id: str, confidence: str = "3") -> list[dict]:
    return [
        make_row("dsa-patterns", "roadmap", row_id, "attempted", True),
        make_row("dsa-patterns", "roadmap", row_id, "solved", True),
        make_row("dsa-patterns", "roadmap", row_id, "confidence (1-5)", confidence),
    ]


def daily_task(
    plan_date: str,
    task_id: str,
    track: str,
    title: str,
    description: str,
    *,
    link: str = "",
    minutes: int = 0,
    status: str = "pending",
    priority: str = "high",
    source_date: str | None = None,
) -> dict:
    return make_row(
        "daily-plan",
        plan_date,
        task_id,
        "task",
        {
            "track": track,
            "title": title,
            "description": description,
            "resource_link": link,
            "estimated_min": minutes,
            "status": status,
            "priority": priority,
            "plan_date": plan_date,
            "source_date": source_date or plan_date,
        },
    )


def picnic_row(field: str, value) -> dict:
    return make_row("picnic-prep", "interview", "main", field, value)


def build_sync_payload() -> list[dict]:
    rows: list[dict] = []

    # Catch-up DSA rows missing from Supabase (Aug 24–25 session)
    dsa_updates = {
        "20": ("3",),   # LC #239 Sliding Window Maximum
        "21": ("3",),   # LC #33 Search in Rotated Sorted Array
        "22": ("3",),   # LC #153 Find Min in Rotated Sorted Array
        "23": ("3",),   # LC #162 Find Peak Element
        "24": ("3",),   # LC #875 Koko Eating Bananas
    }
    for row_id, (confidence,) in dsa_updates.items():
        rows.extend(dsa_solved(row_id, confidence))

    # Aug 24 daily plan
    aug24 = "2026-08-24"
    rows.extend(
        [
            daily_task(
                aug24,
                "lc-239-done",
                "DSA",
                "LC #239 Sliding Window Maximum",
                "Hard. Monotonic Deque. FINISHES Sliding Window pattern.",
                link="https://leetcode.com/problems/sliding-window-maximum/",
                minutes=55,
                status="done",
            ),
            daily_task(
                aug24,
                "lc-33-search-rotated",
                "DSA",
                "LC #33 Search in Rotated Sorted Array",
                "Binary Search. One half is always sorted.",
                link="https://leetcode.com/problems/search-in-rotated-sorted-array/",
                minutes=45,
                status="done",
            ),
            daily_task(
                aug24,
                "lc-153-find-min-rotated",
                "DSA",
                "LC #153 Find Min in Rotated Sorted Array",
                "Binary Search. Compare mid with right.",
                link="https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
                minutes=35,
                status="done",
            ),
            daily_task(
                aug24,
                "lc-162-find-peak",
                "DSA",
                "LC #162 Find Peak Element",
                "Binary Search. Move toward higher neighbor.",
                link="https://leetcode.com/problems/find-peak-element/",
                minutes=30,
                status="done",
            ),
            daily_task(
                aug24,
                "algomaster-scalability",
                "System Design",
                "AlgoMaster: Scalability + Availability",
                "Read 2 core concepts (15 min each). Replace DDIA Ch1 for now.",
                link="https://algomaster.io/learn/system-design/top-30-system-design-concepts",
                minutes=30,
                status="pending",
                priority="medium",
            ),
            daily_task(
                aug24,
                "picnic-bugfix",
                "Career",
                "Picnic Prep: Hand-write 1 bug-fix exercise",
                "45 min block. No IDE autocomplete.",
                minutes=45,
                status="pending",
                priority="high",
            ),
        ]
    )

    # Aug 25 daily plan (today)
    aug25 = "2026-08-25"
    rows.extend(
        [
            daily_task(
                aug25,
                "lc-875-koko",
                "DSA",
                "LC #875 Koko Eating Bananas",
                "Binary Search on answer space. ceil(pile/speed) trick.",
                link="https://leetcode.com/problems/koko-eating-bananas/",
                minutes=40,
                status="done",
            ),
            daily_task(
                aug25,
                "lc-1011-ship",
                "DSA",
                "LC #1011 Capacity to Ship Packages Within D Days",
                "Same BS-on-answer pattern as LC #875.",
                link="https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/",
                minutes=35,
                status="pending",
            ),
            daily_task(
                aug25,
                "revision-binary-search",
                "DSA Revision",
                "Revision: LC #33, #153, #162 (15 min)",
                "Say pattern + key insight for each. No notes.",
                minutes=15,
                status="pending",
            ),
            daily_task(
                aug25,
                "algomaster-reliability",
                "System Design",
                "AlgoMaster: Reliability + SPOF + Latency vs Throughput",
                "3 concepts, ~30 min total.",
                link="https://algomaster.io/learn/system-design/top-30-system-design-concepts",
                minutes=30,
                status="pending",
                priority="medium",
            ),
            daily_task(
                aug25,
                "picnic-java-spring",
                "Career",
                "Picnic Prep: Java/Spring revision (R1 deep-dive)",
                "Harbor architecture + Vodafone stories. 30 min out loud.",
                minutes=30,
                status="pending",
                priority="high",
            ),
        ]
    )

    # Picnic interview tracker
    rows.extend(
        [
            picnic_row("screening_passed", "2026-08-24"),
            picnic_row("round_1_status", "pending"),
            picnic_row("round_2_status", "pending"),
            picnic_row("round_3_status", "pending"),
            picnic_row("round_4_status", "pending"),
            picnic_row("exercises_completed", 1),
            picnic_row("current_exercise", 2),
            picnic_row("last_practice_date", "2026-08-24"),
        ]
    )

    return rows


def upsert_rows(rows: list[dict]) -> None:
    require_credentials()
    url = f"{SUPABASE_REST_URL}/{TABLE}?on_conflict=id"
    body = json.dumps(rows).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status not in (200, 201, 204):
            raise RuntimeError(f"Unexpected status: {resp.status}")


def fetch_status() -> None:
    require_credentials()
    url = (
        f"{SUPABASE_REST_URL}/{TABLE}?user_id=eq.{USER}"
        f"&select=topic_id,field,row_id,doc_id,updated_at"
    )
    req = urllib.request.Request(
        url,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        rows = json.loads(resp.read().decode())

    solved = sorted(
        {r["row_id"] for r in rows if r["topic_id"] == "dsa-patterns" and r["field"] == "solved"},
        key=lambda x: int(x) if x.isdigit() else x,
    )
    plan_dates = sorted(
        {r["doc_id"] for r in rows if r["topic_id"] == "daily-plan" and r["field"] == "task"},
        reverse=True,
    )
    print(f"Total rows: {len(rows)}")
    print(f"DSA solved: {len(solved)} -> {solved}")
    print(f"Daily plan dates: {plan_dates[:10]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync study progress to Supabase")
    parser.add_argument("--status", action="store_true", help="Show current Supabase state")
    parser.add_argument("--dsa-only", action="store_true", help="Sync only DSA rows")
    parser.add_argument("--plan", metavar="DATE", help="Sync only one daily plan (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.status:
        fetch_status()
        return 0

    rows = build_sync_payload()
    if args.dsa_only:
        rows = [r for r in rows if r["topic_id"] == "dsa-patterns"]
    elif args.plan:
        rows = [r for r in rows if r["topic_id"] == "daily-plan" and r["doc_id"] == args.plan]

    print(f"Upserting {len(rows)} rows...")
    try:
        upsert_rows(rows)
    except urllib.error.HTTPError as exc:
        print(f"HTTP error {exc.code}: {exc.read().decode()}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        return 1

    print("Sync complete.")
    fetch_status()
    return 0


def refresh_session_state() -> None:
    pull_script = Path(__file__).resolve().parent / "pull_study_state.py"
    if pull_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(pull_script)], check=False)


if __name__ == "__main__":
    code = main()
    if code == 0 and "--status" not in sys.argv:
        refresh_session_state()
    raise SystemExit(code)
