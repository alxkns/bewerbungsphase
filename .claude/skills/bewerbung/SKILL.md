---
name: bewerbung
description: Kompletter Bewerbungsablauf von der Stellenanzeige bis zu fertigen PDFs (Anschreiben, angepasster Lebenslauf, Gesamtmappe). Nutzen, sobald der Nutzer eine Stellenanzeige (Text, Link oder PDF) schickt, „bewirb mich bei …“ sagt oder Anschreiben/Lebenslauf als PDF braucht.
---

# Bewerbung: Anzeige rein, PDFs raus

Steuert den Ablauf und ruft die Fach-Skills auf. Vor dem Schreiben immer lesen:
- `.claude/skills/bewerbung/stil.md`: allgemeiner Schreibstil + Du/Sie-Regel
- `daten/profil.md`: Eckdaten, ehrliches Level, Motivation und Charakter, Belege, Grenzen, Stil-Vorlieben
- `daten/suchprofil.md`: Ausschlüsse, Match-Grenze, Tracker-URL
- `daten/bewerbungen/_vorlage/lebenslauf.html`: Master-Lebenslauf. Fakten nur aus Master und `profil.md`, nichts erfinden

Fehlen `daten/profil.md` oder der Master-Lebenslauf: abbrechen und Skill `einrichtung` vorschlagen. Steht im Kopf von `profil.md` noch nicht „Kennenlernen abgeschlossen“: einmal darauf hinweisen, dass Skill `kennenlernen` die Anschreiben deutlich persönlicher macht, dann weitermachen, wenn der Nutzer will.

`<Name>` = Name aus `profil.md`, Abschnitt „Eckdaten“.

## Ablauf

1. **Anzeige sichern.** Link → Text holen (WebFetch oder Browser-Pane). Ordner anlegen:
   `daten/bewerbungen/JJJJ-MM-TT_Firmenname/` (Firmenname normal geschrieben, Leerzeichen → Bindestrich).
   Anzeige komplett als `anzeige.md` speichern (Anzeigen verschwinden, fürs Gespräch braucht man sie wieder).

1a. **Neubau eines bestehenden Ordners** (liegen schon `anschreiben.html`, `lebenslauf.html`, PDFs, `recruiter.md` oder `v1/`…): erst alles außer `anzeige.md` und `analyse.md` nach `alt_JJJJ-MM-TT/` verschieben (heutiges Datum), dann frisch ab Schritt 2. Vorher prüfen, ob die Anzeige noch online ist.

2. **Analyse** nach Skill `stellenanalyse` → `analyse.md`. Bestehende `analyse.md` gegen das aktuelle `profil.md` abgleichen und den Abschnitt „Rolle verstehen“ ergänzen, falls er fehlt (Pflicht, darauf baut das Anschreiben auf). Wichtig für die nächsten Schritte:
   Ansprache (Du/Sie), Ansprechpartner, Postanschrift, Kennziffer, ob Eintrittstermin/Gehaltsvorstellung gefordert sind, Muss-Kriterien, Match.
   Match unter der Grenze aus `suchprofil.md` oder harter Ausschluss → kurz an den Nutzer melden, bevor weitergeschrieben wird.

3. **Unternehmensanalyse** nach Skill `unternehmensanalyse` → Abschnitt „Unternehmen verstehen“ in `analyse.md` (Kultur, Werte, Arbeitsweise, Passung, Einladungsgrund; keine News, keine Deutung der Rolle). Pflicht vor dem Anschreiben, auch beim Neubau, falls der Abschnitt fehlt.

3a. **Fehlende Eckdaten** (z. B. Gehaltsvorstellung gefordert, aber in `profil.md` offen) → Nutzer fragen, in `profil.md` eintragen.

4. **Lebenslauf** nach Skill `lebenslauf-anpassen`:
   `cp daten/bewerbungen/_vorlage/lebenslauf.html daten/bewerbungen/<ordner>/` und dort anpassen. Master bleibt unverändert.

