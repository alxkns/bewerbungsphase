---
name: recruiter
description: Fertige Bewerbung (Anschreiben + Lebenslauf) aus Sicht von Recruiter und Fachbereich der Firma prüfen, mit Punkten bewerten und höchstens zweimal umschreiben (Ziel 9 von 10, Stopp früher, wenn nur noch Fakten fehlen). Pflicht für alle Bewerbungen ab der Match-Grenze aus daten/suchprofil.md (Standard 70 %), bevor sie rausgehen. Nutzen bei „Recruiter-Check“, „aus Einstellersicht“, „würden die mich einladen?“, „prüf die Bewerbung“, „auf 9 heben“ oder als Schritt 7a im Skill bewerbung.
---

# Recruiter-Check: bewerten, umschreiben, blind nachbewerten

Ab der Match-Grenze entscheidet nicht mehr die Passung, sondern ob die Unterlagen das in 30 Sekunden rüberbringen. **Ziel: 9,0 / 10.** Was nur mit neuen Fakten ginge, wird als Deckel markiert und an den Nutzer gegeben, nicht schöngeschrieben.

Typische Deckel sind fehlende formale Stationen (Konzern, Beratung, Studium), fehlende Zeugnisse, Ziel-Tools ohne Praxis und nicht gemessene Ergebnisse. Bekannte Deckel des Nutzers stehen ggf. in `daten/profil.md` unter „Stil-Vorlieben“. Sobald die blinde Bewertung nur noch Deckel zeigt: aufhören, Deckel an den Nutzer melden und keine weiteren Kosmetik-Runden drehen.

## Welche Bewerbungen

- **Einzeln:** Ordner, den der Nutzer nennt.
- **Alle ab Match-Grenze:** Tracker lesen (Skill `bewerbung`, „Tracker pflegen“; lokal `list --min-match <Grenze>`), Grenze in `daten/suchprofil.md`. Nur Status `Entworfen` umschreiben. Schon versendet → nur bewerten, nichts überschreiben (dient als Gesprächsvorbereitung).
- Liegt schon eine `recruiter.md` vor, wird die nächste Runde angehängt, nicht neu angefangen.

## Rollen (drei getrennte Köpfe)

| Rolle | Wer | Sieht |
|---|---|---|
| **Prüfer** | Subagent (siehe `AGENTS.md`, „Werkzeuge“), der die Unterlagen nicht geschrieben hat | alles, schreibt `recruiter.md` (Schritte 1–4) |
| **Schreiber** | Hauptchat. Bei mehreren Bewerbungen ein Agent pro Ordner, parallel | `recruiter.md`, setzt um (Schritt 5) |
| **Blinder Endbewerter** | **neuer** Subagent, nie der Prüfer | nur `anzeige.md`, Endfassung, Fakten-Quellen. **Nicht** `recruiter.md`, nicht `v1/`. Sonst bewertet er seine eigenen Vorschläge oder den Abstand zur alten Fassung statt die Bewerbung (Schritt 6) |

Jeder Agent bekommt diese Datei und den Ordnerpfad. Ergebnisse von Agents vor der Übergabe an den Nutzer selbst ansehen (Diff, PDF-Vorschau).

## Fakten-Quellen und Wahrheitslinie

- **Lebenslauf:** Master `daten/bewerbungen/_vorlage/lebenslauf.html` plus „Bausteine“ aus `daten/profil.md` (dürfen bei passender Stelle als Stichpunkt rein).
- **Anschreiben:** Master plus `profil.md`, vor allem „Motivation und Charakter“, „Hintergrund“ und „Eigenschaften und Belege“.
- Was der Prüfer für eine 9 braucht, aber nirgends steht → **Fakten-Frage** an den Nutzer. Alle Fragen gesammelt in einer Nachricht (oder Auswahlfrage), bevor umgeschrieben wird. Läuft der Check unbeaufsichtigt (Routine), Fragen nur sammeln. Bestätigte Fakten zuerst in den Master (bzw. `profil.md`), dann in die Bewerbung.
- Nie: Tools, Zahlen, Ergebnisse oder Verantwortung erfinden; etwas aus „Grenzen“ in `profil.md` vorschlagen.

