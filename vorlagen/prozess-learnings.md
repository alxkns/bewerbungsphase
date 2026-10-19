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
- Felder: `stellenangebotsTitel`, `firma`, `referenznummer`, `stellenlokationen[0].adresse.ort`, `homeofficemoeglich`, `vertragsdauer` (befristet?), `datumErsteVeroeffentlichung`, `veroeffentlichungszeitraum.von` (aktuelle Schaltung, bei neu geschalteten Anzeigen jünger) (nicht `titel`/`refnr`). Bei 0 Treffern fehlt `ergebnisliste` ganz.
- Suche ist wörtlich: zusammengesetzte Wörter getrennt schreiben („Kampagnen Manager“), Reihenfolge und Gender-Form egal.
- `veroeffentlichtseit` filtert ungenau, selbst nach `datumErsteVeroeffentlichung` filtern.
- Remote: Filter `arbeitszeit=ho` liefert immer 0. Stattdessen ohne `wo` mit `was=<Begriff>%20remote` bzw. `%20homeoffice` (nur Volltextsuche, Arbeitsmodell im Text prüfen).
- Volltext: Detailseite `https://www.arbeitsagentur.de/jobsuche/jobdetail/<referenznummer>`, JSON in `<script id="ng-state" type="application/json">`, Pfad `jobdetail.stellenangebotsBeschreibung`. Dort auch `gehaltsspanneVon/Bis`, `homeofficemoeglich`, `kontaktinformationen` (Ansprechpartner), `externeURL`/`allianzpartnerUrl` (Originalanzeige). Text abgeschnitten → Original lesen.
- „Stelle im Rahmen der Personalvermittlung“ auf der Detailseite → Vermittler.

**Stellensuche: weitere Quellen**
- Dubletten über Quellen hinweg: Abgleich über Firma (Kurzname) + Stellentitel, nicht nur über den Link (Aggregatoren verlinken anders als die Karriereseite).
- Indeed: direkt blockt Cloudflare. Einzelne Indeed-Anzeigen sind in der Browser-Pane lesbar.
- Glassdoor direkt: 403, nicht versuchen.
- StepStone: Suchseite `https://www.stepstone.de/jobs/<begriff-mit-bindestrich>/in-<ort>?radius=<km>&ag=age_7` (Browser-User-Agent) enthält JSON mit `title`, `url`, `companyName`, `workFromHome`. Detailseite per curl nicht lesbar: Originalanzeige beim Arbeitgeber suchen oder Browser-Pane.
- XING: Such-URL leitet um, immer `curl -L`. Suchseite enthält `VisibleJob`-Blöcke (`refreshedAt`, `salary` = XING-Schätzung, `companyNameOverride`). Detailseite per `curl -L` lesbar. `applyUrl` führt oft zu Jobware (blockt curl, Browser-Pane geht).
- XING spiegelt Jobware-Feeds weiter, nachdem der Arbeitgeber die Stelle entfernt hat: Originalanzeige beim Arbeitgeber immer prüfen (HTTP 200 = online, 404 = weg).
- Eingebaute Websuche ignoriert `site:` teils: Portal-Suchen dann direkt über die Suchseiten der Portale.
- Karriereseiten im Muster `…-de-j<Nr>.html`: JSON-LD mit `datePosted`, `baseSalary`, Ort; Tag „Präsenz / Mobil“ = hybrid.
- Stellenbaukästen: Mehrere kleine Firmen nutzen denselben Anzeigenbaukasten und schalten dieselbe Anzeige unter neuem Titel, Text identisch.
- Viele Konzerne schalten dieselbe Stelle pro Standort und manche Firmen dieselbe Anzeige unter neuem Titel: neue Treffer bekannter Firmen gegen `anzeige.md` im Bewerbungsordner prüfen.

