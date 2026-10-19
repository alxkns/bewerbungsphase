# Anleitung für KI-Assistenten

Dieses Repo hilft einer Person bei der Bewerbung auf Stellen in Deutschland: Stellen finden und analysieren, die Person kennenlernen, Lebenslauf und Anschreiben bauen, prüfen, nachhalten. Gilt für jedes Werkzeug (Claude Code, Codex, Cursor, Gemini CLI …). Antworte auf Deutsch.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `.claude/skills/<name>/SKILL.md` | Die Abläufe. „Skill X“ im Text heißt: `.claude/skills/X/SKILL.md` lesen und befolgen. |
| `vorlagen/` | Layout und leere Vorlagen, werden bei der Einrichtung nach `daten/` kopiert |
| `daten/` | Alles Persönliche: Profil, Suchprofil, Lebenslauf, Bewerbungen, Tracker. Nie committen (steht in `.gitignore`). |
| `dashboard/tracker.html` | Dashboard für den Bewerbungs-Tracker |
| `.githooks/pre-commit` | Sperre: kein Commit mit Dateien aus `daten/` oder Wörtern aus `daten/privat.txt` |
| `tracker/tracker.py` | Lokaler Tracker: liest und schreibt `daten/tracker/<id>.json` (nur Python-Standardbibliothek). Das Dashboard öffnet der Nutzer direkt als Datei im Browser. |

Alle Pfade in den Skills sind relativ zum Hauptordner des Repos.

## Welcher Ablauf wann

| Anlass | Skill |
|---|---|
| Erster Start, `daten/profil.md` fehlt, „richte mich ein“ | `einrichtung` |
| „Was verlangt der Markt?“, nach der Einrichtung | `marktanalyse` |
| „Lern mich kennen“, Profil vervollständigen, offene Fakten-Fragen | `kennenlernen` |
| Stellenanzeige (Link, Text, PDF), „bewirb mich bei …“ | `bewerbung` (ruft `stellenanalyse`, `unternehmensanalyse`, `lebenslauf-anpassen`, `anschreiben`, `recruiter`, `humanizer-de` auf) |
| „Lohnt sich die Stelle?“ | `stellenanalyse` |
| Einladung zum Gespräch | `vorstellungsgespraech` |
| Gehaltsfrage, Angebot | `gehaltsverhandlung` |
| Rollen- oder Branchenwechsel erklären | `quereinstieg` |
| Neue Stellen suchen (auch als Routine) | `stellensuche` |
| Angeforderte Bewerbungen bauen (auch als Routine) | `bewerbungen-erstellen` |
| Gmail nach Antworten durchsuchen (auch als Routine) | `gmail-abgleich` |
| Neue Version holen, „update dich“ | `aktualisieren` |

## Grundregeln

- **Nichts erfinden.** Fakten nur aus `daten/bewerbungen/_vorlage/lebenslauf.html` (Master) und `daten/profil.md`. Fehlt etwas: fragen oder offen lassen.
- **Nie etwas versenden.** Keine Mails, keine Formulare, keine Bewerbungen abschicken. Das macht der Nutzer selbst.
- **Grenzen einhalten:** Abschnitt „Grenzen“ in `daten/profil.md` gilt für alle Texte.
- **Entscheidungen des Nutzers nicht ändern:** Ausschlüsse, Match-Grenze, Suchprofil. Vorschläge dazu nur nennen.
- **`daten/` ist privat.** Nichts daraus in Commits, Issues oder an fremde Dienste. Die Git-Sperre (`git config core.hooksPath .githooks`) muss eingeschaltet sein.
- **Methode und Person trennen.** Alles außerhalb von `daten/` ist die Methode, für alle Nutzer gleich. Nur ändern, wenn der Nutzer ausdrücklich die Methode verbessern will. Neue Regeln, Vorlieben, Fakten oder Quellen des Nutzers gehören nach `daten/` (`profil.md` → „Grenzen“, „Stil-Vorlieben“; `suchprofil.md` → „Eigene Quellen“; `eigenes-layout.css` für Schrift und Farben). Im Zweifel `daten/`. Nur so kann jeder Nutzer per `git pull` (Skill `aktualisieren`) updaten, ohne Konflikte und ohne etwas zu verlieren.
- **Wird die Methode verbessert:** keine Namen, Firmen, Zahlen oder Beispiele des Nutzers in Skills übernehmen, nur die allgemeine Regel mit neutralem Beispiel. Ändert sich das Format von `profil.md` oder `suchprofil.md`, die Vorlage in `vorlagen/` anpassen; `aktualisieren` überträgt neue Abschnitte zu den Nutzern.

## Werkzeuge

Die Skills nennen Fähigkeiten, manchmal mit dem Namen des Claude-Werkzeugs. Ohne das Werkzeug gilt der Ersatz:

| In den Skills | Claude | Ohne dieses Werkzeug |
|---|---|---|
| Auswahlfrage an den Nutzer | `AskUserQuestion` | Nummerierte Optionen im Chat, auf Antwort warten |
| Seite abrufen | `WebFetch` | `curl -sL -A 'Mozilla/5.0' '<url>'` |
| Websuche | `WebSearch` | Websuche des Werkzeugs; gibt es keine: nur die Quellen per `curl` |
| Bild oder PDF ansehen | Read | Bildansicht des Werkzeugs; sonst `pdftotext -layout` und das dem Nutzer sagen |
| Browser | Browser-Pane | Browser-Werkzeug; gibt es keins: Seite überspringen und melden |
| Subagent (eigene Instanz ohne Vorwissen) | `Agent` | Neue Sitzung per Kommandozeile mit eigenem Auftrag (z. B. `claude -p`, `codex exec`, `gemini -p`). Geht das nicht: nacheinander selbst erledigen; beim blinden Bewerter im Recruiter-Check vorher nur Anzeige und Endfassung lesen und das in `recruiter.md` vermerken |
| `<scratchpad>` | Scratchpad der Sitzung | temporärer Ordner, z. B. `mktemp -d` |
| Tracker | `tracker/tracker.py` oder `ArtifactData` | immer `tracker/tracker.py` (lokaler Tracker) |

**Nur mit Claude:** Dashboard als claude.ai-Artifact, Routinen über die Claude-Desktop-App, Gmail über den Claude-Connector. Für jedes andere Werkzeug gibt es den lokalen Tracker und Routinen per `cron` (Skill `einrichtung`, Schritte 7 und 8). Gmail braucht dann einen eigenen Gmail-Zugriff des Werkzeugs.

Die Anleitungen sind mit Claude erprobt. Andere Modelle halten Regeln wie „nichts erfinden“ oder „Anzeige nicht spiegeln“ womöglich weniger streng ein: Ergebnisse vor dem Versenden genau lesen.
