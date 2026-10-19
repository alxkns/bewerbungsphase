---
name: anschreiben
description: Deutsches Anschreiben nach DIN 5008 schreiben (Du oder Sie wie in der Anzeige) und als HTML für den PDF-Druck befüllen. Nutzen für Anschreiben, Motivationsschreiben, Bewerbungstext für E-Mail oder Portal sowie Nachfass-Mails.
---

# Anschreiben

Pflichtlektüre vorher: `.claude/skills/bewerbung/stil.md` (Ton + Du/Sie), in `daten/profil.md` die Abschnitte „Motivation und Charakter“ (Hauptquelle), „Eigenschaften und Belege“, „Grenzen“ und „Stil-Vorlieben“, `analyse.md` im Bewerbungsordner (vor allem „Rolle verstehen“ und „Unternehmen verstehen“ mit Kultur, Werten und Einladungsgrund), Master-Lebenslauf.

**Grundsatz: Das Anschreiben ist ein Motivationsschreiben.** Es beantwortet vier Fragen, nichts sonst:
1. **Worauf habe ich Lust?** Was den Nutzer an genau dieser Arbeit antreibt (Quelle: „Motivation und Charakter“ in `profil.md`).
2. **Welche gesuchten Eigenschaften bringe ich mit?** Die 3 Eigenschaften, die die Anzeige am stärksten verlangt (Auswahl in `analyse.md`, Tabelle „Eigenschaften und Belege“ in `profil.md`), jeweils mit **einem kurzen Satz Beleg** aus der eigenen Erfahrung.
3. **Wie kann ich die Firma unterstützen?** Was sie davon hat, in den Worten des Nutzers, ohne einen Anwendungsfall zu unterstellen.
4. **Warum bin ich ein Fit?** Wie der Nutzer arbeitet, passend zu Kultur und Werten der Firma, gezeigt als eigenes Verhalten.

**Nichts Technisches.** Keine Tools, keine Methoden-Details, keine Fachbegriffe, die erst entschlüsselt werden müssen. Das alles steht im Lebenslauf. Ein eigenes Projekt darf als Ergebnis vorkommen, nicht als Technik-Beschreibung.

**Kein Kleinkram** (Regel „Flughöhe“ in `stil.md`): keine Fehlerfälle, einzelnen Datenfelder, einzelnen Funktionen oder Anekdoten.

**Ich-Form, eigene Leistung:** Was der Nutzer verantwortet hat, nie „gemeinsam/wir“. Nie als Zitat von Kollegen („Mein Team beschreibt mich …“), immer als eigenes Verhalten. Keine losen Behauptungen („Ich nehme Menschen mit.“), jede Eigenschaft in einen Gedanken mit Beleg eingebettet.

**No-gos:** den Lebenslauf nacherzählen (keine Stationen, keine Tool-Listen, keine Zeitachse), Floskeln (Blacklist in `stil.md`, plus alles, was in jedem Anschreiben stehen könnte), alles aus „Grenzen“ in `profil.md`.

Gibt es in `profil.md` unter „Stil-Vorlieben“ ein freigegebenes Referenz-Anschreiben: Ton und Aufbau daran ausrichten, Sätze nicht kopieren.

## Nichts unterstellen
- Die Rolle ist genau das, was in der Anzeige steht. Keinen Zweck, keine Zielgruppe und keinen Anwendungsfall nennen, den die Anzeige nicht nennt. Die Rolle weder eingrenzen noch erweitern.
- Keine aktuellen Ereignisse der Firma (News, Partnerschaften, Übernahmen), außer die Anzeige nennt sie selbst.
- Der Einstieg muss ohne Vorwissen aus der Recherche verständlich sein. Keine rhetorischen Fragen, kein Fachjargon, den die Leserin erst entschlüsseln muss.

## Bedarf zeigen, Anzeige nicht spiegeln
Nicht „bei euch steht X, ich liefere X“. Das liest sich, als wäre der Text nur geschrieben, weil es in der Anzeige so steht. Stattdessen: Das Anschreiben zeigt mit eigenen Erlebnissen und Worten, dass der Nutzer das mitbringt. Die Leserin soll den Treffer selbst erkennen.
- Keine Sätze oder Wendungen aus der Anzeige übernehmen. Erlaubt sind der Stellentitel (Betreff) und die gesuchten Eigenschaften in der Schreibweise der Anzeige (z. B. „Kommunikationsstärke“, „Prozessverständnis“), jeweils mit Beleg.
- Keine Aufgaben der Anzeige als Zukunftsplan nachsprechen („Bei euch will ich Use Cases identifizieren und …“).
- Kein Abhaken der Anforderungen in Reihenfolge der Anzeige.
- Wünsche an die neue Rolle nicht aus den Versprechen der Anzeige bauen („Mandat für Priorisierung“, „Raum für Ideen“): Das ist dasselbe Echo von der anderen Seite.
- Prüffrage pro Satz: Würde der Satz auch ohne die Anzeige so dastehen? Wenn er nur als Echo funktioniert, umschreiben.

