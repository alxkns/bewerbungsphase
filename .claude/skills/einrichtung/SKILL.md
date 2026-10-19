---
name: einrichtung
description: Ersteinrichtung für neue Nutzer. Prüft Voraussetzungen, legt daten/ an, fragt das Suchprofil ab (Position, Ort, Umkreis, Remote, Arbeitszeit, Gehalt, Ausschlüsse), baut aus dem hochgeladenen Lebenslauf (PDF/Word) den Master-Lebenslauf und den Briefkopf und macht einen PDF-Probedruck; richtet Tracker, Dashboard und geplante Routinen ein (Claude-App oder cron mit beliebiger KI). Nutzen beim ersten Start, wenn daten/profil.md fehlt, bei „richte ein“, „los geht's“, „neuer Lebenslauf“ oder „Suchprofil ändern“.
---

# Einrichtung: vom leeren Repo zum ersten Probedruck

Ergebnis: `daten/` mit Suchprofil, Eckdaten im Profil, Master-Lebenslauf, Briefkopf und Assets. Danach folgen die Skills `marktanalyse` und `kennenlernen`.

Grundregel wie überall: **nichts erfinden.** Was nicht im Lebenslauf steht und der Nutzer nicht gesagt hat, bleibt leer oder wird gefragt. Antworten des Nutzers sinngemäß und mit Datum eintragen: `(Nutzer, TT.MM.JJJJ)`.

Gibt es `daten/` schon: nur die fehlenden oder gewünschten Schritte machen, nichts überschreiben, ohne zu fragen. „Neuer Lebenslauf“ → Schritt 4 und 5, „Suchprofil ändern“ → Schritt 3.

## 1. Voraussetzungen prüfen

```bash
test -x "${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}" && echo "Chrome ok" || echo "Chrome fehlt"
for t in pdfunite pdftoppm pdftotext; do command -v $t >/dev/null && echo "$t ok" || echo "$t fehlt"; done
```

Fehlt etwas: dem Nutzer den Befehl nennen, nicht selbst installieren.
- poppler: `brew install poppler` (Linux: `apt install poppler-utils`)
- Chrome: installieren oder Pfad per `CHROME=/pfad/zu/chrome` setzen

## 2. Ordner anlegen

```bash
mkdir -p daten/bewerbungen/_vorlage/assets
cp -n vorlagen/profil.md vorlagen/suchprofil.md vorlagen/prozess-learnings.md daten/
cp -n vorlagen/lebenslauf.html vorlagen/anschreiben.html daten/bewerbungen/_vorlage/
```

`cp -n` überschreibt nichts, was schon da ist.

## 3. Suchprofil abfragen → `daten/suchprofil.md`

Kurz erklären, was gleich passiert (Suchprofil, dann Lebenslauf), dann in zwei Runden fragen. Freitext im Chat, feste Auswahl als Auswahlfrage (siehe `AGENTS.md`, „Werkzeuge“).

**Runde 1, im Chat (Freitext, eine Nachricht):**
1. Welche Position(en) suchst du? Gern mehrere Titel oder eine Beschreibung der Arbeit.
2. Wohnort (Stadt reicht)?
3. Was willst du auf keinen Fall (Branchen, Firmenarten, Aufgaben, Bedingungen)?
4. Was wäre ok, aber nicht ideal (z. B. befristet, Pendeln, viel Englisch, Reisen)?
5. Wo arbeitest du am liebsten (Firmengröße, Branche, Teamform)?
6. Gehaltsvorstellung brutto im Jahr: Wunsch und Untergrenze? (Unsicher ist ok, dann später Skill `gehaltsverhandlung`.)
7. Frühester Eintritt und Kündigungsfrist?

**Runde 2, als Auswahlfragen:**
- Umkreis für Stellen mit Präsenz: 10 km · 25 km · 50 km · 100 km
- Arbeitsmodell: vor Ort ok · hybrid · nur remote · egal
- Außerhalb des Umkreises: nur vollständig remote · auch hybrid mit Pendeln · gar nicht
- Arbeitszeit: Vollzeit · Teilzeit (ab wie vielen Std. per „Other“) · beides

