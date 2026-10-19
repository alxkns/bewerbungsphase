---
name: marktanalyse
description: Viele passende Stellenanzeigen sammeln und gemeinsam auswerten. Was machen diese Stellen wirklich, welche Voraussetzungen, welcher Charakter wird gesucht, welche Begriffe, Tools und Formulierungen nutzen die Firmen, wie passt der Lebenslauf dazu? Ergebnis daten/markt.md als Grundlage für Kennenlernen, Lebenslauf (ATS) und Suchbegriffe. Nutzen nach der Einrichtung, bei „was sucht der Markt?“, „Marktanalyse“, „was brauche ich für diese Rollen?“ oder wenn sich die Zielrolle ändert.
---

# Marktanalyse: Was verlangen die Stellen, die der Nutzer will?

Die `stellenanalyse` bewertet eine einzelne Anzeige. Die Marktanalyse liest 20–40 Anzeigen auf einmal und sucht das Muster dahinter. Grundlage: `daten/suchprofil.md` (Zielrollen, Suchbegriffe, Ort), `daten/bewerbungen/_vorlage/lebenslauf.html`, `daten/profil.md`.

Ergebnis:
- `daten/markt/` mit den gesammelten Anzeigen (eine Datei je Anzeige, Volltext)
- `daten/markt.md` mit der Auswertung

**Ehrlich zählen, nicht schätzen.** Jede Häufigkeit ist „in X von N Anzeigen“ und lässt sich nachprüfen (Zählweise in Abschnitt 2). Nichts interpretieren, was nicht dasteht (gleiche Regel wie `stellenanalyse`, Abschnitt 0).

## 1. Anzeigen sammeln

Ziel: 20–40 Anzeigen, die zum Suchprofil passen, aus den letzten 30 Tagen. Lieber 25 passende als 60 halbwegs passende.

**Hauptquelle: Jobbörse der Bundesagentur für Arbeit** (kostenlos, öffentlicher Key, enthält viele Partner-Anzeigen von StepStone, Indeed u. a.):

```bash
curl -s -H 'X-API-Key: jobboerse-jobsuche' \
  'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs?was=<Begriff>&wo=<Ort>&umkreis=<km>&veroeffentlichtseit=30&size=100&page=1'
```
- Je Suchbegriff aus `suchprofil.md` ein Aufruf, Begriff URL-kodiert. Treffer unter `ergebnisliste` (fehlt der Schlüssel ganz, gab es 0 Treffer, also mit `.get` lesen). Felder `stellenangebotsTitel`, `firma`, `referenznummer`, `stellenlokationen[0].adresse.ort`, `datumErsteVeroeffentlichung`, nur manchmal `gehaltsspanneVon/Bis`.
- **Suchbegriffe:** Die Suche ist wörtlich. Zusammengesetzte Wörter getrennt schreiben („Kampagnen Manager“ findet viel, „Kampagnenmanager“ nichts). Reihenfolge und Gender-Form ändern nichts.
- **Zeitraum:** `veroeffentlichtseit` filtert ungenau, es kommen auch viel ältere Anzeigen. Nach `datumErsteVeroeffentlichung` selbst filtern (≤ 30 Tage, notfalls ≤ 60 Tage und so in `markt.md` angeben).
- **Remote:** Der Filter `arbeitszeit=ho` liefert nichts. Ohne `wo` mit `was=<Begriff>%20remote` suchen. Das ist nur eine Volltextsuche und liefert viele Präsenzstellen. Im Detail das Feld `homeofficemoeglich` lesen und den Text auf „remote“ prüfen. `homeofficemoeglich: false` heißt nicht sicher „kein Homeoffice“, der Text geht vor.
- **Volltext:** `curl -sL -A 'Mozilla/5.0' 'https://www.arbeitsagentur.de/jobsuche/jobdetail/<referenznummer>'`. Im HTML steckt JSON in `<script id="ng-state" type="application/json">`, Text unter `jobdetail.stellenangebotsBeschreibung`, dazu `jobdetail.homeofficemoeglich`, `gehaltsspanneVon/Bis`, `verguetungsangabe`. Ist der Text leer, sehr kurz oder bricht mitten im Satz ab: Originalanzeige über `externeURL` bzw. `allianzpartnerUrl` oder per WebSearch (Firma + Titel) suchen und mit WebFetch lesen.
- Nur `v6`-Pfade funktionieren.

