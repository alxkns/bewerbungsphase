---
name: stellensuche
description: Neue Stellenanzeigen nach daten/suchprofil.md suchen, nach Skill stellenanalyse bewerten und die passenden als „Vorschlag“ in den Bewerbungs-Tracker eintragen; Aussortiertes protokollieren. Läuft als geplante Routine (werktags morgens) oder auf Zuruf („such neue Stellen“, „Stellensuche“). Bewirbt sich nicht und schreibt keine Anschreiben.
---

# Stellensuche: neue Stellen finden und vorschlagen

Antworte auf Deutsch, kurz. Du bewirbst dich NICHT, schreibst keine Anschreiben und versendest nichts.

Alle Pfade relativ zum Projektordner (im geplanten Lauf nennt der Auftrag ihn, vorher `cd` dorthin).

**Vorher lesen:**
- `daten/prozess-learnings.md`: „Gültige Workarounds“ befolgen, sie haben bei technischen Details Vorrang.
- `daten/suchprofil.md`: Ort, Umkreis, Arbeitsmodell, Suchbegriffe, Ausschlüsse, Risiken, Quellen, Match-Grenze, Zeitraum, Tracker
- `.claude/skills/stellenanalyse/SKILL.md` (Bewertung, Match-Formel: Muss 70 %, Kann 30 %, ehrlich)
- `daten/profil.md` und `daten/bewerbungen/_vorlage/lebenslauf.html` (einzige Faktenquelle)
- falls vorhanden: `daten/bewerbungen/absagen-analyse.md` (Learnings aus Absagen)

Ist kein Tracker eingerichtet: Vorschläge nur als Ordner anlegen und am Ende auflisten.

Tracker lesen und schreiben wie im Skill `bewerbung`, Abschnitt „Tracker pflegen“ (lokal per `tracker/tracker.py` oder claude.ai per ArtifactData, je nach `daten/suchprofil.md` → „Tracker“). Websuche und Seitenabruf nutzen, falls das Werkzeug sie hat. Rohdaten gern per `curl` (Browser-User-Agent setzen).

## Quellen

Nur die Quellen, die in `suchprofil.md` → „Quellen“ auf „ja“ stehen, plus „Eigene Quellen“. Je Suchbegriff einzeln, jeweils im Umkreis UND remote. Technische Details (Parameter, Felder, Fallen) stehen in `daten/prozess-learnings.md`.

1. **Bundesagentur für Arbeit** (immer, kostenlos, enthält viele Partner-Anzeigen von StepStone, Indeed u. a.):
   `curl -s -H 'X-API-Key: jobboerse-jobsuche' 'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs?was=<Begriff>&wo=<Wohnort>&umkreis=<km>&veroeffentlichtseit=<Tage>&size=100&page=1'`. Remote ohne `wo` mit `was=<Begriff>%20remote`.
2. **XING und StepStone-Suchseiten** (kostenlos, per curl, siehe Workarounds).
3. **Eigene Quellen:** nur was der Nutzer in `suchprofil.md` → „Eigene Quellen“ selbst beschrieben hat, genau so, wie es dort steht. Fehlt ein dafür nötiger Connector: überspringen und in der Ausgabe melden.

## Ablauf

1. **Bekannte Stellen:** Alle Tracker-Dokumente lesen (`list`) und `daten/bewerbungen/stellensuche-verworfen.md` (falls vorhanden). Jede Stelle, die dort schon steht, egal mit welchem Status (auch „Verworfen“), wird nicht erneut vorgeschlagen. Abgleich über Firma (Kurzname) + Stellentitel, nicht nur über den Link.
2. **Abfragen:** Quellen oben, Titel grob vorfiltern (Praktikum, Werkstudent, Ausbildung, offensichtlich andere Rolle raus), Dubletten über Quellen hinweg zusammenführen, Anzeigen außerhalb des Zeitraums laut `datumErsteVeroeffentlichung` bzw. Datum der Quelle verwerfen. Für Kandidaten die Originalanzeige (Karriereseite/ATS) holen.
3. **Ortsregel** aus `suchprofil.md` streng anwenden: Arbeitsmodell in der Originalanzeige UND im ATS-Tag prüfen (JOIN, Personio u. a.); widersprechen sie sich, gilt das strengere. Sagt die Anzeige im Umkreis nichts zu Homeoffice, aufnehmen und in `notiz` „Homeoffice klären“.
4. **Bewerten** nach `stellenanalyse`. Nur aufnehmen bei Match ≥ Grenze aus `suchprofil.md` und keinem harten Ausschluss. Risiken in die `notiz`.
5. **Je aufgenommene Stelle:**
   - `doc_id` = `JJJJ-MM-TT_Firmenname` (heute, nur `A-Z a-z 0-9 _ -`, Umlaute ersetzen). Ordner `daten/bewerbungen/<doc_id>/` anlegen.
   - Anzeige komplett als `anzeige.md` (Kopf: Quelle-URL, Abrufdatum), Analyse als `analyse.md` (Format aus `stellenanalyse`, Zeile „**Match: NN %**“).
   - Tracker-Dokument anlegen (`set`): `{"firma", "stelle" (exakt wie Anzeige), "ort" (inkl. remote/hybrid/unklar), "weg" (Portal/E-Mail), "match" (Zahl), "score": null, "status": "Vorschlag", "vorgeschlagen_am": heute, "entworfen_am": null, "versendet_am": null, "einladung_am": null, "antwort_am": null, "naechster_schritt": "Prüfen: Bewerbung erstellen oder verwerfen", "link": Original-URL, "notiz": 1–2 Sätze: warum passend, größte Lücke, Gehalt falls genannt, ggf. „Homeoffice klären“}`. (claude.ai: mehrere als `batch`).
6. **Verworfene protokollieren:** Jede gesichtete Kandidatin, die nach Lesen der Anzeige nicht aufgenommen wird (nicht reine Titel-Treffer), in `daten/bewerbungen/stellensuche-verworfen.md`: unter `## JJJJ-MM-TT` je eine Zeile `- Firma · Stelle · Quelle · Link · Grund (z. B. Match 55 %, hybrid außerhalb Umkreis, älter als Zeitraum)`. Neueste oben, Einträge älter als 60 Tage löschen. So sieht der Nutzer, ob eine Stelle übersehen oder bewusst aussortiert wurde.
7. **Keine neuen Vorschläge:** nichts in den Tracker schreiben, Verworfen-Datei trotzdem pflegen.
8. **Lern-Datei:** am Ende Log-Eintrag in `daten/prozess-learnings.md` nach den Regeln oben in der Datei. Suchprofil, Ausschlüsse und Match-Grenze nie selbst ändern, Ideen dazu unter „Vorschläge an den Nutzer“.

## Ausgabe
Kurze Tabelle der neuen Vorschläge (Firma, Stelle, Ort, Match), Anzahl gesichteter Anzeigen je Quelle, Anzahl verworfener mit den 3 häufigsten Gründen, welche Quelle nicht funktioniert hat oder übersprungen wurde.
