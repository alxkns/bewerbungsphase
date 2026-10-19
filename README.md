# Bewerbungsphase

Claude-Code-Skills, die deutsche Bewerbungen von der Stellenanzeige bis zur fertigen PDF-Mappe bauen: Analyse, Lebenslauf, Anschreiben, Recruiter-Check, Gespräch, Gehalt. Es wird nichts erfunden, alle Fakten kommen aus deinem Profil.

## Aufbau

| Ordner | Inhalt | Im Git |
|---|---|---|
| `.claude/skills/` | Die Methode: Skills für jeden Schritt | ja |
| `vorlagen/` | Layout (`style.css`) und leere Vorlagen für Profil, Suchprofil, Lebenslauf, Anschreiben, Lern-Datei der Routinen | ja |
| `dashboard/` | Bewerbungs-Tracker (`tracker.html`), wird als eigenes privates claude.ai-Artifact veröffentlicht | ja |
| `daten/` | Deine Daten: `profil.md`, `suchprofil.md`, Master-Lebenslauf, Foto, Unterschrift, alle Bewerbungen | **nein** (`.gitignore`) |

Skills lesen nur aus `daten/`. Updates der Skills überschreiben deshalb nie dein Profil.

## Los geht's

Repo klonen, Claude Code im Ordner starten und nacheinander:

1. **„Richte mich ein“** (Skill `einrichtung`): prüft die Voraussetzungen, fragt dein Suchprofil ab (Position, Ort, Umkreis, Remote, Gehalt, Ausschlüsse), baut aus deinem Lebenslauf (PDF/Word) den Master-Lebenslauf, macht einen Probedruck und richtet auf Wunsch Dashboard und Routinen ein.
2. **„Mach die Marktanalyse“** (Skill `marktanalyse`): sammelt 20–40 passende Anzeigen und wertet aus, was die Stellen wirklich verlangen, welche Eigenschaften und Begriffe gefragt sind und wo dein Lebenslauf passt oder Lücken hat.
3. **„Lern mich kennen“** (Skill `kennenlernen`): Interview in Runden, das dein Profil füllt. Darf über mehrere Sitzungen gehen. Je gründlicher, desto persönlicher die Anschreiben.

## Dashboard und Routinen

Das Dashboard zeigt alle Bewerbungen mit Status, Quoten und Versand pro Woche. Jeder Nutzer bekommt bei der Einrichtung eine eigene, private Kopie auf claude.ai, auch am Handy nutzbar.

Drei Routinen laufen auf Wunsch automatisch (geplante Aufgaben in der Claude-Desktop-App):

| Skill | Was | Standard |
|---|---|---|
| `stellensuche` | sucht neue Stellen nach deinem Suchprofil und schlägt passende im Dashboard vor | werktags 7 Uhr |
| `bewerbungen-erstellen` | baut die Mappe, sobald du im Dashboard „Bewerbung erstellen“ klickst | stündlich 8–22 Uhr |
| `gmail-abgleich` | trägt Versand, Einladungen und Absagen aus Gmail ein (Gmail-Connector nötig) | 8 und 18 Uhr |

Die geplanten Aufgaben verweisen nur auf die Skills. Nach `git pull` laufen sie mit der neuen Fassung. Alle Skills lassen sich auch von Hand starten („such neue Stellen“). Routinen laufen nur, solange die Desktop-App offen ist. Gesendet wird nie etwas, Abschicken machst du selbst.

## Genauer recherchieren

Die Stellensuche nutzt von sich aus nur frei zugängliche Quellen: die Jobbörse der Bundesagentur für Arbeit (offizielle Schnittstelle, enthält viele Partner-Anzeigen von StepStone, Indeed u. a.) sowie die öffentlichen Suchseiten von XING und StepStone. Damit ist ein großer Teil des Marktes abgedeckt, aber nicht alles. So wird die Suche genauer:

- **Suchbegriffe schärfen.** Jobbörsen suchen wörtlich. Kurze Begriffe aus ein bis zwei Wörtern, zusammengesetzte Wörter getrennt („Kampagnen Manager“), deutsche und englische Titel. Nach der Marktanalyse die Begriffe übernehmen, die dort häufig vorkommen.
- **Zeitraum.** Viele Anzeigen werden nur neu geschaltet. Wer zu wenig findet, stellt im Suchprofil 14 statt 7 Tage ein.
- **Selbst gefundene Stellen schicken.** Was du auf LinkedIn, Indeed, in Branchenportalen oder über Empfehlungen findest: Link an Claude schicken („bewirb mich bei …“ oder „trag das als Vorschlag ein“). Das ist oft der beste Weg zu Stellen, die keine freie Quelle führt.
- **Job-Alerts per Mail.** Bei LinkedIn, Indeed oder StepStone Suchaufträge mit deinen Suchbegriffen anlegen und die Mails selbst durchsehen.
- **Zielfirmen direkt.** Viele Stellen stehen nur auf der Karriereseite. Eine Liste von Wunschfirmen unter „Eigene Quellen“ im Suchprofil eintragen, dann prüft die Stellensuche deren Karriereseiten mit.
- **Nachsehen, was aussortiert wurde.** `daten/bewerbungen/stellensuche-verworfen.md` zeigt jede gesichtete, aber nicht vorgeschlagene Stelle mit Grund. Fehlt dir eine Stelle, steht dort, ob sie übersehen oder bewusst aussortiert wurde.
- **Weitere Plattformen anbinden (auf eigenes Risiko).** LinkedIn und Indeed haben keine offene Schnittstelle. Wer sie automatisch durchsuchen will, braucht einen Scraping-Dienst (z. B. Apify) als Connector. Das kostet pro Suchlauf und verstößt in der Regel gegen die Nutzungsbedingungen der Plattformen. Das Repo liefert dafür bewusst nichts mit. Wer es trotzdem nutzt, beschreibt Dienst, Einstellungen und Kostengrenze unter „Eigene Quellen“ in `daten/suchprofil.md`.

## Voraussetzungen

- Claude Code in der Claude-Desktop-App (für Routinen), claude.ai-Konto mit Artifacts (für das Dashboard)
- Google Chrome (PDF-Druck; anderer Pfad: `CHROME=/pfad/zu/chrome`)
- poppler (`brew install poppler`) für `pdfunite`, `pdftoppm`, `pdftotext`

Enthalten: Skill `humanizer-de` (MIT, Martin Moeller, auf Basis von blader/humanizer) für den KI-Sprache-Check, Lizenz in `.claude/skills/humanizer-de/LICENSE`.

## Nutzung

Stellenanzeige (Link, Text oder PDF) schicken und „bewirb mich“ sagen. Skill `bewerbung` steuert den Rest, Ergebnis liegt in `daten/bewerbungen/<datum>_<firma>/`.
