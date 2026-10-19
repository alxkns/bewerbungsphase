# Bewerbungsphase

Claude-Code-Skills, die deutsche Bewerbungen von der Stellenanzeige bis zur fertigen PDF-Mappe bauen: Analyse, Lebenslauf, Anschreiben, Recruiter-Check, Gespräch, Gehalt. Es wird nichts erfunden, alle Fakten kommen aus deinem Profil.

## Aufbau

| Ordner | Inhalt | Im Git |
|---|---|---|
| `.claude/skills/` | Die Methode: Skills für jeden Schritt | ja |
| `vorlagen/` | Layout (`style.css`) und leere Vorlagen für Profil, Suchprofil, Lebenslauf, Anschreiben | ja |
| `daten/` | Deine Daten: `profil.md`, `suchprofil.md`, Master-Lebenslauf, Foto, Unterschrift, alle Bewerbungen | **nein** (`.gitignore`) |

Skills lesen nur aus `daten/`. Updates der Skills überschreiben deshalb nie dein Profil.

## Los geht's

Repo klonen, Claude Code im Ordner starten und nacheinander:

1. **„Richte mich ein“** (Skill `einrichtung`): prüft die Voraussetzungen, fragt dein Suchprofil ab (Position, Ort, Umkreis, Remote, Gehalt, Ausschlüsse), baut aus deinem Lebenslauf (PDF/Word) den Master-Lebenslauf und macht einen Probedruck.
2. **„Mach die Marktanalyse“** (Skill `marktanalyse`): sammelt 20–40 passende Anzeigen und wertet aus, was die Stellen wirklich verlangen, welche Eigenschaften und Begriffe gefragt sind und wo dein Lebenslauf passt oder Lücken hat.
3. **„Lern mich kennen“** (Skill `kennenlernen`): Interview in Runden, das dein Profil füllt. Darf über mehrere Sitzungen gehen. Je gründlicher, desto persönlicher die Anschreiben.

## Voraussetzungen

- Claude Code
- Google Chrome (PDF-Druck; anderer Pfad: `CHROME=/pfad/zu/chrome`)
- poppler (`brew install poppler`) für `pdfunite`, `pdftoppm`, `pdftotext`

Enthalten: Skill `humanizer-de` (MIT, Martin Moeller, auf Basis von blader/humanizer) für den KI-Sprache-Check, Lizenz in `.claude/skills/humanizer-de/LICENSE`.

## Nutzung

Stellenanzeige (Link, Text oder PDF) schicken und „bewirb mich“ sagen. Skill `bewerbung` steuert den Rest, Ergebnis liegt in `daten/bewerbungen/<datum>_<firma>/`.