## 1. Rolle einnehmen

`anzeige.md` und `analyse.md` lesen, zwei Personen festlegen:
- **Recruiterin / HR:** 80 Bewerbungen auf dem Tisch, sucht Gründe fürs Aussortieren.
- **Fachvorgesetzte:r** (aus der Anzeige ableiten): löst die Person unser Problem, passt sie ins Team?

Kultur mitnehmen: Konzern oder Mittelstand, Du oder Sie, wie technisch, wie förmlich.

## 2. Lesen wie die Firma

a) **6-Sekunden-Scan des Lebenslaufs:** Kopf, Untertitel, Stationen, Zeiträume. Was bleibt hängen?
b) **30 Sekunden Anschreiben:** erster und letzter Absatz. Warum genau diese Firma, warum genau diese Person?
c) **Gründlich:** Jede Muss-Anforderung suchen: sichtbar belegt? Wörtliche Kernformulierungen der Anzeige (z. B. „Prototyp oder MVP“) gehören in den **Lebenslauf** (ATS). Das Anschreiben ist ein Motivationsschreiben (Skill `anschreiben`, Grundsatz): Es zählt, ob Motivation, die 3 gesuchten Eigenschaften mit kurzem Beleg und der Fit erkennbar sind, in eigenen Worten und ohne Technik. Ein Anschreiben, das die Anzeige nachspricht (übernommene Formulierungen, Aufgaben als Zukunftsplan, Anforderungen der Reihe nach abgehakt), wirkt wie für die Anzeige geschrieben, nicht für die Firma.
d) **Unausgesprochene Fragen** (Skill `quereinstieg`, Bedenken-Tabelle in `profil.md` → „Wechsel“): Warum der Wechsel? Warum so kurz bei der letzten Station? Zu teuer? Wird die relevante Sorge beantwortet, ohne defensiv zu klingen?

## 3. Bewerten (je 1–10)

| Kriterium | Frage aus Einstellersicht |
|---|---|
| Erster Eindruck | Passt das Bild nach 6 Sekunden zur Stelle? |
| Muss-Kriterien belegt | Finde ich jede Kernanforderung mit Beleg, ohne zu suchen? |
| Firmenbezug | Ist das für uns geschrieben oder ein Serienbrief? Hat er verstanden, was die Rolle im Alltag macht und für wen (intern/extern)? Ein Einstieg, der in die falsche Richtung zielt, bekommt höchstens 6. Kann ich nach dem Lesen in einem Satz sagen, warum wir ihn einladen sollten? Wenn nein: höchstens 7. Unterstellt das Anschreiben der Stelle etwas, das nicht in der Anzeige steht (Zweck, Zielgruppe, Anwendungsfall, Bezug zu Firmen-News): höchstens 6. |
| Glaubwürdigkeit | Zahlen, konkrete Ergebnisse, nichts aufgeblasen? |
| Risiken entschärft | Sind Wechsel, Lücken, Gehalt sauber eingeordnet? |
| Ton & Kultur | Klingt das, als würde die Person zu uns passen? Verkaufston über das eigene System, Allgemeinweisheiten oder eine gespiegelte Anzeige: höchstens 7. Kleinkram, der die Arbeit klein wirken lässt (Fehlerfall, einzelnes Datenfeld, einzelne Funktion als Beleg): höchstens 7. Nie solche Einzelbeispiele als Ersatztext vorschlagen (Regel „Flughöhe“ in `stil.md`). |
| Gesuchte Eigenschaften | Sehe ich die 3–4 Eigenschaften, die die Stelle braucht (Tabelle „Eigenschaften und Belege“ in `profil.md`, Auswahl in `analyse.md`), als Verhalten mit Beleg? Eigenschaft ohne Beleg oder Technisches im Anschreiben (Tools, Methoden-Details, Fachjargon): höchstens 7. Sehe ich daneben belegt, dass die Person überdurchschnittlich liefert (A-Merkmale in `bewerbung/stil.md`: Ergebnisse statt Aufgaben, Lerntempo, Eigeninitiative)? Wenn nein: höchstens 8. Nie vorschlagen, ein belegtes A-Merkmal gegen eine weitere Eigenschaft aus der Anzeige zu tauschen. |
| Schlagwörter (ATS) | Kommen die Begriffe der Anzeige in unserer Schreibweise im **Lebenslauf** vor? Im Anschreiben nur die gesuchten Eigenschaften, keine Fachbegriff-Liste. |