**Anzeige und Bewerbungsformular prüfen (ohne Browser)**
- JOIN: `<Anzeigen-URL>/apply` liefert JSON (`documentsConfig`, `applicationFormConfig`, Gehaltsband `salaryAmountFrom/To`, `workplaceType` ONSITE/HYBRID). Online-Status über `"status":"ONLINE"`, nicht per Textsuche.
- Personio: Pflichtfelder, `salary_information`, `employment_type` (befristet!) im Job-HTML (`application_form_fields_v2`), eigene Pflichtfelder im Server-HTML von `/job/<id>/apply`. `application_description` lesen (dort steht teils „kein Anschreiben“).
- Recruitee: `<Karriere-Domain>/api/offers/<slug>` (`options_cv`, `options_cover_letter`, `open_questions`, `hybrid`/`remote`, `published_at`).
- Greenhouse hinter Next.js: `<script id="__NEXT_DATA__">` per curl (`questions`, `first_published`, `pay_input_ranges`).
- SmartRecruiters: API `https://api.smartrecruiters.com/v1/companies/<Firma>/postings/<id>` ohne Key (`releasedDate`, Adresse, `remote`/`hybrid`, Vertragsart). Formular nur in der Browser-Pane (curl → Captcha), Labels per JS aus dem Shadow DOM; Seite 2 nur nach Eingaben erreichbar.
- Workday: POST `https://<firma>.wd3.myworkdayjobs.com/wday/cxs/<firma>/<site>/jobs` mit `{"searchText": …}`, Details per GET `…/job/<externalPath>` (`canApply`, `startDate`). Am Wochenende teils Wartungsseite.
- softgarden: Bewerben-Link `jobdb.softgarden.de/.../applyonline/click?jp=<id>` per `curl -L` → `/application/?jobId=<id>`, Schalter `activate…`/`makeRequired…` = Pflichtfelder; `activateSalaryQuestionForm` ist nur eine Umfrage nach dem Absenden. Online über `"isActive":true`/`validThrough`.
- rexx: Formular unter der Anzeigen-URL mit `-f<Nr>` statt `-j<Nr>`, Pflichtfelder über `aria-required="true"`/Sternchen. Manche rexx-Portale zeigen das Formular erst nach Datenschutz-Zustimmung per POST → nicht prüfbar; JSON-LD der Anzeige liefert `datePosted` und Kennziffer.
- sopea/hrtool24: `ats.sopea-hr.com/ats/DirectRegister?Job=<id>` per curl, Pflichtfelder (*) und `<select>`-Optionen lesbar (z. B. ob die eigene Kündigungsfrist auswählbar ist).
- Liefert eine Seite gzip ohne Entpacken: `curl --compressed`.
- umantis: Liste `https://recruitingapp-<nr>.de.umantis.com/Jobs/1`, Pflichtfelder über `mustfelder[...]`.
- onlyfy: eingebettetes JSON im Apply-HTML (name/label/type/required). Gleiche Stelle teils mehrfach je Standort.
- b-ite-Portale: eingebettetes JSON `window.BJP.config`. concludis: `landingpage.php` per `curl -L` → `/candidate/formapply`.
- Zoho Recruit: verstecktes Feld `moduleMeta`/`jobs` im HTML (`Remote_Job`, `Date_Opened`, `Work_Experience`). Formular nur im Browser: Pane per `preview_start` mit URL öffnen, Cookie-Banner ablehnen, „Ich bin interessiert“, `document.body.innerText` lesen.
- Karriereseiten mit JSON-LD `JobPosting`: `datePosted`, `baseSalary`, `jobLocationType: TELECOMMUTE` (= remote).
- Nur in der Browser-Pane lesbar: Microsoft Power Pages (Pflichtfelder über `window.Page_Validators` und `required`), P&I Bewerber-Web (Pflichtfelder am Sternchen), jobvector (curl 403, nach ca. 5 s Wartezeit lesbar).
- „Kein Anschreiben gewünscht“ steht teils nur auf der Karriereseite: bei Portalen mit nur einem Upload-Feld dort nach „Anschreiben“ suchen.
- Anzeigen, die der Nutzer von LinkedIn schickt („Extern bewerben“ ist hinter dem Login): Originalanzeige auf der Karriereseite oder unter `<firma>.jobs.personio.de` suchen.
- E-Mail-Bewerbung: `mailto:`-Link im HTML liefert Empfänger und vorgegebenen Betreff; Postanschrift aus `/impressum`.

**Bewerbung erstellen**
- ArtifactData meldet beim ersten Aufruf öfter „network error“: einmal wiederholen.
- Mehrere Anforderungen: pro Ordner einen Subagenten, höchstens ca. 7 parallel, jeden frei gewordenen Platz mit dem nächsten Ordner belegen. Tracker-Updates nur im Hauptlauf.
- Recruiter-Bewerter als Subagenten: nur Text zurückgeben lassen, `recruiter.md` schreibt der Bau-Agent. Bau-Agent meldet sich zurück, bevor sein Bewerter fertig ist → per SendMessage fortsetzen lassen.
- Blinde Bewerter schlagen offene Fakten als belegt vor und Anzeigen-Echos: jeden Vorschlag gegen Master und `profil.md` prüfen. Dem Bewerter nur die erlaubten Abschnitte aus `analyse.md` geben.
- Browser-Pane: jeder Agent einen eigenen Tab (`tabs_create` + `tabId`). Ist die Pane geschlossen, scheitert `tabs_create`: erst per `preview_start` mit URL öffnen.
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
- Indeed „Neuigkeiten zu Ihrer Bewerbung von <Firma>“ kann eine Absage sein („leider … nicht berücksichtigt“): Snippet reicht nicht, Mail lesen.
- Erinnerungen von Bewerbungsportalen („Bewerbung fortsetzen?“, „Noch 5 Minuten“) ändern keinen Status, nur melden.
- Absagen ohne Stellentitel bei Firmen mit mehreren Bewerbungen oder schon erfasster Absage nicht zuordnen, sondern melden.
- Hängt der Lauf lange (Start- und Endzeit per `date` vergleichen): am Ende Gmail ab dem Starttag noch einmal durchsuchen und den Tracker neu lesen.

## Offene Probleme

- **Blinde Recruiter-Runden streuen:** Die letzte Runde fällt teils unter die vorige, ohne dass sich etwas verschlechtert hat. Score = letzte Runde, die vorige Fassung bleibt in `vN/` als Alternative.
- **Recruiter-Check im automatischen Lauf:** Rückfragen an den Nutzer gibt es dort nicht. Fakten-Fragen werden gesammelt, Änderungen, die eine Antwort brauchen, ausgelassen.
- **Freigaben im automatischen Lauf:** Ohne passenden Berechtigungsmodus bleiben Läufe an Freigaben hängen (Bash, Edit, ArtifactData). Der Nutzer löst das in der App.
- **Englische Bewerbungen:** `brieftext.py` erkennt „Dear“/„Kind regards“ nicht, humanizer-de ist nur für Deutsch kalibriert.
- **humanizer-de-Fehlalarme:** „doch“ als Konjunktion und „schon“ (= bereits) werden als Partikel gemeldet.
- **Stellen nur auf Karriereseiten** werden von keiner Quelle sicher erfasst.
- **StepStone:** Pro Begriff nur die erste Ergebnisseite (ca. 25) getestet, Seiten 2+ (`&page=2`) ungeprüft.

## Vorschläge an den Nutzer

## Log
