---
name: einrichtung
description: Ersteinrichtung für neue Nutzer. Prüft Voraussetzungen, legt daten/ an, fragt das Suchprofil ab (Position, Ort, Umkreis, Remote, Arbeitszeit, Gehalt, Ausschlüsse), baut aus dem hochgeladenen Lebenslauf (PDF/Word) den Master-Lebenslauf und den Briefkopf und macht einen PDF-Probedruck. Nutzen beim ersten Start, wenn daten/profil.md fehlt, bei „richte ein“, „los geht's“, „neuer Lebenslauf“ oder „Suchprofil ändern“.
---

# Einrichtung: vom leeren Repo zum ersten Probedruck

Ergebnis: `daten/` mit Suchprofil, Eckdaten im Profil, Master-Lebenslauf, Briefkopf und Assets. Danach folgen die Skills `marktanalyse` und `kennenlernen`.

Grundregel wie überall: **nichts erfinden.** Was nicht im Lebenslauf steht und der Nutzer nicht gesagt hat, bleibt leer oder wird gefragt. Antworten des Nutzers sinngemäß und mit Datum eintragen: `(Nutzer, TT.MM.JJJJ)`.

Gibt es `daten/` schon: nur die fehlenden oder gewünschten Schritte machen, nichts überschreiben, ohne zu fragen. „Neuer Lebenslauf“ → Schritt 4 und 5, „Suchprofil ändern“ → Schritt 3.

## 1. Voraussetzungen prüfen

```bash
test -x "${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}" && echo "Chrome ok" || echo "Chrome fehlt"
for t in pdfunite pdftoppm pdftotext; do command -v $t >/dev/null && echo "$t ok" || echo "$t fehlt"; done
ls ~/Library/Fonts /Library/Fonts 2>/dev/null | grep -qi manrope && echo "Manrope ok" || echo "Manrope fehlt"
```

Fehlt etwas: dem Nutzer den Befehl nennen, nicht selbst installieren.
- poppler: `brew install poppler` (Linux: `apt install poppler-utils`)
- Chrome: installieren oder Pfad per `CHROME=/pfad/zu/chrome` setzen
- Manrope: von Google Fonts laden und installieren. Ohne Manrope nimmt Chrome eine Ersatzschrift, das Layout verschiebt sich leicht. Kein Abbruchgrund.

## 2. Ordner anlegen

```bash
mkdir -p daten/bewerbungen/_vorlage/assets
cp -n vorlagen/profil.md vorlagen/suchprofil.md daten/
cp -n vorlagen/lebenslauf.html vorlagen/anschreiben.html daten/bewerbungen/_vorlage/
```

`cp -n` überschreibt nichts, was schon da ist.

## 3. Suchprofil abfragen → `daten/suchprofil.md`

Kurz erklären, was gleich passiert (Suchprofil, dann Lebenslauf), dann in zwei Runden fragen. Freitext im Chat, feste Auswahl per `AskUserQuestion` (max. 4 Fragen pro Aufruf).

**Runde 1, im Chat (Freitext, eine Nachricht):**
1. Welche Position(en) suchst du? Gern mehrere Titel oder eine Beschreibung der Arbeit.
2. Wohnort (Stadt reicht)?
3. Was willst du auf keinen Fall (Branchen, Firmenarten, Aufgaben, Bedingungen)?
4. Gehaltsvorstellung brutto im Jahr: Wunsch und Untergrenze? (Unsicher ist ok, dann später Skill `gehaltsverhandlung`.)
5. Frühester Eintritt und Kündigungsfrist?

**Runde 2, per `AskUserQuestion`:**
- Umkreis für Stellen mit Präsenz: 10 km · 25 km · 50 km · 100 km
- Arbeitsmodell: vor Ort ok · hybrid · nur remote · egal
- Außerhalb des Umkreises: nur vollständig remote · auch hybrid mit Pendeln · gar nicht
- Arbeitszeit: Vollzeit · Teilzeit (ab wie vielen Std. per „Other“) · beides

