# Prozess-Learnings der automatischen Läufe

Gemeinsames Gedächtnis der Skills `stellensuche`, `bewerbungen-erstellen` und `gmail-abgleich`. Liegt als `daten/prozess-learnings.md` beim Nutzer, diese Vorlage ist der Startstand.

**Regeln für jeden Lauf:**
1. Zu Beginn diese Datei lesen. „Gültige Workarounds“ befolgen; bei technischen Details (URLs, Parameter, Tools) haben sie Vorrang vor dem Skill.
2. Am Ende einen Eintrag unter „Log“ anlegen (neueste oben): Datum, Uhrzeit, Skill, nur Probleme, Workarounds und Auffälligkeiten, keine Ergebnislisten. Lief alles glatt: eine Zeile „ohne Befund“.
3. Neuen Workaround gefunden, der funktioniert hat → unter „Gültige Workarounds“ ergänzen. Offenes Problem gelöst → dorthin verschieben. Workaround funktioniert nicht mehr → nach „Offene Probleme“ verschieben.
4. Suchprofil, Ausschlüsse, Match-Grenze und alles, was der Nutzer entscheidet, nie selbst ändern. Solche Ideen unter „Vorschläge an den Nutzer“ eintragen.
5. Datei kurz halten: Log-Einträge älter als 30 Tage löschen, sobald ihr Inhalt in Workarounds/Problemen steckt.

## Gültige Workarounds

**Stellensuche: Bundesagentur für Arbeit**
- Nur `pc/v6/jobs` funktioniert (v4: 403). Header `X-API-Key: jobboerse-jobsuche`.
- Felder: `stellenangebotsTitel`, `firma`, `referenznummer`, `stellenlokationen[0].adresse.ort`, `datumErsteVeroeffentlichung` (nicht `titel`/`refnr`). Bei 0 Treffern fehlt `ergebnisliste` ganz.
- Suche ist wörtlich: zusammengesetzte Wörter getrennt schreiben („Kampagnen Manager“), Reihenfolge und Gender-Form egal.
- `veroeffentlichtseit` filtert ungenau, selbst nach `datumErsteVeroeffentlichung` filtern.
- Remote: Filter `arbeitszeit=ho` liefert immer 0. Stattdessen ohne `wo` mit `was=<Begriff>%20remote` (nur Volltextsuche, Arbeitsmodell im Text prüfen).
- Volltext: Detailseite `https://www.arbeitsagentur.de/jobsuche/jobdetail/<referenznummer>`, JSON in `<script id="ng-state" type="application/json">`, Pfad `jobdetail.stellenangebotsBeschreibung`. Dort auch `gehaltsspanneVon/Bis`, `homeofficemoeglich`, `kontaktinformationen` (Ansprechpartner), `externeURL`/`allianzpartnerUrl` (Originalanzeige). Text abgeschnitten → Original lesen.
- „Stelle im Rahmen der Personalvermittlung“ auf der Detailseite → Vermittler.

**Stellensuche: weitere Quellen**
- Dubletten über Quellen hinweg: Abgleich über Firma (Kurzname) + Stellentitel, nicht nur über den Link (Aggregatoren verlinken anders als die Karriereseite).
- Indeed: direkt blockt Cloudflare. Einzelne Indeed-Anzeigen sind in der Browser-Pane lesbar.
- Glassdoor direkt: 403, nicht versuchen.
- StepStone: Suchseite `https://www.stepstone.de/jobs/<begriff-mit-bindestrich>/in-<ort>?radius=<km>&ag=age_7` (Browser-User-Agent) enthält JSON mit `title`, `url`, `companyName`, `workFromHome`. Detailseite per curl nicht lesbar: Originalanzeige beim Arbeitgeber suchen oder Browser-Pane.
- XING: Such-URL leitet um, immer `curl -L`. Suchseite enthält `VisibleJob`-Blöcke (`refreshedAt`, `salary` = XING-Schätzung). `applyUrl` führt oft zu Jobware (blockt curl).
- Viele Konzerne schalten dieselbe Stelle pro Standort und manche Firmen dieselbe Anzeige unter neuem Titel: neue Treffer bekannter Firmen gegen `anzeige.md` im Bewerbungsordner prüfen.