5. **Anschreiben** nach Skill `anschreiben` (will die Firma ausdrücklich keins, z. B. nur Formularfragen: kein Anschreiben bauen, die Antworten in `portal.md` nach denselben Regeln schreiben):
   `cp daten/bewerbungen/_vorlage/anschreiben.html daten/bewerbungen/<ordner>/` und alle `[…]`-Platzhalter ersetzen. `<title>` = `Anschreiben_<Firma>_<Name>`.

5a. **KI-Sprache-Check (Pflicht, vor jedem PDF):** Skill `humanizer-de` (liegt im Projekt unter `.claude/skills/humanizer-de`), Modus **Sachlich**, Arbeitszweig **Nur Audit**.
   ```bash
   python3 .claude/skills/bewerbung/brieftext.py daten/bewerbungen/<ordner>/anschreiben.html > <scratchpad>/anschreiben.txt
   python3 .claude/skills/humanizer-de/scripts/humanizer_audit.py --file <scratchpad>/anschreiben.txt --mode sachlich
   ```
   Danach die Muster aus `.claude/skills/humanizer-de/references/patterns.md` als Urteil prüfen (Cluster-Regel, Carve-outs). Befunde kurz auflisten (Zitat + Muster), dann selbst im Ton von `stil.md` umschreiben. **humanizer-de schreibt nicht selbst um.** Fakten, Zahlen und Namen bleiben unverändert. Bewerbungsspezifisch zusätzlich prüfen: Doppelpunkt-Pointen („Warum der Wechsel:“, „Ein Beispiel:“), „Genau das …“, „Kein X, sondern Y“, Trikolon-Reihen, Sätze mit „Und …“ als Pointe, Formulierungen oder Aufgaben aus der Anzeige nachgesprochen (Regel „Bedarf zeigen, Anzeige nicht spiegeln“ im Skill `anschreiben`; erlaubt sind nur Stellentitel und Tool-Namen). Einzeln ok, ab zwei gleichen im selben Text umschreiben. Gilt auch für Lebenslauf-Profil und Mail-Texte, und nach jedem Umschreiben im Recruiter-Check (7a) erneut.

6. **PDFs bauen:**
   ```bash
   .claude/skills/bewerbung/pdf.sh daten/bewerbungen/<ordner>
   ```
   Erzeugt `Anschreiben_<Firma>_<Name>.pdf`, `Lebenslauf_<Name>.pdf` und die Mappe `Bewerbung_<Firma>_<Name>.pdf` (beides in einer Datei, für Portale mit nur einem Upload).

7. **Sichtprüfung (Pflicht):**
   ```bash
   pdftoppm -r 70 -png "daten/bewerbungen/<ordner>/Anschreiben_<Firma>_<Name>.pdf" <scratchpad>/vorschau
   ```
   Vorschau-PNGs ansehen (Read). Anschreiben **genau 1 Seite**, Unterschrift und „Anlage“ sichtbar, nichts abgeschnitten. Lebenslauf max. 2 Seiten, keine verwaisten Überschriften am Seitenende. Zu lang → kürzen, nicht die Schrift verkleinern.

7a. **Recruiter-Check** (ab Match-Grenze, max. 2 Verbesserungsrunden): nach Skill `recruiter` bewerten und umschreiben, Ergebnis in `recruiter.md`.

7b. **`portal.md`** im Ordner: Texte zum Kopieren für Formularfelder (Portale füllt der Nutzer selbst aus).
   - Kurzanschreiben 80–120 Wörter (Variante E-Mail/Portal aus Skill `anschreiben`, ebenfalls durch 5a)
   - Gehaltsvorstellung (Jahresbrutto nach `profil.md`, bei Teilzeit anteilig mit Wochenstunden)
   - Frühester Eintritt und Kündigungsfrist (`profil.md`, „Eckdaten“)
   - Wie auf die Stelle aufmerksam geworden (Quelle aus `anzeige.md`)

8. **Übergabe:** Anschreiben-Text kurz im Chat zeigen, Pfade zu den PDFs und `portal.md` nennen, Eintrag im Bewerbungs-Tracker anlegen (siehe unten). Abschicken macht der Nutzer selbst.

