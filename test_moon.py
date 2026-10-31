"""Test: manens alder ur moon.toml mot kanda nymanar och fullmanar.

Kor: python3 test_moon.py
Inga beroenden utover python3 >= 3.11 (tomllib).
"""
import tomllib
from datetime import datetime, timezone
from pathlib import Path

TOLERANS_SEKUNDER = 86400  # 1 dygn

# Kallor: NASA Eclipse Web Site (eclipse.gsfc.nasa.gov), formorkelser sker
# exakt vid nymane (sol) resp. fullmane (man). Tider i UTC.
KANDA = [
    ("2025-03-14T06:55:00Z", "full", "total manformorkelse 2025-03-14"),
    ("2025-03-29T10:58:00Z", "ny",   "partiell solformorkelse 2025-03-29"),
    ("2025-09-07T18:09:00Z", "full", "total manformorkelse 2025-09-07"),
    ("2025-09-21T19:54:00Z", "ny",   "partiell solformorkelse 2025-09-21"),
    ("2026-02-17T12:01:00Z", "ny",   "ringformig solformorkelse 2026-02-17"),
    ("2026-03-03T11:38:00Z", "full", "total manformorkelse 2026-03-03"),
    ("2026-08-12T17:46:00Z", "ny",   "total solformorkelse 2026-08-12"),
    ("2026-08-28T04:18:00Z", "full", "partiell manformorkelse 2026-08-28"),
]


def las_konstanter():
    with open(Path(__file__).parent / "moon.toml", "rb") as f:
        return tomllib.load(f)


def manens_alder(unix, k):
    """Sekunder sedan senaste nymane enligt medelmodellen."""
    synodisk = k["synodisk_manad"]["sekunder"]
    ref = k["referens_nymane"]["unix"]
    return (unix - ref) % synodisk


def iso_till_unix(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def main():
    k = las_konstanter()
    synodisk = k["synodisk_manad"]["sekunder"]
    fel = 0
    for iso, fas, kalla in KANDA:
        alder = manens_alder(iso_till_unix(iso), k)
        vantad = 0.0 if fas == "ny" else synodisk / 2
        # cirkular skillnad, sa 29.4 dygn ~ -0.1 dygn
        diff = (alder - vantad + synodisk / 2) % synodisk - synodisk / 2
        ok = abs(diff) <= TOLERANS_SEKUNDER
        fel += not ok
        print(f"{'OK ' if ok else 'FEL'} {iso} {fas:4} avvikelse {diff/3600:+6.1f} h  ({kalla})")
    print(f"{len(KANDA) - fel}/{len(KANDA)} godkanda, tolerans {TOLERANS_SEKUNDER/86400:.0f} dygn")
    raise SystemExit(1 if fel else 0)


if __name__ == "__main__":
    main()