**Anzeige und Bewerbungsformular prüfen (ohne Browser)**
- JOIN: `<Anzeigen-URL>/apply` liefert JSON (`documentsConfig`, `applicationFormConfig`, Gehaltsband `salaryAmountFrom/To`, `workplaceType` ONSITE/HYBRID). Online-Status über `"status":"ONLINE"`, nicht per Textsuche.
- Personio: Pflichtfelder, `salary_information`, `employment_type` (befristet!) im Job-HTML (`application_form_fields_v2`), eigene Pflichtfelder im Server-HTML von `/job/<id>/apply`. `application_description` lesen (dort steht teils „kein Anschreiben“).
- Recruitee: `<Karriere-Domain>/api/offers/<slug>` (`options_cv`, `options_cover_letter`, `open_questions`, `hybrid`/`remote`, `published_at`).
- Greenhouse hinter Next.js: `<script id="__NEXT_DATA__">` per curl (`questions`, `first_published`, `pay_input_ranges`).
- SmartRecruiters: API `https://api.smartrecruiters.com/v1/companies/<Firma>/postings/<id>` ohne Key. Formular nur in der Browser-Pane (curl → Captcha).
- Workday: POST `https://<firma>.wd3.myworkdayjobs.com/wday/cxs/<firma>/<site>/jobs` mit `{"searchText": …}`, Details per GET `…/job/<externalPath>`. Am Wochenende teils Wartungsseite.
- umantis: Liste `https://recruitingapp-<nr>.de.umantis.com/Jobs/1`, Pflichtfelder über `mustfelder[...]`.
- onlyfy: eingebettetes JSON im Apply-HTML (name/label/type/required). Gleiche Stelle teils mehrfach je Standort.
- b-ite-Portale: eingebettetes JSON `window.BJP.config`. concludis: `landingpage.php` per `curl -L` → `/candidate/formapply`.
- Zoho Recruit: verstecktes Feld `jobs` im HTML (`Remote_Job`, `Date_Opened`).
- Karriereseiten mit JSON-LD `JobPosting`: `datePosted`, `baseSalary`, `jobLocationType: TELECOMMUTE` (= remote).
- Microsoft Power Pages, P&I Bewerber-Web, jobvector: nur in der Browser-Pane lesbar.
- „Kein Anschreiben gewünscht“ steht teils nur auf der Karriereseite: bei Portalen mit nur einem Upload-Feld dort nach „Anschreiben“ suchen.
- Anzeigen, die der Nutzer von LinkedIn schickt („Extern bewerben“ ist hinter dem Login): Originalanzeige auf der Karriereseite oder unter `<firma>.jobs.personio.de` suchen.
- E-Mail-Bewerbung: `mailto:`-Link im HTML liefert Empfänger und vorgegebenen Betreff; Postanschrift aus `/impressum`.

**Bewerbung erstellen**
- ArtifactData meldet beim ersten Aufruf öfter „network error“: einmal wiederholen.
- Mehrere Anforderungen: pro Ordner einen Subagenten, höchstens ca. 7 parallel, jeden frei gewordenen Platz mit dem nächsten Ordner belegen. Tracker-Updates nur im Hauptlauf.
- Recruiter-Bewerter als Subagenten: nur Text zurückgeben lassen, `recruiter.md` schreibt der Bau-Agent. Bau-Agent meldet sich zurück, bevor sein Bewerter fertig ist → per SendMessage fortsetzen lassen.
- Blinde Bewerter schlagen offene Fakten als belegt vor und Anzeigen-Echos: jeden Vorschlag gegen Master und `profil.md` prüfen. Dem Bewerter nur die erlaubten Abschnitte aus `analyse.md` geben.
- Browser-Pane: jeder Agent einen eigenen Tab (`tabs_create` + `tabId`).
- Lebenslauf rutscht auf 3 Seiten (meist nur der Unterschriftsblock): Text kürzen, nicht Schrift verkleinern. Leere Seite 3 mit `pdftotext -f 3` erkennen.
- Beim Neubau Fakten greppen, die aus alten Mappen kopiert, aber nicht im Master belegt sind, und entfernen.

**Shell (macOS/zsh)**
- `rm` mit Shell-Variable wird teils blockiert → `"${S:?}"/…` schreiben.
- `echo ====` scheitert (=-Expansion): Trenner in Anführungszeichen. Heredocs immer `<<'EOF'`.
- zsh teilt unquotierte Variablen nicht auf: Arrays oder Schleifen nutzen.
- `timeout` gibt es auf macOS nicht: `pdf.sh` direkt aufrufen, danach Seitenzahl prüfen.
- Python-`urllib` scheitert lokal teils an SSL-Zertifikaten → `curl` nehmen.

**Gmail-Abgleich**
- Zur Stichwortsuche eine zweite Suche nach Portal-Absendern ergänzen (`from:successfactors OR from:indeed OR from:personio …`). Job-Alerts (jobagent.stepstone, jobalert.indeed u. ä.) ignorieren.
- Indeed „Stellenanzeige entfernt“ ist keine Absage: Status nicht ändern, nur melden.
- Indeed „Bewerbung über Indeed: <Titel>“ zählt als Versand, nicht als Eingangsbestätigung.
- Absagen ohne Stellentitel bei Firmen mit mehreren Bewerbungen oder schon erfasster Absage nicht zuordnen, sondern melden.
- Hängt der Lauf lange (Start- und Endzeit per `date` vergleichen): am Ende Gmail ab dem Starttag noch einmal durchsuchen und den Tracker neu lesen.

## Offene Probleme

- **Blinde Recruiter-Runden streuen:** Die letzte Runde fällt teils unter die vorige, ohne dass sich etwas verschlechtert hat. Score = letzte Runde, die vorige Fassung bleibt in `vN/` als Alternative.
- **Recruiter-Check im automatischen Lauf:** `AskUserQuestion` gibt es dort nicht. Fakten-Fragen werden gesammelt, Änderungen, die eine Antwort brauchen, ausgelassen.
- **Freigaben im automatischen Lauf:** Ohne passenden Berechtigungsmodus bleiben Läufe an Freigaben hängen (Bash, Edit, ArtifactData). Der Nutzer löst das in der App.
- **Englische Bewerbungen:** `brieftext.py` erkennt „Dear“/„Kind regards“ nicht, humanizer-de ist nur für Deutsch kalibriert.
- **humanizer-de-Fehlalarme:** „doch“ als Konjunktion und „schon“ (= bereits) werden als Partikel gemeldet.
- **Stellen nur auf Karriereseiten** werden von keiner Quelle sicher erfasst.

## Vorschläge an den Nutzer

## Log