Daraus `daten/suchprofil.md` füllen:
- **Ort und Arbeitsmodell:** alle Antworten aus Runde 2, auch die Arbeitszeit. Die Arbeitszeit ist kein eigener Ausschluss-Eintrag.
- **Zielrollen:** die Positionen aus Frage 1, zusätzlich in `daten/profil.md` → „Zielrollen“. **Wunschumfeld:** Frage 5.
- **Suchbegriffe:** aus den Positionen 5–10 kurze Begriffe aus ein bis zwei Wörtern ableiten. Jobbörsen suchen wörtlich: Zusammengesetzte Wörter getrennt schreiben („Kampagnen Manager“ statt „Kampagnenmanager“), die männliche Form reicht, Reihenfolge ist egal. Deutsche und englische Titel, wenn der Markt beide nutzt. Dem Nutzer zur Bestätigung zeigen. Die Marktanalyse schärft sie später nach.
- **Harte Ausschlüsse:** nur, was der Nutzer in Frage 3 genannt hat, plus Ortsregel aus Runde 2. Nichts dazu erfinden.
- **Nur als Risiko markieren:** Frage 4.
- **Match-Grenze:** 70 % als Standard, erklären, dass der Nutzer sie ändern kann.
- **Tracker:** leer lassen (füllt Schritt 7).
- **Quellen:** Bundesagentur und XING/StepStone auf „ja“. „Eigene Quellen“ nur füllen, wenn der Nutzer selbst welche nennt (siehe README, „Genauer recherchieren“).

Gehalt, Eintritt, Kündigungsfrist, Ort/Remote und Arbeitszeit zusätzlich in `daten/profil.md` → „Eckdaten“.

## 4. Lebenslauf einlesen → Master-Lebenslauf

Nutzer um den Lebenslauf bitten (Pfad zur Datei oder in den Chat ziehen). Text holen:

```bash
pdftotext -layout "<lebenslauf.pdf>" <scratchpad>/cv.txt      # PDF
textutil -convert txt -stdout "<lebenslauf.docx>" > <scratchpad>/cv.txt   # Word (macOS)
```

Ist der PDF-Text leer oder zerstückelt (Scan, Grafik-Lebenslauf): die PDF seitenweise als Bild ansehen (z. B. `pdftoppm -r 80 -png`) und daraus lesen. Bei Mehrspalten-Layouts immer zusätzlich das PDF ansehen, damit Zeiträume den richtigen Stationen zugeordnet werden.

`daten/bewerbungen/_vorlage/lebenslauf.html` aus dem Gerüst befüllen:
- `{Platzhalter}` ersetzen, Abschnitte nach Bedarf wiederholen (`.eintrag` je Station, `<li>` je Stichpunkt). Klassen aus `vorlagen/style.css`, keine Inline-Styles.
- **Deutsches Format:** antichronologisch, `MM/JJJJ`, kein Geburtsdatum, keine Konfession, kein Familienstand (außer der Nutzer will es ausdrücklich).
- **Zeitangaben:** `MM/JJJJ`, bei Schule und Abschlüssen ohne Monat im Original nur das Jahr. Erklärte Lücken (Sabbatical, Elternzeit, Pflege) als kompakter Eintrag in die Berufserfahrung (`.eintrag kompakt`), ein Halbsatz, ohne Rechtfertigung.
- **Inhalt 1:1 aus dem Lebenslauf.** Umformulieren nur sprachlich (Stichpunkte statt Fließtext, aktive Verben), keine neuen Zahlen, Tools oder Ergebnisse. Der Master darf länger als 2 Seiten sein, gekürzt wird pro Bewerbung.
- **Profiltext:** aus dem Lebenslauf zusammenfassen, nur Verben und Umfang, die dort stehen („koordiniert“ bleibt „koordiniert“, nicht „verantwortet“). Kein Entwurfs-Vermerk ins HTML (würde mitgedruckt), stattdessen in `profil.md` → „Offen aus der Einrichtung“: „Profiltext im Lebenslauf ist Entwurf“.
- **Englischer Lebenslauf:** Inhalt übersetzen, Firmennamen und Titel im Original lassen, wenn sie so geführt werden.

Danach eine Liste **Unklar im Lebenslauf** für den Nutzer (Lücken > 3 Monate, Stationen ohne Aufgaben, Abkürzungen, fehlende Zeiträume, widersprüchliche Angaben). Antworten in den Master, offene Punkte in `profil.md` → „Offen aus der Einrichtung“ (dort holt `kennenlernen` sie ab).

**Eckdaten** aus dem Lebenslauf in `profil.md` übernehmen: Name, Anschrift, Telefon, E-Mail, Sprachen. Unter „Positionierung“ einen Entwurf aus Lebenslauf + gesuchter Position, markiert mit „Entwurf, im Kennenlernen bestätigen“.

