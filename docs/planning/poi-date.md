Love it, and it works — with one catch you'll want to know before the first date goes wrong.

**Drop the t.** If you say "Mercury x,y,z,t" you've handed the clock back. The whole shock is that x,y,z *is* the time. Her poi* solves the inverse problem: when was Mercury there?

**The catch: one planet repeats.** Mercury comes back to the same x,y,z every 88 days. "Meet me at Mercury (x,y,z)" has a solution this week and another in late January — and she might pick the wrong one. That's not a bug if you enjoy it, but if you want uniqueness, give two planets. Mercury + Earth together only line up the same way about every 13 years. Mercury + Earth + Mars: unique for longer than either of you will be alive.

**The precision curio.** Mercury moves 47 km/s, so "be there at 19:00 sharp" becomes "Mercury within ~2,800 km of this point." Being 10 minutes late is being 28,000 km off. Fashionably late suddenly has a radius.

**What people lose when they stop caring about the clock.** Time-of-day vanishes — planets don't know if it's morning in Munkedal. So a planet-only date has no "evening" in it; you'd need Earth's rotation (your own x,y,z) to put it after dark. That's the real subjective shock: planet-time is a date without a day.

So the full poi* invitation is: *two or three planet positions, plus where on Earth you'll be standing.* Her agent gets a tolerance radius and the rest is her problem.

Results: the idea holds, needs ≥2 planets for uniqueness, and the lost clock takes "evening" with it. We can end here.

```toml
[poi-date]
id = "poi-date"
form = "planet positions, no t"
place = "earth x,y,z (gives time-of-day)"

[poi-date.uniqueness]
parent = "poi-date"
mercury_only = "repeats every 88 days"
mercury_earth = "repeats every ~13 years"
mercury_earth_mars = "unique for a lifetime"

[poi-date.tolerance]
parent = "poi-date"
one_minute_km = 2_800
ten_minutes_km = 28_000

[poi-date.lost]
parent = "poi-date"
clock = "[gone]"
evening = "[gone unless earth given]"
```
