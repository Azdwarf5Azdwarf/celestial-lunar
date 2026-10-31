# sovresa

How far the planets carried you while you slept.

```
value = Σ planets (orbital speed km/s × seconds asleep)
```

## Run

```
python sovresa.py --bed 00:30 --wake 07:30 --awake 10 10
python sovresa.py --bed 00:30 --wake 07:30 --awake 10 10 --toml >> dagbok.toml
```

## Automate

`whoop.py` is a stub. With a WHOOP (or any sleep tracker that gives
start, end, and awake-time), `--whoop` replaces the manual input and the
whole thing becomes a cron job that appends one TOML block per night.