**Maßstab (damit Runden vergleichbar sind):**
- **10:** Besser geht es mit diesen Fakten nicht. Nichts, was ich ändern würde.
- **9:** Top 3 von 80. Ich rufe heute an. Höchstens Kleinigkeiten.
- **8:** Klar einladen, aber ein sichtbarer Schwachpunkt.
- **7:** Einladen, wenn die Top-Kandidaten absagen.
- **5–6:** Vielleicht-Stapel.
- **≤ 4:** Absage.

**Was wohin gehört:** „Muss-Kriterien belegt“, „Glaubwürdigkeit“ und „Schlagwörter“ werden über den **Lebenslauf** erfüllt. Das Anschreiben wird als Motivationsschreiben bewertet: worauf der Nutzer Lust hat, 3 gesuchte Eigenschaften mit je einem kurzen Beleg, wie er unterstützt, warum er passt (Grundsatz im Skill `anschreiben`). Ersatztexte fürs Anschreiben nie technischer oder kleinteiliger machen; fehlende Technik-Belege gehören in den Lebenslauf. No-gos: Lebenslauf nacherzählen, Floskeln. Fehlt ein erkennbarer Mehrwert-Satz, bekommt „Firmenbezug“ höchstens 7. Fehlt ein Beleg oder Schlagwort, gehört der Ersatztext in den Lebenslauf, nie als Anzeigen-Satz ins Anschreiben (einzelne Fachbegriffe mit Beleg sind erlaubt). Keine Zahlen für Bearbeitungszeit oder Fehlerquote vorschlagen: sofern nicht gemessen und in `profil.md` belegt: Deckel oder Fakten-Frage an den Nutzer. Vorschläge fürs Anschreiben beziehen sich auf „Rolle verstehen“ und „Unternehmen verstehen“ (Kultur, Werte, Einladungsgrund) in `analyse.md` und halten „Grenzen“ in `profil.md` ein. Nie vorschlagen, der Stelle einen Zweck, eine Zielgruppe oder einen Anwendungsfall zuzuschreiben, der nicht in der Anzeige steht, und keine Firmen-News einbauen, die die Anzeige nicht nennt. Ins Anschreiben nur, wenn danach weiter der Aufbau aus vier Absätzen, nichts Technisches und die Wortgrenze aus Skill `anschreiben` gelten. Ein Anschreiben, das den Lebenslauf nacherzählt, bekommt bei „Ton & Kultur“ höchstens 7.

Gesamt = Durchschnitt, eine Nachkommastelle. Dazu **Urteil** und der **interne Satz** der Recruiterin. Ehrlich und hart.

**Deckel:** Kann ein Kriterium nur mit Fakten steigen, die es nicht gibt (fehlendes Tool, kein Zeugnis, keine Konzernerfahrung), bekommt es den ehrlichen Wert plus den Vermerk „Deckel: …“. Das ist kein Schreibfehler, sondern die Entscheidung des Nutzers.

## 4. `recruiter.md` schreiben (bzw. Runde anhängen)