## 5. Briefkopf und Assets

- `daten/bewerbungen/_vorlage/anschreiben.html`: `{Name}`, `{Untertitel}` (Zielrolle, kurz), `{Straße}`, `{PLZ Ort}`, `{Telefon}`, `{E-Mail}`, `{Ort}` ersetzen. Die `[eckigen]` Platzhalter bleiben, die füllt `anschreiben` pro Bewerbung.
- **Foto** (in Deutschland üblich, nicht Pflicht): Nutzer fragen. Ja → als `daten/bewerbungen/_vorlage/assets/foto.jpg` speichern (Hochformat, ca. 3:4). Nein → Zeile `<img class="foto" …>` im Master löschen.
- **Unterschrift:** Bild mit transparentem oder weißem Hintergrund als `assets/unterschrift.png`. Keins da → Nutzer kann auf Papier unterschreiben und abfotografieren, oder die beiden `<img class="unterschrift" …>` (Master und Briefkopf) löschen. Nie eine Unterschrift erzeugen.

## 6. Probedruck

```bash
T=daten/bewerbungen/0000-00-00_Probedruck
mkdir -p "$T" && cp daten/bewerbungen/_vorlage/*.html "$T"/
.claude/skills/bewerbung/pdf.sh "$T"
pdftoppm -r 50 -png "$T"/Lebenslauf_*.pdf <scratchpad>/probe
pdftoppm -r 50 -png "$T"/Anschreiben_*.pdf <scratchpad>/probe-brief
```

`pdf.sh` baut zusätzlich eine Mappe `Bewerbung_Probedruck_<Name>.pdf`, das ist normal.

Vorschau-PNGs ansehen: Kopf, Foto, Unterschrift, Umbrüche, keine `{Platzhalter}` mehr außer den `[eckigen]` im Anschreiben. Fehler beheben, dann dem Nutzer die erste Seite des Lebenslaufs zeigen und fragen, ob Inhalt und Kopf stimmen. Erst nach seinem Ok den Ordner `0000-00-00_Probedruck` löschen.

## 7. Tracker und Dashboard

Der Tracker ist die Liste aller Bewerbungen. Das Dashboard (`dashboard/tracker.html`) zeigt Kennzahlen, Trichter, Versand pro Woche und eine Tabelle, in der der Nutzer Status ändert und Vorschläge per „Bewerbung erstellen“ anfordert. Die Routinen lesen und schreiben dieselbe Liste. Nutzer fragen (Auswahlfrage):

- **Lokal (Standard):** Datei `daten/tracker.sqlite`, funktioniert mit jeder KI und offline. Dashboard im Browser auf diesem Rechner.
- **claude.ai:** privates Artifact mit Datenbank, auch am Handy. Nur, wenn der Nutzer mit Claude arbeitet und ein claude.ai-Konto mit Artifacts hat.

**Lokal:**
1. `python3 tracker/tracker.py list` einmal ausführen (legt die Datei an, Ausgabe `[]`).
2. In `daten/suchprofil.md` → „Tracker“: `Art: lokal`.
3. Dem Nutzer zeigen, wie er das Dashboard öffnet: `python3 tracker/tracker.py serve`, dann http://localhost:8765 (in Claude Code: Startkonfiguration „tracker“ aus `.claude/launch.json`). Kurz selbst starten, Seite laden, wieder beenden.

**claude.ai** (nur mit Claude):
1. Skill `artifact-capabilities` laden (Pflicht, bevor `capabilities` übergeben werden).
2. `Artifact` publish mit `file_path` `dashboard/tracker.html`, `icon` „chart“, `description` „Bewerbungen, Status und Quoten auf einen Blick“ und
   `capabilities` `{"db": {"rules": [{"path": "", "read": "view", "write": "owner"}]}, "user": {}}`.
3. In `daten/suchprofil.md` → „Tracker“: `Art: claude.ai` und die URL aus dem Ergebnis. Anbieten, das Dashboard anzupinnen (nur auf Ja).
4. Steht `capabilities` laut Ergebnis nicht zur Verfügung: auf „Lokal“ wechseln.

Spätere Updates von `dashboard/tracker.html` (nach `git pull`): lokal sofort aktiv; claude.ai erneut publishen mit `url` = Tracker-URL, die Daten bleiben erhalten. Wechsel von claude.ai zu lokal: Datenbank mit `ArtifactData` `list` (`out_dir`) exportieren, dann `python3 tracker/tracker.py import <out_dir>/bewerbungen`.

