"""Gibt den Brieftext (Anrede bis Gruß) eines anschreiben.html als reinen Text aus."""
import html, re, sys

s = open(sys.argv[1], encoding="utf-8").read()
ps = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", s, re.S)]
start = next(i for i, p in enumerate(ps) if re.match(r"(Hallo|Hey|Guten Tag|Sehr geehrte)", p))
end = next(i for i, p in enumerate(ps) if i > start and "Grüße" in p)
print("\n\n".join(ps[start:end + 1]))
