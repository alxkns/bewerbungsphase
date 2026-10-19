#!/usr/bin/env python3
"""Lokaler Bewerbungs-Tracker: eine JSON-Datei je Bewerbung in daten/tracker/, nur Python-Standardbibliothek.

Datei daten/tracker/<id>.json = {"version": N, "geaendert": "…", "data": {firma, stelle, status, …}}.
Dieselben Dateien liest und schreibt das Dashboard (dashboard/tracker.html) direkt im Browser.
Die Versionsnummer verhindert, dass parallele Änderungen sich still überschreiben.

  python3 tracker/tracker.py list [--status S] [--min-match N]   alle (oder gefilterte) Bewerbungen als JSON
  python3 tracker/tracker.py get ID
  python3 tracker/tracker.py set ID '{"firma": ...}'             anlegen oder ganz ersetzen
  python3 tracker/tracker.py update ID '{"status": ...}' [--if-version N]   Felder ändern
  python3 tracker/tracker.py delete ID
  python3 tracker/tracker.py import DIR                           <id>.json-Dateien einlesen (z. B. Export aus claude.ai)
  python3 tracker/tracker.py serve [--port 8765]                  nur für Safari/Firefox: Dashboard über localhost
"""
import argparse, json, os, sys, tempfile
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ORDNER = ROOT / "daten" / "tracker"
DASHBOARD = ROOT / "dashboard" / "tracker.html"


class Konflikt(Exception):
    pass


def gueltige_id(i):
    if not i or len(i) > 120 or any(not (c.isascii() and (c.isalnum() or c in "_-")) for c in i):
        raise ValueError(f"Ungültige id {i!r}: nur A-Z a-z 0-9 _ - erlaubt")
    return i


def pfad(i):
    return ORDNER / f"{gueltige_id(i)}.json"


def holen(i):
    p = pfad(i)
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    return {"id": i, "version": d.get("version", 1), "data": d.get("data", d)}


def liste():
    ORDNER.mkdir(parents=True, exist_ok=True)
    return [holen(p.stem) for p in sorted(ORDNER.glob("*.json"))]


def schreiben(i, daten, merge, if_version=None):
    # ponytail: Versionsprüfung ohne Sperre, ein Rest-Risiko bleibt bei Änderungen in derselben Sekunde; Sperrdatei, falls das je stört
    if not isinstance(daten, dict):
        raise ValueError("Daten müssen ein JSON-Objekt sein")
    alt = holen(i)
    if if_version is not None and (alt is None or alt["version"] != if_version):
        raise Konflikt(f"Version passt nicht (aktuell {alt and alt['version']}), neu lesen")
    if merge and alt is None:
        raise KeyError(f"{i} gibt es nicht")
    neu = {**alt["data"], **daten} if merge else daten
    version = (alt["version"] if alt else 0) + 1
    ORDNER.mkdir(parents=True, exist_ok=True)
    inhalt = {"version": version, "geaendert": datetime.now().isoformat(timespec="seconds"), "data": neu}
    fd, tmp = tempfile.mkstemp(dir=ORDNER, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(inhalt, f, ensure_ascii=False, indent=1)
    os.replace(tmp, pfad(i))  # atomar: Leser sehen nie eine halbe Datei
    return {"id": i, "version": version, "data": neu}


def loeschen(i):
    p = pfad(i)
    if p.exists():
        p.unlink()
        return 1
    return 0


class Handler(BaseHTTPRequestHandler):
    def _antwort(self, code, body, typ="application/json; charset=utf-8"):
        roh = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", typ)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(roh)

    def _erlaubt(self):
        # Nur lokale Aufrufe: schützt vor DNS-Rebinding und Anfragen fremder Webseiten
        host = (self.headers.get("Host") or "").split(":")[0]
        if host not in ("localhost", "127.0.0.1"):
            self._antwort(403, {"fehler": "nur localhost"})
            return False
        if self.command != "GET" and not (self.headers.get("Content-Type") or "").startswith("application/json"):
            self._antwort(415, {"fehler": "Content-Type application/json nötig"})
            return False
        return True

    def _id(self):
        teile = self.path.split("?")[0].strip("/").split("/")
        return unquote(teile[2]) if len(teile) == 3 and teile[:2] == ["api", "bewerbungen"] else None

    def do_GET(self):
        if not self._erlaubt():
            return
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"):
            return self._antwort(200, DASHBOARD.read_bytes(), "text/html; charset=utf-8")
        if p == "/api/bewerbungen":
            return self._antwort(200, liste())
        self._antwort(404, {"fehler": "nicht gefunden"})

    def _schreiben(self, merge):
        if not self._erlaubt():
            return
        i = self._id()
        if i is None:
            return self._antwort(404, {"fehler": "nicht gefunden"})
        try:
            daten = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            self._antwort(200, schreiben(i, daten, merge))
        except Konflikt as e:
            self._antwort(409, {"fehler": str(e)})
        except (ValueError, KeyError) as e:
            self._antwort(400, {"fehler": str(e)})

    def do_PUT(self):
        self._schreiben(merge=False)

    def do_PATCH(self):
        self._schreiben(merge=True)

    def do_DELETE(self):
        if not self._erlaubt():
            return
        i = self._id()
        if i is None:
            return self._antwort(404, {"fehler": "nicht gefunden"})
        try:
            self._antwort(200, {"geloescht": loeschen(i)})
        except ValueError as e:
            self._antwort(400, {"fehler": str(e)})

    def log_message(self, *args):
        pass


def main(argv=None):
    p = argparse.ArgumentParser(description="Lokaler Bewerbungs-Tracker")
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--status")
    l.add_argument("--min-match", type=float)
    for name in ("get", "delete"):
        sub.add_parser(name).add_argument("id")
    for name in ("set", "update"):
        s = sub.add_parser(name)
        s.add_argument("id")
        s.add_argument("json")
        s.add_argument("--if-version", type=int)
    sub.add_parser("import").add_argument("dir")
    s = sub.add_parser("serve")
    s.add_argument("--port", type=int, default=8765)
    a = p.parse_args(argv)

    if a.cmd == "serve":
        print(f"Dashboard: http://localhost:{a.port}  (Strg+C beendet)")
        ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()
        return
    try:
        if a.cmd == "list":
            out = [d for d in liste()
                   if (not a.status or d["data"].get("status") == a.status)
                   and (a.min_match is None or (d["data"].get("match") or 0) >= a.min_match)]
        elif a.cmd == "get":
            out = holen(a.id)
            if out is None:
                sys.exit(f"{a.id} gibt es nicht")
        elif a.cmd in ("set", "update"):
            out = schreiben(a.id, json.loads(a.json), a.cmd == "update", a.if_version)
        elif a.cmd == "delete":
            out = {"geloescht": loeschen(a.id)}
        elif a.cmd == "import":
            n = 0
            for f in sorted(Path(a.dir).glob("*.json")):
                d = json.loads(f.read_text(encoding="utf-8"))
                schreiben(f.stem, d.get("data", d), merge=False)
                n += 1
            out = {"importiert": n}
    except (Konflikt, KeyError, ValueError) as e:
        sys.exit(str(e))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