## Tracker pflegen

Einzige Liste aller Bewerbungen ist die Datenbank des Bewerbungs-Trackers: URL in `daten/suchprofil.md`, Abschnitt „Tracker“, Collection `bewerbungen`, ein Dokument pro Bewerbung. Der Nutzer ändert dort selbst Status und Daten im Browser. Ist noch kein Tracker eingerichtet: Schritt überspringen und das sagen.

- **Lesen:** `ArtifactData` `list` auf `bewerbungen` (Seiten mit `query.cursor`).
- **Neu:** `ArtifactData` `set` mit `doc_id` = Ordnername ohne Umlaute und Sonderzeichen (nur `A-Z a-z 0-9 _ -`, z. B. `2026-10-15_Beispiel-GmbH`).
- **Ändern:** `ArtifactData` `update` nur mit den geänderten Feldern und `if_version` aus dem letzten Lesen. Der Nutzer kann parallel im Browser ändern.

```json
{"firma": "", "stelle": "", "ort": null, "weg": "", "match": 75, "score": null,
 "status": "Entworfen", "entworfen_am": "2026-10-14", "versendet_am": null,
 "einladung_am": null, "antwort_am": null, "naechster_schritt": "", "link": "https://…", "notiz": null}
```

Status (genau so schreiben): Vorschlag → Angefordert → In Arbeit → Entworfen → Versendet → Eingang bestätigt → Einladung → Angebot, oder Absage / Zurückgezogen / Verworfen.
- Automatik: Routine Stellensuche legt neue Stellen als „Vorschlag“ an (mit `anzeige.md`, `analyse.md`, `vorgeschlagen_am`). Der Nutzer klickt im Dashboard „Bewerbung erstellen“ → „Angefordert“. Routine Erstellen baut daraus die Mappe → „Entworfen“. „Verworfen“ = Vorschlag abgelehnt, wird nicht erneut vorgeschlagen.
- `versendet_am`: Tag des Absendens (Portal-Bestätigung per Mail zählt).
- `match`: Match aus `analyse.md` in % (Zahl). `score`: Endnote des Recruiter-Checks (/10, Zahl mit einer Nachkommastelle, z. B. 8.6), sonst null. Beide zeigt das Dashboard als Spalten.
- `antwort_am`: erste echte Rückmeldung (Einladung oder Absage), nicht die automatische Eingangsbestätigung.
- `einladung_am`: bleibt gesetzt, auch wenn später eine Absage kommt.
Nachfassen nur auf ausdrücklichen Wunsch (Skill `anschreiben`, Variante Nachfassen): nicht vorschlagen, keine Entwürfe anlegen.

## Weitere Skills
- `einrichtung`, `marktanalyse`, `kennenlernen`: einmalig vor der ersten Bewerbung, `kennenlernen` später erneut für offene Fakten-Fragen
- `unternehmensanalyse`: Kultur und Werte der Firma, Einladungsgrund (Schritt 3)
- `quereinstieg`: Rollen- oder Branchenwechsel übersetzen (bei jeder Bewerbung mitdenken, wenn `profil.md` einen Abschnitt „Wechsel“ hat)
- `vorstellungsgespraech`: sobald eine Einladung kommt, Ergebnis als `gespraech.md` in den Ordner
- `gehaltsverhandlung`: bei Gehaltsfrage oder Angebot
- `recruiter`: Einstellersicht-Check + Umschreiben, Pflicht ab Match-Grenze, max. 2 Verbesserungsrunden

## Technik
- Layout: `vorlagen/style.css` (Arial, Navy, hellblaues Kopfband; Standardschrift, damit Bewerberportale den Text sauber auslesen). Foto und Unterschrift in `daten/bewerbungen/_vorlage/assets/`.
- HTML-Dateien im Bewerbungsordner verweisen auf `../../../vorlagen/style.css` und `../_vorlage/assets/…`, deshalb immer genau eine Ebene unter `daten/bewerbungen/` ablegen.
- PDF über Chrome headless, Mappe über `pdfunite` (poppler).
