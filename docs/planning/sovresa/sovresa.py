#!/usr/bin/env python3
"""sovresa — how far the planets carried you while you slept.

value = sum over planets of (orbital speed km/s * seconds asleep)

Usage:
  sovresa.py --bed 00:30 --wake 07:30 --awake 10 10
  sovresa.py --seconds 24000
  sovresa.py --whoop            # reads last night from WHOOP (see whoop.py)
  sovresa.py ... --toml         # print a TOML block for the dagbok
"""
import argparse
import datetime as dt
import sys

# mean orbital speeds, km/s
PLANETS = {
    "mercury": 47.4,
    "venus": 35.0,
    "earth": 29.8,
    "mars": 24.1,
    "jupiter": 13.1,
    "saturn": 9.7,
    "uranus": 6.8,
    "neptune": 5.4,
}


def asleep_seconds(bed: str, wake: str, awake_minutes: list[int]) -> int:
    b = dt.datetime.strptime(bed, "%H:%M")
    w = dt.datetime.strptime(wake, "%H:%M")
    if w <= b:
        w += dt.timedelta(days=1)
    total = int((w - b).total_seconds())
    return total - 60 * sum(awake_minutes)


def planet_km(seconds: int) -> dict[str, int]:
    out = {name: round(v * seconds) for name, v in PLANETS.items()}
    out["total"] = sum(out.values())
    return out


def as_toml(date: str, seconds: int, km: dict[str, int], source: str) -> str:
    lines = [
        f'[night."{date}"]',
        f'source = "{source}"',
        f"asleep_seconds = {seconds}",
        "",
        f'[night."{date}".planets]',
    ]
    for k, v in km.items():
        lines.append(f"{k} = {v:_}")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bed")
    p.add_argument("--wake")
    p.add_argument("--awake", nargs="*", type=int, default=[], help="minutes awake, per wake-up")
    p.add_argument("--seconds", type=int)
    p.add_argument("--whoop", action="store_true")
    p.add_argument("--date", default=dt.date.today().isoformat())
    p.add_argument("--toml", action="store_true")
    a = p.parse_args()

    if a.whoop:
        from whoop import last_night_asleep_seconds
        seconds, source = last_night_asleep_seconds(), "whoop"
    elif a.seconds is not None:
        seconds, source = a.seconds, "manual"
    elif a.bed and a.wake:
        seconds, source = asleep_seconds(a.bed, a.wake, a.awake), "manual"
    else:
        sys.exit("give --bed/--wake, --seconds, or --whoop")

    km = planet_km(seconds)
    if a.toml:
        print(as_toml(a.date, seconds, km, source))
    else:
        h, m = divmod(seconds // 60, 60)
        print(f"asleep {h}h{m:02d}  ({seconds} s)")
        for k, v in km.items():
            print(f"{k:>8}  {v:>12,} km")


if __name__ == "__main__":
    main()
