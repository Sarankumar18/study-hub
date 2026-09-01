#!/usr/bin/env python3
"""
Pull Supabase study_progress + local tracker-data.json into a single
session state file for agent-to-agent context handoff.

Usage:
  python3 scripts/pull_study_state.py
  python3 scripts/pull_study_state.py --stdout   # print JSON only
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "study-session-state.json"
TRACKER_FILE = ROOT / "tracker-data.json"

# This repo is public. The key grants read access to the study_progress table,
# so it is supplied at runtime rather than committed.
#   export SUPABASE_URL="https://<project>.supabase.co/rest/v1"
#   export SUPABASE_KEY="sb_publishable_..."
SUPABASE_REST_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
TABLE = "study_progress"


def require_credentials() -> None:
    missing = [n for n, v in (("SUPABASE_URL", SUPABASE_REST_URL),
                              ("SUPABASE_KEY", SUPABASE_KEY)) if not v]
    if missing:
        sys.exit(f"Missing environment variable(s): {', '.join(missing)}. "
                 "See scripts/README.md.")
USER = "sbaskar"

ROW_TO_LC = {
    "1": "LC #1 Two Sum",
    "2": "LC #49 Group Anagrams",
    "3": "LC #238 Product Except Self",
    "4": "LC #128 Longest Consecutive",
    "5": "LC #347 Top K Frequent",
    "6": "LC #11 Container With Most Water",
    "7": "LC #15 3Sum",
    "8": "LC #75 Sort Colors",
    "9": "LC #287 Find Duplicate",
    "10": "LC #5 Longest Palindrome",
    "11": "LC #3 Longest Substring",
    "12": "LC #424 Repeating Char Replacement",
    "13": "LC #567 Permutation in String",
    "14": "LC #438 Find All Anagrams",
    "15": "LC #76 Min Window Substring",
    "16": "LC #904 Fruit Into Baskets",
    "17": "LC #1004 Max Consecutive Ones III",
    "18": "LC #713 Subarray Product < K",
    "19": "LC #1838 Freq Most Frequent",
    "20": "LC #239 Sliding Window Maximum",
    "21": "LC #33 Search Rotated Sorted Array",
    "22": "LC #153 Find Min Rotated",
    "23": "LC #162 Find Peak Element",
    "24": "LC #875 Koko Eating Bananas",
    "25": "LC #1011 Capacity Ship Packages",
    "26": "LC #1482 Min Days Bouquets",
    "28": "LC #34 First Last Position",
    "27": "LC #410 Split Array Largest Sum",
    "29": "LC #4 Median Two Sorted Arrays",
    "30": "LC #378 Kth Smallest Matrix",
    "135": "LC #48 Rotate Image",
    "136": "LC #54 Spiral Matrix",
    "137": "LC #121 Best Time Buy Sell Stock",
}

PATTERNS = {
    "Arrays & Hashing": [str(i) for i in range(1, 6)] + ["135", "136"],
    "Two Pointers": [str(i) for i in range(6, 11)],
    "Sliding Window": [str(i) for i in range(11, 21)] + ["137"],
    "Binary Search": [str(i) for i in range(21, 31)],
    "Bit Manipulation": [str(i) for i in range(31, 35)],
}

NEXT_BS = [
    ("30", "LC #378 Kth Smallest in Sorted Matrix"),
    ("27", "LC #410 Split Array Largest Sum"),
    ("29", "LC #4 Median of Two Sorted Arrays"),
]


def fetch_progress() -> list[dict]:
    require_credentials()
    url = (
        f"{SUPABASE_REST_URL}/{TABLE}?user_id=eq.{USER}"
        "&select=topic_id,doc_id,row_id,field,value,updated_at"
        "&order=updated_at.desc"
    )
    req = urllib.request.Request(
        url,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def build_state(rows: list[dict]) -> dict:
    solved_ids = sorted(
        {
            r["row_id"]
            for r in rows
            if r["topic_id"] == "dsa-patterns"
            and r["field"] == "solved"
            and r["value"] is True
        },
        key=lambda x: int(x) if x.isdigit() else x,
    )

    pattern_progress = {}
    for name, ids in PATTERNS.items():
        done = sum(1 for i in ids if i in solved_ids)
        pattern_progress[name] = {
            "solved": done,
            "total": len(ids),
            "complete": done == len(ids),
        }

    daily_tasks: dict[str, list] = {}
    for r in rows:
        if r["topic_id"] == "daily-plan" and r["field"] == "task":
            date = r["doc_id"]
            task = dict(r["value"])
            task["task_id"] = r["row_id"]
            daily_tasks.setdefault(date, []).append(task)

    latest_plan_date = max(daily_tasks.keys()) if daily_tasks else None
    latest_plan = daily_tasks.get(latest_plan_date, []) if latest_plan_date else []

    career = {}
    if TRACKER_FILE.exists():
        career = json.loads(TRACKER_FILE.read_text())

    next_problems = [
        {"row_id": rid, "label": label}
        for rid, label in NEXT_BS
        if rid not in solved_ids
    ]

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "scripts/pull_study_state.py",
        "user_id": USER,
        "dsa": {
            "solved_count": len(solved_ids),
            "total": 142,
            "solved_row_ids": solved_ids,
            "solved_labels": [ROW_TO_LC.get(i, f"row {i}") for i in solved_ids],
            "current_pattern": "Binary Search",
            "pattern_progress": pattern_progress,
            "next_problems": next_problems,
        },
        "daily_plan": {
            "latest_date": latest_plan_date,
            "tasks": sorted(
                latest_plan,
                key=lambda t: {"high": 0, "medium": 1, "low": 2}.get(t.get("priority"), 9),
            ),
        },
        "career": career,
        "agent_instructions": (
            "Read this file at the start of every session and before launching subagents. "
            "After marking work done, run: python3 scripts/pull_study_state.py"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    rows = fetch_progress()
    state = build_state(rows)
    payload = json.dumps(state, indent=2)

    if args.stdout:
        print(payload)
    else:
        STATE_FILE.write_text(payload + "\n")
        print(f"Wrote {STATE_FILE}")
        print(f"DSA: {state['dsa']['solved_count']}/142")
        print(f"Latest plan: {state['daily_plan']['latest_date']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
