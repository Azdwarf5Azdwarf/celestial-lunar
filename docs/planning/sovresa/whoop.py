"""WHOOP adapter — STUB. Not wired yet.

WHOOP has a developer API (OAuth2) with sleep records that include
start/end times and time-awake. Wire this once you have:
  WHOOP_ACCESS_TOKEN   (from the OAuth flow in the WHOOP developer portal)

Replace the body of last_night_asleep_seconds() with:
  1. GET the most recent sleep record
  2. seconds = (end - start) - awake_time
  3. return seconds
"""
import os


def last_night_asleep_seconds() -> int:
    token = os.environ.get("WHOOP_ACCESS_TOKEN")
    if not token:
        raise SystemExit("WHOOP_ACCESS_TOKEN not set — WHOOP adapter is a stub, use --bed/--wake for now")
    raise NotImplementedError("wire the WHOOP sleep endpoint here")
