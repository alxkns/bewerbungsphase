---
name: gmail-abgleich
description: Gmail nach Rückmeldungen auf Bewerbungen durchsuchen (Eingangsbestätigung, Einladung, Absage, Portal-Mails) und den Status im Bewerbungs-Tracker aktualisieren; Bewerbungen außerhalb des Ablaufs nachtragen. Braucht Lesezugriff auf Gmail. Läuft als geplante Routine (z. B. zweimal täglich) oder auf Zuruf („gleich meine Mails ab“). Sendet, beantwortet oder verschiebt keine Mails.
---

# Gmail-Abgleich: Tracker aktuell halten

Antworte auf Deutsch, kurz. Alle Pfade relativ zum Projektordner (im geplanten Lauf nennt der Auftrag ihn, vorher `cd` dorthin).

**Vorher lesen:** `daten/prozess-learnings.md` („Gültige Workarounds“ befolgen), `daten/suchprofil.md` → „Tracker“. Ist keiner eingerichtet: mit einem Satz beenden.

Tracker lesen und schreiben wie im Skill `bewerbung`, Abschnitt „Tracker pflegen“ (lokal per `tracker/tracker.py` oder claude.ai per ArtifactData, je nach `daten/suchprofil.md` → „Tracker“). Dazu braucht es Lesezugriff auf das Gmail-Postfach des Nutzers (in Claude: Gmail-Connector, Tools wie „search_threads“, „get_thread“). Gibt es keinen: mit dem Satz beenden, dass der Gmail-Zugriff fehlt.

## Ablauf

1. Alle Tracker-Dokumente lesen (`list`), Version jedes Dokuments merken. Startzeit per `date` merken.
2. Gmail der letzten 3 Tage nach Rückmeldungen auf Bewerbungen durchsuchen: Eingangsbestätigungen, Einladungen/Terminanfragen, Absagen, Portal-Mails (Personio, Workday, SuccessFactors, softgarden, JOIN, Teamtailor, Greenhouse, Indeed, StepStone, rexx, hyrise), Personalvermittler. Suchbeispiel: `newer_than:3d (Bewerbung OR application OR Absage OR Einladung OR Vorstellungsgespräch OR "leider" OR Kandidat)`, dazu eine zweite Suche nach Portal-Absendern. Werbung und Job-Alerts ignorieren.
3. Jede relevante Mail einer Tracker-Zeile zuordnen (Firma + Stelle). Nur eindeutig zuordnen, im Zweifel nichts ändern und melden.
4. Status setzen (genau so schreiben): Entworfen → Versendet → Eingang bestätigt → Einladung → Angebot, oder Absage / Zurückgezogen. Nie zurückstufen (Einladung bleibt nicht hinter „Eingang bestätigt“).
   - `versendet_am`: Tag des Absendens (Portal-Bestätigung zählt), nur setzen, wenn leer.
   - `antwort_am`: erste echte Rückmeldung (Einladung oder Absage), nicht die automatische Eingangsbestätigung. Nur setzen, wenn leer.
   - `einladung_am`: bei Einladung setzen, bleibt auch bei späterer Absage stehen.
   - Bei „Eingang bestätigt“ `naechster_schritt` = „Warten“.
   - Bei Absage `naechster_schritt` = „Abgeschlossen“. Bei Einladung den Termin (falls genannt) in `naechster_schritt` und auf Skill `vorstellungsgespraech` hinweisen.
   - Schreiben mit `update`, nur geänderte Felder, Version aus Schritt 1. Bei Versionskonflikt neu lesen und erneut versuchen.
5. **Bewerbungen außerhalb des Ablaufs** (in Gmail, aber nicht im Tracker): neues Dokument mit `set`, `id` = `JJJJ-MM-TT_Firmenname` (Versanddatum, nur `A-Z a-z 0-9 _ -`). Felder: firma, stelle, ort (null), weg (Portal/Kanal), match (null), status, entworfen_am (null), versendet_am, einladung_am, antwort_am, naechster_schritt, link (falls in der Mail), notiz (null).
6. **Finder-Tags (optional, nur macOS):** `python3 .claude/skills/bewerbung/status-ordner.py <ordner>` mit `<ordner>` = `daten/tracker` (lokal) bzw. bei claude.ai: vorher `list` mit `query.limit` 1000 und `out_dir` = neuer leerer Ordner, dann `<out_dir>/bewerbungen`. Setzt nur den Status als farbigen Finder-Tag auf die Ordner in `daten/bewerbungen/`, benennt und verschiebt nichts.
7. **Lern-Datei:** am Ende Log-Eintrag in `daten/prozess-learnings.md` nach den Regeln oben in der Datei.

**Nicht tun:** keine Mails senden, beantworten, entwerfen oder verschieben. Keine Nachfass-Mails vorschlagen oder anlegen. Keine Dateien ändern außer `daten/prozess-learnings.md` (Finder-Tags aus Schritt 6 sind erlaubt).

## Ausgabe
Kurze Liste der Änderungen (Firma: alt → neu), neu angelegte Zeilen, Mails, die nicht eindeutig zuordenbar waren. Keine Änderungen → ein Satz.
