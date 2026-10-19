# Bewerbungsphase

Claude-Code-Skills, die deutsche Bewerbungen von der Stellenanzeige bis zur fertigen PDF-Mappe bauen: Analyse, Lebenslauf, Anschreiben, Recruiter-Check, Gespräch, Gehalt. Es wird nichts erfunden, alle Fakten kommen aus deinem Profil.

## Aufbau

| Ordner | Inhalt | Im Git |
|---|---|---|
| `.claude/skills/` | Die Methode: Skills für jeden Schritt | ja |
| `vorlagen/` | Layout (`style.css`) und leere Vorlagen für Profil, Suchprofil, Lebenslauf, Anschreiben | ja |
| `daten/` | Deine Daten: `profil.md`, `suchprofil.md`, Master-Lebenslauf, Foto, Unterschrift, alle Bewerbungen | **nein** (`.gitignore`) |

Skills lesen nur aus `daten/`. Updates der Skills überschreiben deshalb nie dein Profil.

## Einrichtung (vorerst von Hand)

```bash
mkdir -p daten/bewerbungen/_vorlage/assets
cp vorlagen/profil.md vorlagen/suchprofil.md daten/
cp vorlagen/lebenslauf.html vorlagen/anschreiben.html daten/bewerbungen/_vorlage/
```

Dann in Claude Code: Lebenslauf (PDF/Word) hochladen und `daten/bewerbungen/_vorlage/lebenslauf.html` daraus befüllen lassen, `{Platzhalter}` im Anschreiben ersetzen, `foto.jpg` (optional) und `unterschrift.png` nach `daten/bewerbungen/_vorlage/assets/` legen, `profil.md` und `suchprofil.md` im Gespräch füllen lassen.

## Voraussetzungen

- Claude Code
- Google Chrome (PDF-Druck; anderer Pfad: `CHROME=/pfad/zu/chrome`)
- poppler (`brew install poppler`) für `pdfunite`, `pdftoppm`, `pdftotext`
- Schrift Manrope (installiert, sonst Ersatzschrift)

Enthalten: Skill `humanizer-de` (MIT, Martin Moeller, auf Basis von blader/humanizer) für den KI-Sprache-Check, Lizenz in `.claude/skills/humanizer-de/LICENSE`.

## Nutzung

Stellenanzeige (Link, Text oder PDF) schicken und „bewirb mich“ sagen. Skill `bewerbung` steuert den Rest, Ergebnis liegt in `daten/bewerbungen/<datum>_<firma>/`.
