---
name: bewerbungen-erstellen
description: Alle Bewerbungen mit Status „Angefordert“ im Bewerbungs-Tracker komplett bauen (Analyse, Lebenslauf, Anschreiben, KI-Sprache-Check, Recruiter-Check, PDFs, portal.md) und auf „Entworfen“ setzen. Läuft als geplante Routine (stündlich tagsüber) oder auf Zuruf („bau die angeforderten Bewerbungen“). Versendet nie etwas.
---

# Bewerbungen erstellen: angeforderte Mappen bauen

Der Nutzer klickt im Dashboard bei einem Vorschlag „Bewerbung erstellen“ (Status → „Angefordert“). Dieser Skill baut daraus die fertige Mappe. Antworte auf Deutsch, kurz. Du versendest NIE etwas und schreibst keine Mails; Absenden macht der Nutzer selbst.

Alle Pfade relativ zum Projektordner (im geplanten Lauf nennt der Auftrag ihn, vorher `cd` dorthin).

**Vorher lesen:** `daten/prozess-learnings.md` („Gültige Workarounds“ befolgen), `daten/suchprofil.md` → „Tracker“. Ist keiner eingerichtet: mit einem Satz beenden („Kein Tracker eingerichtet“).

Tracker lesen und schreiben wie im Skill `bewerbung`, Abschnitt „Tracker pflegen“ (lokal per `tracker/tracker.py` oder claude.ai per ArtifactData, je nach `daten/suchprofil.md` → „Tracker“). Schreiben immer mit `update`, nur geänderte Felder, Version aus dem letzten Lesen; bei Konflikt neu lesen.

## Ablauf

1. Alle mit Status „Angefordert“ lesen (lokal `list --status Angefordert`, claude.ai `query` mit `where: [["status", "==", "Angefordert"]]`). Leer → Log-Eintrag „ohne Befund“, mit einem Satz beenden.
2. Für jedes Dokument:
   a. Sofort `status` = „In Arbeit“ setzen (verhindert Doppelbearbeitung durch einen parallelen Lauf).
   b. Ordner `daten/bewerbungen/<id>/` verwenden (dort liegen meist schon `anzeige.md` und `analyse.md`). Fehlen sie: Anzeige über `link` holen, `anzeige.md` speichern, Analyse nach Skill `stellenanalyse` als `analyse.md`.
   c. Skill `bewerbung` ab Schritt 3 vollständig befolgen (dort genannte Dateien vorher lesen: `stil.md`, `profil.md`, Master-Lebenslauf, Skills `lebenslauf-anpassen`, `anschreiben`, KI-Sprache-Check, `pdf.sh`, Sichtprüfung).
   d. Recruiter-Check nach Skill `recruiter`, wenn Match ≥ Grenze aus `suchprofil.md`, höchstens 2 Verbesserungsrunden. Fakten-Fragen kannst du hier nicht stellen: nicht erfinden, sondern sammeln (sie landen später im Skill `kennenlernen`).
   e. Fehlende Eckdaten (z. B. Gehaltsfeld): Werte aus `profil.md`. Gibt es dort keinen Wert: offen lassen und notieren.
   f. Tracker `update`: `status` „Entworfen“, `entworfen_am` heute, `score` (beste Recruiter-Note als Zahl, die der Endfassung, sonst null), `naechster_schritt` (z. B. „Mappe prüfen und über Personio absenden“, inkl. Gehalt/Eintritt, falls ein Formular sie verlangt), `notiz` um „Recruiter-Check: a → b → c“ und offene Fakten-Fragen ergänzen (bestehende Notiz behalten).
   g. Scheitert etwas (Anzeige offline, harter Ausschluss entdeckt, z. B. Pflicht-Upload, den der Nutzer laut `profil.md` nicht liefert): `status` zurück auf „Vorschlag“ und den Grund in `naechster_schritt`. Nichts schönrechnen.
3. **Mehrere Anforderungen:** pro Ordner einen Subagenten, höchstens ca. 7 parallel, frei gewordene Plätze mit dem nächsten Ordner belegen. Tracker-Updates nur im Hauptlauf. Ergebnisse der Subagenten selbst prüfen (Seitenzahl, Sichtprüfung, keine Fakten außerhalb von Master und `profil.md`).
4. **Lern-Datei:** am Ende Log-Eintrag in `daten/prozess-learnings.md` nach den Regeln oben in der Datei.

## Ausgabe
Pro Bewerbung: Firma, Match, Score, Pfad zur Mappe `Bewerbung_<Firma>_<Name>.pdf`, offene Fragen.