Daraus `daten/suchprofil.md` füllen:
- **Suchbegriffe:** aus den Positionen 5–10 kurze, einzelne Begriffe ableiten (Jobbörsen suchen wörtlich, lange Kombinationen finden nichts). Deutsche und englische Titel, wenn der Markt beide nutzt. Dem Nutzer zur Bestätigung zeigen. Die Marktanalyse schärft sie später nach.
- **Harte Ausschlüsse:** nur, was der Nutzer genannt hat, plus Ortsregel aus Runde 2. Nichts dazu erfinden.
- **Match-Grenze:** 70 % als Standard, erklären, dass der Nutzer sie ändern kann.
- **Tracker:** leer lassen (wird mit dem Dashboard eingerichtet).

Gehalt, Eintritt, Kündigungsfrist, Ort/Remote und Arbeitszeit zusätzlich in `daten/profil.md` → „Eckdaten“.

## 4. Lebenslauf einlesen → Master-Lebenslauf

Nutzer um den Lebenslauf bitten (Pfad zur Datei oder in den Chat ziehen). Text holen:

```bash
pdftotext -layout "<lebenslauf.pdf>" <scratchpad>/cv.txt      # PDF
textutil -convert txt -stdout "<lebenslauf.docx>" > <scratchpad>/cv.txt   # Word (macOS)
```

Ist der PDF-Text leer oder zerstückelt (Scan, Grafik-Lebenslauf): die PDF mit dem Read-Tool seitenweise ansehen und daraus lesen. Bei Mehrspalten-Layouts immer zusätzlich das PDF ansehen, damit Zeiträume den richtigen Stationen zugeordnet werden.

`daten/bewerbungen/_vorlage/lebenslauf.html` aus dem Gerüst befüllen:
- `{Platzhalter}` ersetzen, Abschnitte nach Bedarf wiederholen (`.eintrag` je Station, `<li>` je Stichpunkt). Klassen aus `vorlagen/style.css`, keine Inline-Styles.
- **Deutsches Format:** antichronologisch, `MM/JJJJ`, kein Geburtsdatum, keine Konfession, kein Familienstand (außer der Nutzer will es ausdrücklich).
- **Inhalt 1:1 aus dem Lebenslauf.** Umformulieren nur sprachlich (Stichpunkte statt Fließtext, aktive Verben), keine neuen Zahlen, Tools oder Ergebnisse. Der Master darf länger als 2 Seiten sein, gekürzt wird pro Bewerbung.
- **Profiltext:** aus dem Lebenslauf zusammenfassen, als Entwurf markieren. Er wird nach `kennenlernen` überarbeitet.
- **Englischer Lebenslauf:** Inhalt übersetzen, Firmennamen und Titel im Original lassen, wenn sie so geführt werden.

Danach eine Liste **Unklar im Lebenslauf** für den Nutzer (Lücken > 3 Monate, Stationen ohne Aufgaben, Abkürzungen, fehlende Zeiträume, widersprüchliche Angaben). Antworten in den Master, Rest wandert an `kennenlernen`.

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

Vorschau-PNGs ansehen: Kopf, Foto, Unterschrift, Umbrüche, keine `{Platzhalter}` mehr außer den `[eckigen]` im Anschreiben. Fehler beheben, dann den Ordner `0000-00-00_Probedruck` wieder löschen. Dem Nutzer die erste Seite des Lebenslaufs zeigen und fragen, ob Inhalt und Kopf stimmen.

## 7. Übergabe

Kurz im Chat: was eingerichtet ist, was fehlt (Voraussetzungen, Foto, Unterschrift, offene Punkte im Lebenslauf). Dann den nächsten Schritt vorschlagen:
1. `marktanalyse`: passende Anzeigen sammeln und auswerten, was der Markt verlangt
2. `kennenlernen`: Interview, das `profil.md` füllt (braucht die Marktanalyse für gezielte Fragen)

Erst danach entstehen gute Anschreiben. Eine Bewerbung vorher geht, wird aber generisch.
