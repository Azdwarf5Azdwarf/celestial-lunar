"""Armband adapter — STUB. Not wired yet. An example, not a dependency.

Any standard fitness bracelet with a sleep API works here (Fitbit, Garmin,
Oura, WHOOP, ...). Most give a sleep record with start, end and time awake,
behind an OAuth2 access token. Wire this once you have:
  ARMBAND_ACCESS_TOKEN   (from your bracelet's developer portal)

Replace the body of last_night_asleep_seconds() with:
  1. GET the most recent sleep record
  2. seconds = (end - start) - awake_time
  3. return seconds
"""
import os


def last_night_asleep_seconds() -> int:
    token = os.environ.get("ARMBAND_ACCESS_TOKEN")
    if not token:
        raise SystemExit("ARMBAND_ACCESS_TOKEN not set — armband adapter is a stub, use --bed/--wake for now")
    raise NotImplementedError("wire your bracelet's sleep endpoint here")