## 8. Automatik (geplante Routinen)

Nur mit Tracker aus Schritt 7. Fragen, welche Routinen laufen sollen (Mehrfachauswahl):

| Routine | Skill | Vorschlag Zeitplan | cron |
|---|---|---|---|
| Neue Stellen suchen und vorschlagen | `stellensuche` | werktags 7 Uhr | `0 7 * * 1-5` |
| Angeforderte Bewerbungen bauen | `bewerbungen-erstellen` | stündlich 8–22 Uhr | `0 8-22 * * *` |
| Gmail nach Antworten durchsuchen | `gmail-abgleich` | 8 und 18 Uhr | `0 8,18 * * *` |

Gmail-Abgleich nur anbieten, wenn das Werkzeug, das die Routine ausführt, Gmail lesen kann (in Claude: Gmail-Connector).

Der Auftrag jeder Routine ist immer derselbe, ohne eigene Logik (nach `git pull` gilt sofort die neue Fassung des Skills; `<Projektordner>` = absoluter Pfad per `pwd`):
```
Projektordner: <Projektordner>
Wechsle per cd in diesen Ordner und arbeite nur dort. Lies .claude/skills/<skill>/SKILL.md und befolge es vollständig. Antworte auf Deutsch, kurz.
```

**Weg A: Claude-Desktop-App** (wenn diese Sitzung dort läuft und es das Werkzeug für geplante Aufgaben gibt, `mcp__scheduled-tasks__…`, per ToolSearch laden):
1. Erst `list_scheduled_tasks`: Gibt es schon eine Aufgabe mit derselben `taskId`, den Nutzer fragen, nie überschreiben.
2. Je Routine `create_scheduled_task` mit `taskId` `bewerbung-<skill>`, `title` und `description` aus der Tabelle, `cronExpression`, `prompt` = Auftrag oben.
3. Hinweise: Routinen laufen nur bei offener App, verpasste holt sie beim nächsten Start nach. Ohne passenden Berechtigungsmodus bleiben Läufe an Freigaben hängen: Routinen im Auto-Modus anlegen oder die Freigaben beim ersten Lauf erteilen.

**Weg B: Systemzeitplan mit beliebiger KI-Kommandozeile** (Claude Code, Codex, Gemini CLI …; macOS/Linux per `cron`):
1. Absoluten Pfad der Kommandozeile ermitteln (`command -v claude`, `command -v codex` …), cron kennt den normalen PATH nicht.
2. Je Routine eine Zeile, Muster:
   `<cron> cd "<Projektordner>" && <befehl> >> daten/logs/<skill>.log 2>&1`
   Der `<befehl>` führt den Auftrag oben ohne Rückfragen aus. Beispiele (Optionen ändern sich, vorher mit `--help` prüfen):
   - Claude Code: `/pfad/claude -p "<Auftrag>" --permission-mode acceptEdits --allowedTools "Bash Read Write Edit WebFetch WebSearch"`
   - Codex: `/pfad/codex exec --full-auto "<Auftrag>"`
   - Gemini CLI: `/pfad/gemini --yolo -p "<Auftrag>"`
3. Dem Nutzer die fertigen Zeilen zeigen und erklären: Die KI arbeitet dann unbeaufsichtigt mit Schreib- und Shell-Rechten im Projektordner. Erst nach seinem ausdrücklichen Ok eintragen: `mkdir -p daten/logs`, dann `(crontab -l 2>/dev/null; echo '<zeile>') | crontab -`. Bestehende Einträge nie entfernen.
4. Hinweise: Der Rechner muss zur geplanten Zeit an sein. Unter macOS braucht `cron` ggf. „Festplattenvollzugriff“ (Systemeinstellungen → Datenschutz), sonst darf es nicht in `Dokumente` schreiben; das richtet der Nutzer selbst ein. Logs liegen in `daten/logs/`.

## 9. Übergabe

Kurz im Chat: was eingerichtet ist, was fehlt (Voraussetzungen, Foto, Unterschrift, offene Punkte im Lebenslauf, Tracker, Routinen). Dann den nächsten Schritt vorschlagen:
1. `marktanalyse`: passende Anzeigen sammeln und auswerten, was der Markt verlangt
2. `kennenlernen`: Interview, das `profil.md` füllt (braucht die Marktanalyse für gezielte Fragen)

Erst danach entstehen gute Anschreiben. Eine Bewerbung vorher geht, wird aber generisch.