> ✗ „Ihr sucht jemanden, der Use Cases identifiziert und Mitarbeitende befähigt. Genau das habe ich bei meinem Arbeitgeber gemacht.“
>
> ✓ „Mir ist wichtig, dass ein Team eine neue Lösung mitträgt. Deshalb habe ich die Kolleg:innen von Anfang an eingebunden, als ich ein neues System eingeführt habe. Heute arbeiten alle täglich darin.“

## Formalien (DIN 5008, in der Vorlage schon angelegt)
Vorlage: `daten/bewerbungen/_vorlage/anschreiben.html` (Briefkopf des Nutzers ist dort schon eingetragen). Ersetzen:
- **Anschriftfeld:** Firma (mit Rechtsform), „z. Hd. Vorname Nachname“ wenn bekannt, Straße, PLZ Ort. Keine Anschrift bekannt (reine Portal-Bewerbung): Firma + Ort reicht.
- **Datum:** `<Wohnort>, TT.MM.JJJJ` (heutiges Datum).
- **Betreff:** fett, ohne das Wort „Betreff“, ohne Punkt. `Bewerbung als [Titel exakt aus Anzeige inkl. (m/w/d)]`, ggf. `, Kennziffer 123`.
- **Anrede:** nach Du/Sie-Tabelle, endet mit Komma. Erster Satz danach beginnt klein.
- **Gruß** ohne Komma, darunter Unterschrift (automatisch), darunter Name (Du: Vorname, Sie: Vor- und Nachname).
- **Anlage:** „Anlage: Lebenslauf“ (bei Zeugnissen: „Anlagen: Lebenslauf, Arbeitszeugnis“).

## Länge
**Maximal 200 Wörter** von Anrede bis Gruß (oder die Grenze aus „Stil-Vorlieben“ in `profil.md`; zählen mit `python3 .claude/skills/bewerbung/brieftext.py <anschreiben.html> | wc -w`), vier Absätze plus Schlusssatz, genau eine Seite.

## Aufbau

Vier Absätze, entlang der vier Fragen aus dem Grundsatz.

**1. Worauf ich Lust habe (2–3 Sätze).** Kein „hiermit bewerbe ich mich“. Was den Nutzer an dieser Arbeit freut, passend zur Rolle aus „Rolle verstehen“ (gleiche Richtung: intern Kolleg:innen, extern Kunden). Dazu kurz, warum jetzt (aus „Motivation und Charakter“ bzw. „Wechsel“). Nie mit Größe argumentieren. Keine Allgemeinweisheit, kein Verkaufston über die eigene Arbeit.

**2. Welche gesuchten Eigenschaften ich mitbringe (Kern).** Die 3 wichtigsten Eigenschaften aus `analyse.md`. Je Eigenschaft ein Gedanke: was der Nutzer mitbringt und ein kurzer Beleg aus seiner Erfahrung (Tabelle in `profil.md`, Ergebnis auf Systemebene). Eine Einleitung wie „Dafür bringe ich drei Dinge mit.“ ist erlaubt. Nicht technisch, nicht in Reihenfolge der Anzeige abhaken.

**3. Warum ich passe und wie ich unterstütze.** Wie der Nutzer arbeitet, passend zu Kultur und Werten aus „Unternehmen verstehen“, als eigenes Verhalten in der Ich-Form (z. B. „Für mich zählt eine Lösung erst, wenn sie genutzt wird. Deshalb fange ich beim Ablauf an, nicht beim Werkzeug.“). Daraus muss der Einladungsgrund hervorgehen. Einen Wechsel einordnen nur, wenn nötig (Skill `quereinstieg`). Was unter „Grenzen“ als „nur im Gespräch“ steht, kommt nicht hinein.
- **Lücken nur nennen, wenn sie ein Muss der Anzeige betreffen** und der Recruiter sie ohnehin sieht. Dann kurz, mit Gegenbeleg, nicht entschuldigen. Tools nie als Lücke. Sonst gehört die Lücke in `analyse.md` als Gesprächsvorbereitung.

