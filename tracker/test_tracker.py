#!/usr/bin/env python3
"""Selbsttest des lokalen Trackers: python3 tracker/test_tracker.py"""
import json, tempfile, threading, urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import tracker as t

with tempfile.TemporaryDirectory() as tmp:
    t.DB = Path(tmp) / "test.sqlite"
    con = t.verbinden()

    d = t.schreiben(con, "2026-10-20_Beispiel-GmbH", {"firma": "Beispiel GmbH", "status": "Vorschlag", "match": 75}, merge=False)
    assert d["version"] == 1
    d = t.schreiben(con, "2026-10-20_Beispiel-GmbH", {"status": "Angefordert"}, merge=True, if_version=1)
    assert d["data"] == {"firma": "Beispiel GmbH", "status": "Angefordert", "match": 75} and d["version"] == 2
    for fehler, args in [(t.Konflikt, ({"status": "x"}, True, 1)), (KeyError, ({"a": 1}, True, None))]:
        try:
            t.schreiben(con, "2026-10-20_Beispiel-GmbH" if fehler is t.Konflikt else "fehlt", *args)
            raise AssertionError(f"{fehler.__name__} erwartet")
        except fehler:
            pass
    for schlecht in ["../x", "a b", "ä", ""]:
        try:
            t.schreiben(con, schlecht, {}, merge=False)
            raise AssertionError("ungültige id angenommen")
        except ValueError:
            pass
    assert t.holen(con, "2026-10-20_Beispiel-GmbH")["data"]["status"] == "Angefordert"

    t.main(["export", tmp + "/dump"])
    t.main(["delete", "2026-10-20_Beispiel-GmbH"])
    assert t.liste(con) == []
    t.main(["import", tmp + "/dump"])
    assert t.liste(con)[0]["data"]["firma"] == "Beispiel GmbH"

    # HTTP: lesen, ändern, fremder Host und falscher Content-Type werden abgewiesen
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
    assert code == 200 and json.loads(body)[0]["id"] == "2026-10-20_Beispiel-GmbH"
    assert req("PATCH", "/api/bewerbungen/2026-10-20_Beispiel-GmbH", {"status": "Entworfen"})[0] == 200
    assert t.holen(con, "2026-10-20_Beispiel-GmbH")["data"]["status"] == "Entworfen"
    assert req("PATCH", "/api/bewerbungen/2026-10-20_Beispiel-GmbH", {"status": "x"}, typ="text/plain")[0] == 415
    assert req("GET", "/api/bewerbungen", host="evil.example")[0] == 403
    assert req("GET", "/")[0] == 200
    srv.shutdown()

print("tracker ok")
