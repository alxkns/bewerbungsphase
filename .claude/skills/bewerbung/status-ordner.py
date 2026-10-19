#!/usr/bin/env python3
"""Setzt den Tracker-Status als farbigen Finder-Tag auf jeden Ordner in daten/bewerbungen/ (nur macOS).

Aufruf: python3 .claude/skills/bewerbung/status-ordner.py <db-dump-dir>
<db-dump-dir> = Ordner mit <doc_id>.json aus ArtifactData list (out_dir, Collection bewerbungen).
Ordner werden weder umbenannt noch verschoben. Vorhandene Tags des Ordners werden ersetzt.
"""
import json, plistlib, subprocess, sys
from pathlib import Path

BEW = Path(__file__).resolve().parents[3] / "daten" / "bewerbungen"
# Finder-Farben: 1 grau, 2 grün, 3 lila, 4 blau, 5 gelb, 6 rot, 7 orange
FARBE = {"Entworfen": 7, "Versendet": 4, "Eingang bestätigt": 3, "Einladung": 2, "Angebot": 2,
         "Absage": 6, "Verworfen": 1, "Zurückgezogen": 1}

for f in sorted(Path(sys.argv[1]).glob("*.json")):
    doc = json.loads(f.read_text())
    doc = doc.get("data", doc)
    ordner = BEW / f.stem
    if not ordner.is_dir() or not doc.get("status"):
        continue
    tag = f"{doc['status']}\n{FARBE.get(doc['status'], 0)}"
    hexwert = plistlib.dumps([tag], fmt=plistlib.FMT_BINARY).hex()
    subprocess.run(["xattr", "-wx", "com.apple.metadata:_kMDItemUserTags", hexwert, str(ordner)], check=True)
    print(f"{doc['status']:18} {f.stem}")
