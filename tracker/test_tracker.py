#!/usr/bin/env python3
"""Selbsttest des lokalen Trackers: python3 tracker/test_tracker.py"""
import json, tempfile, threading, urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import tracker as t

ID = "2026-10-20_Beispiel-GmbH"
with tempfile.TemporaryDirectory() as tmp:
    t.ORDNER = Path(tmp) / "tracker"

    d = t.schreiben(ID, {"firma": "Beispiel GmbH", "status": "Vorschlag", "match": 75}, merge=False)
    assert d["version"] == 1
    d = t.schreiben(ID, {"status": "Angefordert"}, merge=True, if_version=1)
    assert d["data"] == {"firma": "Beispiel GmbH", "status": "Angefordert", "match": 75} and d["version"] == 2
    datei = json.loads((t.ORDNER / f"{ID}.json").read_text())
    assert datei["version"] == 2 and datei["data"]["status"] == "Angefordert"   # Format, das das Dashboard liest
    for fehler, i, args in [(t.Konflikt, ID, ({"status": "x"}, True, 1)), (KeyError, "fehlt", ({"a": 1}, True, None))]:
        try:
            t.schreiben(i, *args)
            raise AssertionError(f"{fehler.__name__} erwartet")
        except fehler:
            pass
    for schlecht in ["../x", "a b", "ä", ""]:
        try:
            t.schreiben(schlecht, {}, merge=False)
            raise AssertionError("ungültige id angenommen")
        except ValueError:
            pass
    assert not list(t.ORDNER.glob("*.tmp"))

    dump = Path(tmp) / "dump"
    dump.mkdir()
    (dump / "2026-10-21_Import-AG.json").write_text(json.dumps({"data": {"firma": "Import AG", "status": "Versendet"}}))
    t.main(["import", str(dump)])
    t.main(["delete", ID])
    assert [d["id"] for d in t.liste()] == ["2026-10-21_Import-AG"]

    # HTTP (Fallback für Safari/Firefox): lesen, ändern, fremder Host und falscher Content-Type werden abgewiesen
    srv = ThreadingHTTPServer(("127.0.0.1", 0), t.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"

    def req(method, path, body=None, typ="application/json", host=None):
        r = urllib.request.Request(base + path, method=method, data=body and json.dumps(body).encode())
        if body is not None:
            r.add_header("Content-Type", typ)
        if host:
            r.add_header("Host", host)
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    code, body = req("GET", "/api/bewerbungen")
    assert code == 200 and json.loads(body)[0]["id"] == "2026-10-21_Import-AG"
    assert req("PATCH", "/api/bewerbungen/2026-10-21_Import-AG", {"status": "Absage"})[0] == 200
    assert t.holen("2026-10-21_Import-AG")["data"]["status"] == "Absage"
    assert req("PATCH", "/api/bewerbungen/2026-10-21_Import-AG", {"status": "x"}, typ="text/plain")[0] == 415
    assert req("GET", "/api/bewerbungen", host="evil.example")[0] == 403
    assert req("GET", "/")[0] == 200
    srv.shutdown()

print("tracker ok")