```markdown
# Recruiter-Check: [Stelle] bei [Firma]

## Runde 1 · 6,4 / 10 · Vielleicht-Stapel
> Interner Satz: „…“

| Kriterium | Punkte | Begründung | Weg zur 9 |
|---|---|---|---|
| Firmenbezug | 5 | … | Absatz 3 auf X beziehen: „Ersatztext …“ |
| Risiken | 6 | … | Deckel: Arbeitszeugnis fehlt (Nutzer) |
…

### 6-Sekunden-Scan
…

### Änderungen (nach Wirkung, je mit Ersatztext und was dafür rausfliegt)
1. **Anschreiben, Absatz 3:** „…“ → „…“ · Platz: streicht „…“
…

### Fakten-Fragen an den Nutzer
- …

### Was bleiben muss
…
```

Pro Kriterium unter 9 steht in „Weg zur 9“ entweder ein umsetzbarer Ersatztext oder ein Deckel. Keine vagen Tipps („konkreter werden“).

## 5. Umschreiben

1. **Sichern:** `mkdir -p vN && cp anschreiben.html lebenslauf.html vN/` (N = Runde). Nie `*_v1.html` daneben legen, sonst rendert `pdf.sh` die alte Fassung mit und überschreibt die neuen PDFs.
2. **Platzbudget zuerst:** Das Anschreiben ist fast immer schon voll (eine Seite, Unterschrift + „Anlage“ sichtbar). Jede Ergänzung braucht eine Streichung gleicher Länge. Erst streichen, was für diese Firma nichts bringt (branchenfremde Beispiele, Doppelungen mit dem Lebenslauf), dann ergänzen. Lebenslauf: max. 2 Seiten, Unterschrift nicht allein auf Seite 3.
3. Änderungen umsetzen nach den Skills `anschreiben` (Floskel-Blacklist, Du/Sie) und `lebenslauf-anpassen`. „Was bleiben muss“ bleibt.
4. **Bezüge prüfen:** Nach Kürzungen jeden geänderten Absatz ganz lesen: Zeigt „es“, „dort“, „beides“ noch auf das Richtige? Fehlt eine Zeitangabe o. ä., weil ein Satz zusammengezogen wurde?
5. **PDFs bauen** (`.claude/skills/bewerbung/pdf.sh daten/bewerbungen/<ordner>`, bei Hängern mit `run_in_background`) und Sichtprüfung wie im Skill `bewerbung`, Schritt 7: Vorschau-PNGs lesen, nicht nur die Seitenzahl.

## 6. Blind nachbewerten

Neuer Subagent (siehe Rollen), bekommt keine Vorgeschichte. Er liest die Endfassung so, wie ein ATS sie sieht: `pdftotext -layout` der fertigen PDFs, nicht das HTML. Was dort fehlt oder zerrissen ist, zählt als fehlend. Er bewertet nach Schritt 1–3 und hängt an `recruiter.md` an:

```markdown
## Runde 2 (blind) · 8,6 / 10 · Einladen
| Kriterium | Punkte | Weg zur 9 |
…
```

- **≥ 9,0** oder alle Kriterien unter 9 haben einen Deckel → fertig.
- Sonst nächste Runde (Schreiber setzt „Weg zur 9“ um, wieder ein neuer blinder Bewerter). **Höchstens 2 Verbesserungsrunden** (Sicherungen `v1/`, `v2/`), also max. 3 Bewertungen. Danach nicht weiter umschreiben, offene Punkte entscheidet der Nutzer.

## Übergabe

Im Chat pro Bewerbung: Punkte je Runde, die 3 wichtigsten Änderungen, Deckel und Fakten-Fragen. Im Tracker `score` auf die letzte Bewertung setzen (Zahl, z. B. `9.1`) und `notiz` ergänzen: `Recruiter-Check: 6,4 → 8,6 → 9,1` (ein `update` mit Version aus dem letzten Lesen, siehe Skill `bewerbung`, „Tracker pflegen“). Abschicken macht der Nutzer selbst.
