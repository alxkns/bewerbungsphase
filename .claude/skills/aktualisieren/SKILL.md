---
name: aktualisieren
description: Bewerbungshelfer auf die neueste Version bringen, ohne persönliche Daten zu verlieren. Holt die neue Version per git, erklärt die Neuerungen, ergänzt neue Abschnitte und Felder aus vorlagen/ in daten/ (ohne etwas zu überschreiben) und zieht Dashboard und Vorlagen nach. Nutzen bei „update dich“, „aktualisieren“, „gibt es eine neue Version?“.
---

# Aktualisieren: neue Version holen, nichts verlieren

Grundsatz: `daten/` gehört dem Nutzer. Hier wird nur **ergänzt**, nie überschrieben oder gelöscht. Alles außerhalb von `daten/` ist die Methode und kommt aus dem Repo.

## 1. Ausgangslage prüfen

```bash
git status --short
```
- Geänderte Dateien außerhalb von `daten/` (Skills, Vorlagen, Dashboard …): **anhalten.** Dem Nutzer zeigen, was geändert ist (`git diff --stat`), und klären: Ist es persönlich (dann nach `daten/` übertragen, z. B. in `profil.md` → „Grenzen“ oder „Stil-Vorlieben“), soll es als Verbesserung ins Repo, oder kann es weg? Erst nach seiner Antwort weiter, nie selbst verwerfen.
- `daten/` taucht nicht auf (steht in `.gitignore`). Tut es doch: anhalten und melden.

## 2. Neue Version holen

```bash
alt=$(git rev-parse HEAD)
git pull --ff-only
git config core.hooksPath .githooks
git log --oneline "$alt"..HEAD
```
Scheitert `--ff-only`: nichts erzwingen, dem Nutzer den Fehler zeigen. Keine Neuerungen: mit einem Satz beenden.

Die Commits in zwei bis fünf Sätzen auf Deutsch zusammenfassen: was ist neu, was ändert sich für den Nutzer.

## 3. Vorlagen nach `daten/` übertragen (nur ergänzen)

Welche Vorlagen sich geändert haben: `git diff --stat "$alt"..HEAD -- vorlagen/ dashboard/`.

- **`vorlagen/profil.md` → `daten/profil.md`** und **`vorlagen/suchprofil.md` → `daten/suchprofil.md`:** Jede `##`-Überschrift der Vorlage, die in `daten/` fehlt, samt leerem Vorlagentext an derselben Stelle einfügen (nach dem Abschnitt, der in der Vorlage davor steht). Innerhalb bestehender Abschnitte neue Feldzeilen (`- Feld:`, Tabellenzeilen) ergänzen, die es noch nicht gibt. Bestehende Inhalte nie ändern. Umbenannte Abschnitte: nicht raten, dem Nutzer zeigen.
- **`vorlagen/prozess-learnings.md` → `daten/prozess-learnings.md`:** neue Zeilen unter „Gültige Workarounds“ und „Offene Probleme“ übernehmen, die es dort noch nicht gibt. Log und „Vorschläge an den Nutzer“ nicht anfassen.
- **`vorlagen/anschreiben.html` und `vorlagen/lebenslauf.html`:** Änderungen außerhalb der `{Platzhalter}` und Inhalte (z. B. eine neue `<link>`-Zeile im Kopf, eine geänderte Klasse) genauso in `daten/bewerbungen/_vorlage/anschreiben.html` und `lebenslauf.html` nachziehen. Inhalte, Texte und Foto nie anfassen. Fertige Bewerbungsordner bleiben, wie sie sind.
- **Fehlende Dateien:** gibt es eine Vorlage, deren Gegenstück in `daten/` fehlt (z. B. neu hinzugekommen), mit `cp -n` anlegen.

## 4. Tracker und Dashboard

- `python3 tracker/test_tracker.py` muss „tracker ok“ melden. Sonst anhalten und melden.
- **Lokal:** nichts zu tun, das Dashboard lädt die neue Fassung beim nächsten Öffnen.
- **claude.ai** (laut `daten/suchprofil.md`, nur mit Claude): Hat sich `dashboard/tracker.html` geändert, das Artifact neu veröffentlichen (`Artifact` publish mit `url` = Tracker-URL, `file_path` `dashboard/tracker.html`). Die Daten bleiben erhalten.
- **Routinen:** Die geplanten Aufträge verweisen nur auf Skills, sie laufen automatisch mit der neuen Fassung. Gibt es einen neuen Routine-Skill, ihn dem Nutzer anbieten (Skill `einrichtung`, Schritt 8).

## 5. Abschluss

Kurz im Chat: Version (`git log -1 --format='%h %s'`), was neu ist, was in `daten/` ergänzt wurde (Datei, Abschnitt), was der Nutzer selbst tun sollte (z. B. neue Felder im Profil ausfüllen, dann Skill `kennenlernen`).
