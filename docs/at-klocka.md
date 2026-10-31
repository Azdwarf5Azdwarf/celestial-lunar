# Åt-klockan: Altairs personliga klocka

Unix 1793440743. Kod: `at_klocka.py`, test: `test_at_klocka.py`.

## Karna (ordagrant, orord)

> Kan du lagga in till ~/dev/celestial-lunar min personliga Åt klocka. Dvs inkludera den nya filerna MED denna filosofi hur hanger det ihop personligt?
>
> Typ 12:30 är 30åt12 men inkludera planertarna kanske for klockan bara solen och manens differens inget mer?

## Karna 2 (ordagrant, orord)

> ska vi ta med xnix och dar har vi perfektion alltsa att tifen måste visas just så i 3 parallellt?

## Karna 3 (ordagrant, orord)

> 57at12 nu exempelvis

Skrivet klockan 11:03. Altair bekraftade regeln: **åt = minuter kvar till nasta hela timme.** (Forsta exemplet "12:30 = 30åt12" ersatts: 12:30 = 30åt13.)

## Karna 4 (ordagrant, orord)

> unix moment, kvar till timmen, i just kvar till timmen räknar man alltid i differensen mellan solen och månen makes sense

## Vad klockan visar

Tre parallella tider, alltid i den har ordningen:

```
unix  1793440743
sol   1åt11
mane  18åt19
```

- **unix**: sanningen for nar (samma som stampeln i varje svar, AFC-001). Ingen zon, ingen tolkning.
- **sol**: vaggklockan. Minuter kvar, sedan timmen de ar pa vag mot. 11:03 blir `57åt12`, 12:30 blir `30åt13`, 12:00 blir `0åt12`.
- **mane**: samma klocka, fast manens. Manen ligger efter solen med vinkeln mellan dem (fas x 360 grader, 15 grader per timme).
- **skillnad** (finns i koden, visas inte): hur langt efter, i timmar och minuter. Nymane ca 0 h, de gar ihop. Fullmane ca 12 h, de star mitt emot varandra.

Bara solen och manen, inget mer. Planeterna ar inte med i klockan. De bor i `docs/planning/poi-date.md` (tid utan t) och `docs/planning/sovresa/`.

## Personligt (Altairs ord, 2026-10-28, pa vag till bussen)

> I can see the sun and I can see the moon and the moon is behind me to my right, the Sun in front. It feels like I am connected to them, or metaphysically so to speak.

Samma dag: beslutet att ata och dricka kom efter att han sag solen och manen. Lunchen flyttades till solens hogsta punkt. Hans egen teori om forfaderna i Mellanostern fore 1900, utan mekaniska klockor: "the Sun is sorted right there".

## Lasning (utanfor karnan)

- Klockan ar den han redan anvander: solen framfor, manen bakom. Siffrorna skriver bara ner det han ser.
- `skillnad` ar avstandet mellan dem pa himlen, omraknat till tid. Det ar det enda som klockan lagger till.

## Hur filerna hanger ihop

- `moon.toml`: rytmen (synodisk manad, nymane-nollpunkt, ljusets restid 1,28 s). Klockan laser harifran.
- `at_klocka.py`: unix, sol och mane, med sol och mane som `minuterkvaråttimme`.
- `test_moon.py` / `test_at_klocka.py`: kollar mot NASA:s formorkelser (ny- och fullmanar).
- `agents/khonsu.toml`, `agents/thoth.toml`: platshallarna som ror sig med manen. Khonsu bar ljuset de 1,28 sekunderna.
- `drama.lisp`: handelserna, en rad per handelse, unix-tid forst.
- `docs/tidvatten.md`: manens drag pa manniskan.
- `docs/planning/`: planeterna, for senare.
