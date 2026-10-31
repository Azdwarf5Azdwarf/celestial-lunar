# Exakt mane i Åt-klockan

Not, unix 1793441581. Inget byggt an. Hor till `at_klocka.py` och `docs/at-klocka.md`.

## Karna (ordagrant, orord)

> Ja du kan skapa en not kring det for att fa det exakt (kanner redan kollar klockan kanns annorlunda ser inte timmen langre ser bara åt 11:12 maste rakna da)

## Vad medelmodellen missar

Idag raknar klockan manen med medelmanaden i `moon.toml`. Det ar enkelt men grovt.

1. **Manens verkliga bana.** Banan ar elliptisk och lutar ca 5 grader. Manen gar fortare och langsammare under manaden. `test_moon.py` visar fasfel upp till ca 16 h, vilket ger upp till ca 30 min fel pa manklockan.
2. **Upp- och nedgang.** Uddevalla ligger pa 58,35 N. Hur lange manen ar uppe beror pa latitud och manens deklination, inte bara pa skillnaden mot solen. Pa var latitud kan det skilja flera timmar fran "solens schema".
3. **Solen ar vaggklockan, inte soltid.** Uddevalla (11,94 E) ligger ca 12 min fore CET:s meridian, och tidsekvationen svanger +-16 min over aret. Idag ar sann soltid ca 4 min fore vaggklockan. Altairs regel just nu: sol = vaggklockan. Andra bara om han vill.
4. **Ljusets restid** 1,28 s finns redan i `moon.toml`. Spelar ingen roll for minuterna.

## Vagar till exakt

- **Meeus, "Astronomical Algorithms", kap. 47.** Manens position med ren Python, inga beroenden. Ca 100 rader tabeller. Noggrannhet ca 10 bagsekunder, langt battre an minuter.
- **Skyfield** (`pip install skyfield` + JPL-filen de421.bsp, ca 17 MB). Exakt, och ger manens upp- och nedgang for en plats direkt. Bryter mot "inga beroenden".

Forslag: Meeus, sa att klockan forblir fristaende.

## Hur det kollas

- Jamfor manens upp- och nedgang for Uddevalla mot timeanddate.com eller USNO for nagra dagar.
- Jamfor fas mot NASA-formorkelserna i `test_moon.py`. Kravet skarps fran 1 dygn till ca 1 timme.

## Kanslan (Altairs ord ovan)

Han ser inte timmen langre nar han kollar klockan. Han ser bara åt, och maste rakna. Spara, kommentera inte.