**Zusatzquellen** (wenn die Bundesagentur zu wenig liefert, z. B. bei englischsprachigen oder Start-up-Rollen): WebSearch nach „<Begriff> Stellenangebot <Ort>“ und Karriereseiten bzw. Portale (Personio, JOIN, softgarden) mit WebFetch lesen. Hat der Nutzer in `suchprofil.md` „Eigene Quellen“ beschrieben, die auch nutzen. Indeed und Glassdoor direkt blocken (Cloudflare), nicht versuchen.

**Auswahl:**
- Titel grob vorfiltern (Praktikum, Werkstudent, Ausbildung, offensichtlich andere Rolle raus).
- Harte Ausschlüsse aus `suchprofil.md` gelten hier **nicht** streng: Die Marktanalyse soll den Markt zeigen, wie er ist. Nur Anzeigen weglassen, die eine ganz andere Rolle sind.
- Dubletten zusammenführen (dieselbe Stelle an mehreren Standorten, über Vermittler und direkt). Vermittler-Anzeigen ohne erkennbaren Arbeitgeber nur nehmen, wenn sonst zu wenig da ist.
- Mischung zählt: verschiedene Firmengrößen und Branchen, nicht 10 Anzeigen derselben Firma.

**Speichern:** je Anzeige `daten/markt/NN_Firma.md` (NN = laufende Nummer). **Zeile 1** ist der Kopf, alles in einer Zeile: `Quelle: <URL> · Abruf: TT.MM.JJJJ · Titel: … · Firma: <Arbeitgeber laut Text> · Ort: … · Homeoffice laut Text: … · Gehalt laut Text/API: …`. Ab Zeile 3 der Volltext im Wortlaut, nur lesbar gemacht (HTML-Entities wie `&amp;` dekodieren, Markdown-Escapes wie `\#` entfernen). Liegt schon ein `daten/markt/` von einer früheren Analyse: in `daten/markt/alt_JJJJ-MM-TT/` verschieben, dann neu sammeln.

Dem Nutzer vor der Auswertung kurz zeigen: Anzahl, Quellen, Liste Titel · Firma. Passt die Auswahl nicht zu dem, was er sucht → Suchbegriffe anpassen und neu sammeln.

## 2. Auswerten

Jede Anzeige einmal ganz lesen, dabei pro Anzeige notieren (im Scratchpad): Aufgaben, Muss, Kann, gesuchte Eigenschaften, Tools/Fachbegriffe, Ansprache Du/Sie, Arbeitsmodell, Gehalt, Firmengröße/Branche. Dann zählen.

**Zählweise:**
- Rollenbilder, Muss/Kann und Eigenschaften aus diesen Lesenotizen zählen und die Nummern der Anzeigen dazuschreiben („8 von 20: 01, 03, …“). Nur der Anforderungsteil zählt, nicht Firmenbeschreibung oder Benefits („Budget für Events“ ist kein Event-Kriterium).
- Begriffe und Tools zusätzlich per `grep` gegenprüfen, **ohne die Kopfzeile** (sonst trifft z. B. „Agentur“ jede URL von arbeitsagentur.de):
  ```bash
  for f in daten/markt/*.md; do tail -n +2 "$f" | grep -qiE '<muster>' && echo "$f"; done | wc -l
  ```
  Kurze Begriffe als ganzes Wort suchen (`grep -qiwE`), sonst trifft „SEA“ auch „Research“ und „befristet“ auch „unbefristet“. Treffer bei Zweifel gegenlesen. Weicht die Lesezählung vom grep ab, gilt die Lesezählung, mit Vermerk.

**Was die Stellen wirklich sind (Rollenbilder).** 2–4 Gruppen bilden, wenn die Anzeigen unterschiedliche Rollen unter ähnlichen Titeln verstecken (z. B. „Projektmanager“ = einmal Kundenprojekte, einmal interne IT-Einführung). Je Gruppe: typische Aufgaben in Reihenfolge der Häufigkeit, für wen (intern/extern), Anteil der Anzeigen, typische Titel. Nur aus dem Text, keine Deutung.

**Voraussetzungen.** Muss und Kann getrennt (Signalwörter wie im Skill `stellenanalyse`, Abschnitt 2), je Kriterium „X von N“. Ausbildung/Studium, Berufsjahre, Branchenerfahrung, Sprachen und Zertifikate eigens aufführen.

**Charakter.** Gesuchte Eigenschaften und Arbeitsweisen in den Worten der Anzeigen („Hands-on-Mentalität“, „Kommunikationsstärke“, „strukturierte Arbeitsweise“), zusammengefasst zu 6–10 Eigenschaften mit Häufigkeit und den typischen Schreibweisen. Das wird die Spalte „Eigenschaft“ in der Tabelle „Eigenschaften und Belege“ in `profil.md`.

