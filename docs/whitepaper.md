# poi\*time: a three-line clock of unix, sun and moon

**Altair** · celestial-lunar · draft 1, unix 1793443400

---

## Abstract

poi\*time is a clock that shows three times in parallel: the unix second, a solar clock and a lunar clock. Both the solar and the lunar clock are written in *åt* form, as minutes remaining until the next whole hour (11:03 is `57åt12`). The lunar clock is the solar clock shifted back by the angular separation between the sun and the moon, converted to time at 15° per hour. The current implementation uses a mean synodic month and has no dependencies beyond Python 3.11. Validated against eight NASA eclipse times, the model places new and full moons within 16 hours, which corresponds to a lunar-clock error of about 30 minutes. We describe the model, its validation, its known limits and a path to sub-minute accuracy.

## 1. Motivation

Mechanical clocks answer *what hour is it*. A person standing outside answers a different question: where is the sun, where is the moon, and how long until the next turn. poi\*time writes down that second answer.

Three choices follow from it:

1. **Unix is the ground truth for *when*.** It has no zone, no calendar and no interpretation. Every other line is derived from it.
2. **Count down, not up.** Minutes remaining to the hour (`57åt12`) put the attention on what is coming rather than what has passed.
3. **Only the sun and the moon.** They are the two bodies anyone can see. The planets are deliberately left out of the clock (see `docs/planning/poi-date.md` for a separate planetary-time idea).

## 2. Name

poi\* reads two ways, and both are intended:

- **polynomial input/output.** Classical astronomical algorithms compute positions as polynomials in time plus periodic terms. One input, the time, goes in; positions come out. poi\*time today is the degree-one case of that.
- **Poimandres**, the voice of mind in the first treatise of the *Corpus Hermeticum*.

## 3. Model

### 3.1 Constants

From `moon.toml`:

| Symbol | Value | Meaning |
|---|---|---|
| *P* | 2 551 442.88 s (29.530 588 853 d) | mean synodic month |
| *t₀* | 947 182 440 (2000-01-06 18:14 UTC) | reference new moon |
| *d* | 384 400 km | mean Earth–Moon distance |
| *c* | 299 792 458 m/s | speed of light |
| *d/c* | 1.2822 s | light travel time, Moon to eye |

### 3.2 Lunar phase and lag

For a unix time *t*:

```
φ(t) = ((t − t₀) mod P) / P          phase, 0 = new, 0.5 = full
L(t) = φ(t) · 86 400 s               lag of the moon behind the sun
```

The elongation of the moon from the sun is 360°·φ. At 15° per hour that is φ·24 h, which is *L*. The lag grows by about 48.8 minutes per day: 0 at new moon, 12 h at full moon.

### 3.3 The three lines

Let *s* be seconds since local midnight in Europe/Stockholm.

```
unix  = t
sol   = åt(s)
måne  = åt((s − L(t)) mod 86 400)
```

where, for hour *h* and minute *m*:

```
åt(h, m) = 0åt h                 if m = 0
           (60 − m)åt(h + 1)     otherwise, hour mod 24
```

Examples: 11:03 → `57åt12`, 12:30 → `30åt13`, 12:00 → `0åt12`, 23:45 → `15åt0`.

Reading the lunar line: a lunar clock near `0åt12` means the moon is near its highest point; near the solar sunset hour it is near setting.

### 3.4 Example

```
unix  1793440743
sol   1åt11
måne  18åt19
```

Phase 0.678 (waning gibbous), lag 16 h 16 min.

## 4. Validation

`test_moon.py` compares the mean model with eight eclipse times from the NASA Eclipse Web Site (eclipses happen exactly at new or full moon), 2025–2026:

| Eclipse | Expected | Model deviation |
|---|---|---|
| 2025-03-14 total lunar | full | −6.0 h |
| 2025-03-29 partial solar | new | +3.7 h |
| 2025-09-07 total lunar | full | +0.8 h |
| 2025-09-21 partial solar | new | −15.8 h |
| 2026-02-17 annular solar | new | +8.7 h |
| 2026-03-03 total lunar | full | −10.1 h |
| 2026-08-12 total solar | new | −14.0 h |
| 2026-08-28 partial lunar | full | +2.2 h |

All eight pass the one-day tolerance. The worst case, 15.8 h, is a phase error of 0.022, which moves the lunar clock by about 32 minutes.

`test_at_klocka.py` checks the *åt* format (four edge cases, including midnight wrap), the solar line at a known wall time, the exact three-line output, and that the lag is about 0 h at a new moon and about 12 h at a full moon.

Run both:

```
python3 test_moon.py
python3 test_at_klocka.py
```

## 5. Limits

1. **Mean motion.** The Moon's orbit is elliptical (e ≈ 0.055) and perturbed by the Sun, so a true new or full moon can fall over half a day from the mean one (15.8 h in the worst case above). This is the main error source.
2. **Elongation is not hour angle.** The lag uses ecliptic elongation as if it were the difference in hour angle. The Moon's orbit is inclined about 5° to the ecliptic, and at high latitudes (Uddevalla, 58.35° N) rise and set times depend strongly on declination. The lunar line says where the moon is *in the day*, not exactly when it rises.
3. **Wall clock, not solar time.** The solar line follows Europe/Stockholm wall time by design. True solar time differs: Uddevalla lies 3.06° west of the CET meridian (−12.2 min), and the equation of time swings by up to ±16 min over the year. On 31 October these nearly cancel, leaving true solar time about 4 min ahead.
4. **Light travel time** (1.28 s) is defined in `moon.toml` but is far below the clock's minute resolution.

## 6. Toward exact

Two paths, both in `docs/planning/exakt-mane.md`:

- **Meeus, *Astronomical Algorithms* (2nd ed., 1998), ch. 47 and 49.** The Moon's longitude as a polynomial in Julian centuries plus periodic terms, in pure Python and without dependencies. Accuracy about 10″, far below a minute. This is the polynomial-input/output path in its full form.
- **Skyfield with JPL DE421.** Exact, with rise and set for any location, at the cost of a 17 MB ephemeris and an external package.

The proposed acceptance test: tighten the eclipse tolerance from one day to one hour, and compare lunar rise and set for Uddevalla against a published almanac over several days.

## 7. Outlook: world calendars

Unix is a shared base line. Any calendar that can be computed from it, whether solar, lunar or lunisolar, can stand as another line next to sun and moon. The companion repository [multi-calendar](https://github.com/Azdwarf5Azdwarf/multi-calendar) starts with the Egyptian civil calendar. The aim is one instant read in many systems at once, so that people who count time differently can still point at the same moment.

## 8. Files

| File | Role |
|---|---|
| `moon.toml` | constants |
| `at_klocka.py` | poi\*time, the three lines |
| `test_moon.py`, `test_at_klocka.py` | validation |
| `docs/at-klocka.md` | design notes and origin |
| `docs/planning/exakt-mane.md` | path to exact |
| `agents/*.toml`, `drama.lisp` | agents that read the clock, and their event log |

## License

MIT, see `LICENSE`.
