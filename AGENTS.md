# Agent Instructions — Personal Study Hub

This repo uses **shared state files** so new Cursor chats and subagents do not lose context.

## Start every session

```bash
python3 scripts/pull_study_state.py
```

Then read:

1. `study-session-state.json` — DSA progress, daily plan, next problems
2. `tracker-data.json` — interviews, machine coding, career notes

## User commands

| Command | Agent must |
|---------|------------|
| `Today` | Read session state → generate/seed daily plan in Supabase |
| `Done` | Sync Supabase → run `pull_study_state.py` |
| `Progress` | Read session state (refresh if stale) |

## Source of truth

- **DSA progress:** Supabase table `study_progress`
- **Career/interview:** `tracker-data.json`
- **Handoff snapshot:** `study-session-state.json` (auto-generated)

## Subagents

Task subagents do **not** see parent chat history. Parent must paste relevant context from `study-session-state.json` into the subagent prompt.
