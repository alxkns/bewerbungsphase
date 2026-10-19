---
name: lebenslauf-anpassen
description: Tabellarischen Lebenslauf des Nutzers (deutsches Format) für eine konkrete Stelle anpassen, also umsortieren, umformulieren und kürzen, ohne etwas zu erfinden. Nutzen bei „Lebenslauf anpassen“, „CV für die Stelle“ oder als Schritt 4 im Skill bewerbung.
---

# Lebenslauf anpassen

Master: `daten/bewerbungen/_vorlage/lebenslauf.html`. **Nie den Master für eine Bewerbung ändern.** Kopie in den Bewerbungsordner, dort anpassen.

## Deutsches Format (im Master umsetzen, dann so lassen)
- Tabellarisch, antichronologisch (Neuestes zuerst), Zeitangaben `MM/JJJJ`
- Kopf mit Kontakt, Foto optional, kein Geburtsdatum
- Ort, Name + Unterschrift am Ende
- Max. 2 Seiten, Lücken > 3 Monate erklärt
- Neutral formuliert, keine Ansprache (Du/Sie gilt nur fürs Anschreiben)

## Die Wahrheitslinie

| Erlaubt | Verboten |
|---|---|
| Reihenfolge von Stichpunkten und Kenntnissen ändern | Tools, Zahlen, Titel oder Zeiträume erfinden oder aufblähen |
| Begriffe der Anzeige verwenden, wenn sie dasselbe meinen | Kenntnisse höher einstufen als sie sind |
| Irrelevantes kürzen oder streichen | Verantwortung behaupten, die es nicht gab |
| Untertitel und Profiltext auf die Rolle zuschneiden | Stationen weglassen, sodass Lücken entstehen |

Neue Fakten, die der Nutzer im Chat nennt: zuerst in den Master, dann in die Kopie.

**Alles muss stimmen, aber nicht alles muss rein.** Keine ungefragten Abschwächungen: Was nur getestet oder in Grundzügen bekannt ist („Ehrliches Level“ in `profil.md`), kommt nur rein, wenn die Anzeige es als Muss oder Kann nennt, dann ehrlich eingestuft. Produktiv Genutztes steht ohne Zusatz. Keine Erklärungen, die nur Fragen aufwerfen (das ist Gesprächsstoff).

Zusätzlich erlaubt: „Bausteine“ aus `daten/profil.md` als Stichpunkt, wenn sie zur Stelle passen. **Nie in den Lebenslauf:** alles unter „Grenzen“ in `profil.md` (nie behaupten, nie erwähnen, nur im Gespräch). Feste Lebenslauf-Regeln des Nutzers stehen unter „Stil-Vorlieben“.

## Was pro Stelle angepasst wird

1. **`<title>`** bleibt `Lebenslauf_<Name>`.
2. **Untertitel** im Kopfband (`.untertitel`): Rolle der Anzeige aufgreifen, solange sie ehrlich passt.
3. **Profil** (3–5 Sätze): erster Satz auf die Kernanforderung der Stelle. Letzter Satz: was der Nutzer dort machen will (Richtung „Motivation und Charakter“ in `profil.md`). Stil wie `bewerbung/stil.md`, aber sachlicher als das Anschreiben.
4. **Stichpunkte der aktuellen Station:** die zur Stelle passendsten nach oben. Für Fachrollen Methoden- und Tool-Details sichtbar lassen, für Führungs- und Operations-Rollen eher Wirkung betonen. Unpassendes kürzen.
5. **Führungs- und Querschnittsaufgaben:** für Führungs- oder Operations-Rollen ausbauen, für reine Fachrollen knapp halten.
6. **Kenntnisse:** Kategorien in Reihenfolge der Anzeige. Schlagwörter aus `analyse.md` in exakter Schreibweise, sofern belegt.
7. **Nebenstationen:** knapp halten, nur ausbauen, wenn sie für die Stelle etwas belegen.

## Schlagwörter (ATS)
Viele Firmen filtern per Software. Wichtige Begriffe der Anzeige 1–2× natürlich einbauen (Profil + Stichpunkt oder Kenntnisse). Kein Keyword-Stuffing, keine versteckten Wörter.

## Layout-Regeln
- Klassen aus `vorlagen/style.css` verwenden (`.eintrag`, `.zeit`, `.firma`, `.info`, `h4`, `ul`), keine Inline-Styles
- Nach `pdf.sh` Sichtprüfung: max. 2 Seiten, keine Überschrift allein am Seitenende, Unterschrift-Block nicht allein auf neuer Seite. Zu lang → Text kürzen, nicht Schrift verkleinern.

## Ausgabe
Angepasste `lebenslauf.html` im Bewerbungsordner + kurze Liste im Chat: was umgestellt, was gekürzt, welche Schlagwörter rein.
