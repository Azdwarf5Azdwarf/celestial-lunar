"""At-klocka: Altairs personliga klocka. Minuter kvar till timmen: 11:03 = 57åt12.

Tre parallella tider, alltid visade sa har:
    unix  1793440743
    sol   1åt11
    mane  18åt19

Bara solen och manen, inget mer.
- Solen ar vaggklockan (lokal tid i Europe/Stockholm).
- Manen ar samma klocka minus manens eftersläpning: vinkeln mellan sol och
  mane (fas * 360 grader), 15 grader per timme. Vid nymane gar de ihop,
  vid fullmane ar de 12 timmar isar.
Planeterna ar inte med i klockan, se docs/planning/poi-date.md.

Kor: python3 at_klocka.py              (nu)
     python3 at_klocka.py 1793440743   (en unix-tid)
Inga beroenden utover python3 >= 3.11 (tomllib).
"""
import sys
import time
import tomllib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZON = ZoneInfo("Europe/Stockholm")
DYGN = 86400


def las_konstanter():
    with open(Path(__file__).parent / "moon.toml", "rb") as f:
        return tomllib.load(f)


def at(timme, minut):
    """Minuter kvar till nasta hela timme. 11:03 -> '57åt12', 12:00 -> '0åt12'."""
    if minut == 0:
        return f"0åt{timme}"
    return f"{60 - minut}åt{(timme + 1) % 24}"


def manens_fas(unix, k):
    """0 = nymane, 0.5 = fullmane. Medelmodellen i moon.toml."""
    synodisk = k["synodisk_manad"]["sekunder"]
    ref = k["referens_nymane"]["unix"]
    return ((unix - ref) % synodisk) / synodisk


def manens_slapning(unix, k):
    """Sekunder som manen ligger efter solen: fas * 360 grader / 15 grader per h."""
    return manens_fas(unix, k) * DYGN


def klocka(unix, k):
    lokal = datetime.fromtimestamp(unix, ZON)
    sol = lokal.hour * 3600 + lokal.minute * 60 + lokal.second
    slap = manens_slapning(unix, k)
    mane = int(sol - slap) % DYGN
    return {
        "unix": int(unix),
        "sol": at(lokal.hour, lokal.minute),
        "mane": at(mane // 3600, mane % 3600 // 60),
        "skillnad": f"{int(slap) // 3600} h {int(slap) % 3600 // 60} min",
        "fas": round(manens_fas(unix, k), 3),
    }


def rader(r):
    """Tre parallella tider, alltid i den har ordningen: unix, sol, mane."""
    return [
        f"unix  {r['unix']}",
        f"sol   {r['sol']}",
        f"mane  {r['mane']}",
    ]


def main():
    unix = int(sys.argv[1]) if len(sys.argv) > 1 else int(time.time())
    print("\n".join(rader(klocka(unix, las_konstanter()))))


if __name__ == "__main__":
    main()