**4. Schluss.** Keine Einschränkungen (Präsenz, Pendeln, Reisen, Teilzeit-Bedingungen): Die klärt der Nutzer im Gespräch. Der letzte Eindruck ist Vorfreude, keine Bedingung.
- Eintrittstermin nach `profil.md`, „Eckdaten“ (z. B. „Ich kann ab dem 01.12. bei euch starten.“ oder „Starten kann ich mit einem Monat Vorlauf.“).
- Gehaltsvorstellung **nur wenn gefordert**: „Meine Gehaltsvorstellung liegt bei X € brutto im Jahr.“ (eine Zahl oder enge Spanne, nie raten). Wert und Rahmen aus `profil.md`. Liegt die Spanne der Anzeige höher, höher ansetzen. Bei Teilzeit anteilig umrechnen.
- Aktiver Abschluss: Du „… und freue mich darauf, euch kennenzulernen.“ / Sie „… und freue mich darauf, Sie kennenzulernen.“ Nicht „Lasst uns sprechen.“

## Ansprache konsequent durchziehen
- Du: „ihr/euch/euer“ klein, „du“ klein. Keine Mischformen.
- Sie: „Sie/Ihnen/Ihr“ groß.
- Ton bei Du wärmer, aber nicht kumpelhaft. Bei Sie sachlicher, aber nicht steif.

## Qualitätscheck vor dem PDF
- [ ] Vier Fragen beantwortet: worauf ich Lust habe, 3 gesuchte Eigenschaften mit je einem kurzen Beleg, wie ich unterstütze, warum ich passe
- [ ] Nichts Technisches, kein Kleinkram (Fehlerfall, Datenfeld, einzelne Funktion)
- [ ] Ich-Form: eigene Leistung nie „gemeinsam/wir“, kein Zitat von Kollegen, keine losen Behauptungssätze
- [ ] Kein Wort aus der Floskel-Blacklist (`stil.md`)
- [ ] KI-Sprache-Check gemacht (Schritt 5a im Skill `bewerbung`), Cluster umgeschrieben
- [ ] Ansprache = Anzeige, durchgehend
- [ ] Jede Behauptung durch Lebenslauf oder `profil.md` gedeckt, nichts erfunden
- [ ] Alle Punkte unter „Grenzen“ in `profil.md` eingehalten (nie behaupten, nie erwähnen, nur im Gespräch)
- [ ] Einstieg passt zu „Rolle verstehen“ in `analyse.md` (Kernaufgabe, intern/extern), kein Verkaufston, keine Allgemeinweisheit
- [ ] Mehrwert für die Firma in einem Satz erkennbar, auf die Aufgaben der Anzeige bezogen
- [ ] Nichts unterstellt: kein Zweck, keine Zielgruppe, kein Anwendungsfall, keine Firmen-News, die nicht in der Anzeige stehen
- [ ] Firmenbezug über Kultur/Werte, mit eigenem Verhalten belegt, nicht benannt
- [ ] Einstieg ohne Vorwissen verständlich, keine rhetorische Frage
- [ ] Einladungsgrund klar: Nach dem Lesen kann man in einem Satz sagen, warum man den Nutzer einladen sollte
- [ ] Anzeige nicht gespiegelt: keine übernommenen Sätze oder Wendungen, keine Aufgaben als Zukunftsplan nachgesprochen
- [ ] Ein Absatz, ein Thema
- [ ] Kein Lebenslauf in Prosa (keine Stationen, Tool-Listen, Zeitachse)
- [ ] Kein Satz, der in jedem Anschreiben stehen könnte
- [ ] Privates höchstens ein Satz und nur mit echtem Bezug zur Firma (Abschnitt „Privat“ in `profil.md`)
- [ ] Firmenname, Stellentitel, Ansprechpartner richtig geschrieben
- [ ] Max. ein Drittel der Sätze beginnt mit „Ich“
- [ ] Register passend zum Niveau der Stelle, keine Umgangssprache, nie dritte Person über sich
- [ ] Keine Zahlen, die klein wirken, kein Größenvergleich in der Motivation
- [ ] Nach `pdf.sh`: 1 Seite, Sichtprüfung gemacht

## Varianten
- **E-Mail-/Portal-Text** (wenn Anschreiben als Freitext): 80–120 Wörter, gleicher Ton, gleiche Regeln (Motivation, gesuchte Eigenschaften, nichts Technisches, kein Spiegeln), Verweis auf Anhang, das Anschreiben nicht wörtlich doppeln. Betreffzeile wie Betreff oben.
- **Formularfragen statt Anschreiben:** Frage wörtlich lesen und genau diese Frage beantworten, nicht das Thema der Stelle („Was müsste die Rolle dir bieten …“ fragt nach den Bedingungen des Nutzers, nicht nach dem, was er liefert). Gleiche Regeln wie das Anschreiben.
- **Nachfassen** (nur auf ausdrücklichen Wunsch): 3–4 Sätze, freundlich, kein Vorwurf, ein neuer kleiner Aufhänger.

## Ausgabe
Befüllte `anschreiben.html` im Bewerbungsordner + Text des Anschreibens im Chat (zum schnellen Gegenlesen). Optional 1–2 alternative Einstiegssätze anbieten.
