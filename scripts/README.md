# Study sync scripts

`sync_supabase.py` pushes study progress to Supabase; `pull_study_state.py` pulls
it back into `study-session-state.json` for agent context handoff.

## Credentials

This repository is public, so the Supabase URL and key are read from the
environment instead of being committed. Both scripts exit with a clear message
if they are missing.

```bash
export SUPABASE_URL="https://<project>.supabase.co/rest/v1"
export SUPABASE_KEY="sb_publishable_..."
```

Add those to `~/.zshrc` so they persist across shells.

## Usage

```bash
python3 scripts/sync_supabase.py            # full sync
python3 scripts/sync_supabase.py --status   # show current state
python3 scripts/pull_study_state.py         # refresh session state
```

## Note on the publishable key

A Supabase publishable key is safe to expose only when row level security is
enabled and scoped to the owning user. Verify that on the `study_progress`
table — without it, anyone holding the key can read every row.
