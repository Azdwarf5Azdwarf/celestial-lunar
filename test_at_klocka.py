"""Test: at-klockan. Format och sol/mane-skillnad vid kanda ny- och fullmanar.

Kor: python3 test_at_klocka.py
"""
from datetime import datetime

from at_klocka import ZON, at, klocka, las_konstanter, manens_slapning, rader

# en dag av fasfel = ca 49 min skillnad i klockan
TOLERANS_SEKUNDER = 3600


def unix(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def cirkular(a, b):
    return abs((a - b + 43200) % 86400 - 43200)


def main():
    k = las_konstanter()
    fall = []

    fall.append(("format 11:03", at(11, 3) == "57åt12"))
    fall.append(("format 12:30", at(12, 30) == "30åt13"))
    fall.append(("format 12:00", at(12, 0) == "0åt12"))
    fall.append(("format 23:45", at(23, 45) == "15åt0"))

    altairs = datetime(2026, 10, 31, 11, 3, tzinfo=ZON).timestamp()
    fall.append(("sol 2026-10-31 11:03 (Altairs exempel)", klocka(altairs, k)["sol"] == "57åt12"))

    tre = rader(klocka(1793440743, k))
    fall.append(("tre rader: unix, sol, mane",
                 tre == ["unix  1793440743", "sol   1åt11", "mane  18åt19"]))

    # NASA-formorkelser: nymane = sol och mane ihop, fullmane = 12 h isar
    ny = manens_slapning(unix("2026-08-12T17:46:00Z"), k)
    fall.append(("nymane 2026-08-12, skillnad ~0", cirkular(ny, 0) <= TOLERANS_SEKUNDER))
    full = manens_slapning(unix("2026-08-28T04:18:00Z"), k)
    fall.append(("fullmane 2026-08-28, skillnad ~12h", cirkular(full, 43200) <= TOLERANS_SEKUNDER))

    fel = 0
    for namn, ok in fall:
        fel += not ok
        print(f"{'OK ' if ok else 'FEL'} {namn}")
    print(f"{len(fall) - fel}/{len(fall)} godkanda")
    raise SystemExit(1 if fel else 0)


if __name__ == "__main__":
    main()
