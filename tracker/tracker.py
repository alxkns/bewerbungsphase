#!/usr/bin/env python3
"""Lokaler Bewerbungs-Tracker: SQLite-Datei daten/tracker.sqlite, nur Python-Standardbibliothek.

Ein Dokument pro Bewerbung (id = Ordnername, Felder als JSON), mit Versionsnummer gegen
gleichzeitiges Überschreiben. Gleiche Felder wie der claude.ai-Tracker.

  python3 tracker/tracker.py list [--status S] [--min-match N]   alle (oder gefilterte) Bewerbungen als JSON
  python3 tracker/tracker.py get ID
  python3 tracker/tracker.py set ID '{"firma": ...}'             anlegen oder ganz ersetzen
  python3 tracker/tracker.py update ID '{"status": ...}' [--if-version N]   Felder ändern
  python3 tracker/tracker.py delete ID
  python3 tracker/tracker.py export DIR                           je Bewerbung DIR/<id>.json (für status-ordner.py)
  python3 tracker/tracker.py import DIR                           <id>.json-Dateien einlesen (z. B. Export aus claude.ai)
  python3 tracker/tracker.py serve [--port 8765]                  Dashboard unter http://localhost:8765
"""
import argparse, json, sqlite3, sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "daten" / "tracker.sqlite"
DASHBOARD = ROOT / "dashboard" / "tracker.html"


class Konflikt(Exception):
    pass


def verbinden(pfad=None):
    pfad = pfad or DB
    pfad.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(pfad, timeout=30, isolation_level=None)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("CREATE TABLE IF NOT EXISTS bewerbungen (id TEXT PRIMARY KEY, data TEXT NOT NULL, "
                "version INTEGER NOT NULL, geaendert TEXT NOT NULL)")
    return con


def gueltige_id(i):
    if not i or len(i) > 120 or any(not (c.isascii() and (c.isalnum() or c in "_-")) for c in i):
        raise ValueError(f"Ungültige id {i!r}: nur A-Z a-z 0-9 _ - erlaubt")
    return i


def zeile(r):
    return {"id": r[0], "version": r[2], "data": json.loads(r[1])}


def liste(con):
    return [zeile(r) for r in con.execute("SELECT id, data, version FROM bewerbungen ORDER BY id")]


def holen(con, i):
    r = con.execute("SELECT id, data, version FROM bewerbungen WHERE id = ?", (i,)).fetchone()
    return zeile(r) if r else None


def schreiben(con, i, daten, merge, if_version=None):
    if not isinstance(daten, dict):
        raise ValueError("Daten müssen ein JSON-Objekt sein")
    gueltige_id(i)
    con.execute("BEGIN IMMEDIATE")
    try:
        alt = holen(con, i)
        if if_version is not None and (alt is None or alt["version"] != if_version):
            raise Konflikt(f"Version passt nicht (aktuell {alt and alt['version']}), neu lesen")
        if merge and alt is None:
            raise KeyError(f"{i} gibt es nicht")
        neu = {**alt["data"], **daten} if merge else daten
        version = (alt["version"] if alt else 0) + 1
        con.execute("INSERT OR REPLACE INTO bewerbungen VALUES (?, ?, ?, ?)",
                    (i, json.dumps(neu, ensure_ascii=False), version, datetime.now().isoformat(timespec="seconds")))
        con.execute("COMMIT")
    except BaseException:
        con.execute("ROLLBACK")
        raise
    return {"id": i, "version": version, "data": neu}


def loeschen(con, i):
    return con.execute("DELETE FROM bewerbungen WHERE id = ?", (i,)).rowcount


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
        pfad = self.path.split("?")[0]
        if pfad in ("/", "/index.html"):
            seite = DASHBOARD.read_text(encoding="utf-8")
            html = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
                    + seite + "</body></html>")
            return self._antwort(200, html.encode(), "text/html; charset=utf-8")
        if pfad == "/api/bewerbungen":
            with verbinden() as con:
                return self._antwort(200, liste(con))
        self._antwort(404, {"fehler": "nicht gefunden"})

    def _schreiben(self, merge):
        if not self._erlaubt():
            return
        i = self._id()
        if i is None:
            return self._antwort(404, {"fehler": "nicht gefunden"})
        try:
            daten = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            with verbinden() as con:
                self._antwort(200, schreiben(con, i, daten, merge))
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
        with verbinden() as con:
            self._antwort(200, {"geloescht": loeschen(con, i)})

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
    for name in ("export", "import"):
        sub.add_parser(name).add_argument("dir")
    s = sub.add_parser("serve")
    s.add_argument("--port", type=int, default=8765)
    a = p.parse_args(argv)

    if a.cmd == "serve":
        print(f"Dashboard: http://localhost:{a.port}  (Strg+C beendet)")
        ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()
        return
    con = verbinden()
    try:
        if a.cmd == "list":
            out = [d for d in liste(con)
                   if (not a.status or d["data"].get("status") == a.status)
                   and (a.min_match is None or (d["data"].get("match") or 0) >= a.min_match)]
        elif a.cmd == "get":
            out = holen(con, a.id)
            if out is None:
                sys.exit(f"{a.id} gibt es nicht")
        elif a.cmd in ("set", "update"):
            out = schreiben(con, a.id, json.loads(a.json), a.cmd == "update", a.if_version)
        elif a.cmd == "delete":
            out = {"geloescht": loeschen(con, a.id)}
        elif a.cmd == "export":
            ziel = Path(a.dir)
            ziel.mkdir(parents=True, exist_ok=True)
            for d in liste(con):
                (ziel / f"{d['id']}.json").write_text(json.dumps(d["data"], ensure_ascii=False, indent=1), encoding="utf-8")
            out = {"exportiert": len(liste(con))}
        elif a.cmd == "import":
            n = 0
            for f in sorted(Path(a.dir).glob("*.json")):
                d = json.loads(f.read_text(encoding="utf-8"))
                schreiben(con, f.stem, d.get("data", d), merge=False)
                n += 1
            out = {"importiert": n}
    except (Konflikt, KeyError, ValueError) as e:
        sys.exit(str(e))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