**Sprache, Begriffe, Formulierungen.**
- Fachbegriffe und Tools in **exakter Schreibweise** mit Häufigkeit (für Lebenslauf und ATS-Filter).
- Typische Formulierungen für Aufgaben und Anforderungen (kurze Zitate, je mit Anzahl). Sie dienen dem Verständnis des Marktes und dem Lebenslauf. **Nicht ins Anschreiben kopieren**, dort gilt „Bedarf zeigen, Anzeige nicht spiegeln“ (Skill `anschreiben`).
- Ton: Anteil Du/Sie, wie förmlich, wie viel Englisch.

**Rahmen.** Arbeitsmodell (vor Ort/hybrid/remote, Anteil, laut Text), Gehalt, wo genannt (aus Text oder API, Monatswerte ×12 umrechnen und so kennzeichnen): niedrigste Untergrenze, Median der Spannen-Mitten, höchste Obergrenze, mit Anzahl, Firmengrößen und Branchen, Befristungen, häufige Pflichtunterlagen (Zeugnisse, Anschreiben ja/nein).

## 3. Abgleich mit dem Lebenslauf

Für jedes Muss-Kriterium und jede Eigenschaft mit mindestens 20 % Anteil:
- ✅ im Master-Lebenslauf belegt (Stelle nennen)
- 🟡 vermutlich vorhanden, aber nicht belegt oder anders benannt (z. B. Lebenslauf „Kundenbetreuung“, Markt „Account Management“)
- ❌ nicht erkennbar

Daraus zwei Listen:
- **Fragen fürs Kennenlernen:** jedes 🟡 und ❌ als konkrete Frage („In 18 von 30 Anzeigen wird Erfahrung mit Change Management verlangt. Hast du schon einmal eine Einführung begleitet? Was genau hast du gemacht?“). Das ist der wichtigste Output für den Skill `kennenlernen`.
- **Begriffe für den Lebenslauf:** Marktbegriffe, die dasselbe meinen wie vorhandene Erfahrung, zum Übernehmen nach Bestätigung durch den Nutzer.

## 4. `daten/markt.md` schreiben

```markdown
# Marktanalyse: [Zielrolle], [Ort/Remote]
Stand: TT.MM.JJJJ · N Anzeigen (Bundesagentur X, andere Y) · Suchbegriffe: … · Zeitraum: 30 Tage

## Rollenbilder
### A: [Name] (X von N)
Typische Titel: … · Für wen: … · Aufgaben (häufigste zuerst): …
### B: …

## Muss-Kriterien
| Kriterium | Anzahl | Schreibweisen | Lebenslauf |
|---|---|---|---|

## Kann-Kriterien
| … |

## Gesuchte Eigenschaften
| Eigenschaft | Anzahl | So steht es in den Anzeigen | Lebenslauf |
|---|---|---|---|

## Begriffe und Tools (exakte Schreibweise)
| Begriff | Anzahl | Varianten |
|---|---|---|

## Typische Formulierungen (nur Verständnis und Lebenslauf, nie ins Anschreiben)
- „…“ (X×)

## Rahmen
Du/Sie: … · Arbeitsmodell: … · Gehalt (X Anzeigen mit Angabe): Min … / Median … / Max … · Firmen: … · Pflichtunterlagen: …

## Abgleich mit dem Lebenslauf
Stark belegt: … · Lücken: … · Anders benannt: …

## Fragen fürs Kennenlernen
1. …

## Empfehlungen
- Suchbegriffe: behalten / neu / streichen (mit Grund)
- Zielrollen: welches Rollenbild passt am besten zum Lebenslauf
- Lebenslauf: Begriffe zum Übernehmen
```

## 5. Übergabe

Im Chat in wenigen Sätzen: was die Stellen wirklich verlangen, die 3 wichtigsten Stärken und Lücken des Nutzers im Vergleich, welches Rollenbild am besten passt. Dann:
- Vorgeschlagene Suchbegriffe zeigen und erst nach Bestätigung in `daten/suchprofil.md` übernehmen.
- Begriffe für den Lebenslauf erst nach Bestätigung in den Master übernehmen.
- Nächster Schritt: `kennenlernen` mit den Fragen aus `markt.md`.

Wiederholen, wenn sich Zielrolle oder Ort ändern oder nach ca. 3 Monaten.
