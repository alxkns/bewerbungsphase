#!/bin/zsh
# HTML -> PDF über Chrome headless. Dateiname = <title> der HTML-Datei.
# Nutzung: pdf.sh daten/bewerbungen/<ordner>   (rendert alle *.html darin, fügt danach eine Gesamtmappe zusammen)
set -e
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
dir="${1:?Ordner angeben}"
cd "$dir"
pdfs=()
for f in anschreiben.html lebenslauf.html *.html(N); do
  [[ -f $f && ${pdfs[(Ie)$f]} -eq 0 ]] || continue
  name=$(sed -n 's:.*<title>\(.*\)</title>.*:\1:p' "$f" | head -1)
  out="$name.pdf"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
    --print-to-pdf="$PWD/$out" "file://$PWD/$f" 2>/dev/null
  echo "$out: $(pdfinfo "$out" | awk '/^Pages/{print $2}') Seite(n)"
  pdfs+=("$f" "$out")
done
# Gesamtmappe: Anschreiben + Lebenslauf (+ evtl. weitere) in einer Datei
files=(${pdfs:#*.html})
if (( ${#files} > 1 )); then
  firma=$(basename "$PWD" | sed 's/^[0-9-]*_//')
  name=$(sed -n 's:.*<title>Lebenslauf_\(.*\)</title>.*:\1:p' lebenslauf.html | head -1)
  pdfunite "${files[@]}" "Bewerbung_${firma}_${name}.pdf"
  echo "Bewerbung_${firma}_${name}.pdf: Mappe"
fi
