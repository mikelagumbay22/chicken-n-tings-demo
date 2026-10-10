"""Static ban/rule checks over dist/ for the Chicken "N" Tings demo."""
import json, re, html as H
from pathlib import Path
D = Path("/workspace/sites/chicken-n-tings/dist")
BANNER = "Business package demo concept"
FOOTER = 'Demo concept, not affiliated with or approved by Chicken "N" Tings.'
BADGE = "Illustrative image, not a photo of the restaurant's food"
TEL = 'href="tel:+19056779888"'
fails, lines = [], []
def ok(c, m): lines.append(("PASS " if c else "FAIL ") + m); c or fails.append(m)
pages = sorted(D.glob("*.html"))
texts = {f: f.read_text() for f in D.rglob("*") if f.suffix in (".html", ".css", ".js", ".svg", ".json", ".txt", ".xml")}
alltext = "\n".join(texts.values()); low = alltext.lower()
ok(not re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", alltext, re.I), "no e-mail address anywhere in dist")
for w in ["mailto", "hotmail", "gmail", "aggregaterating", "openinghoursspecification", "higgsfield"]:
    ok(w not in low, f"no '{w}' anywhere")
vis = H.unescape(" ".join(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|head)\b.*?</\1>", " ", texts[f], flags=re.S)) for f in texts if f.suffix == ".html"))
for pat, why in [(r"\$\s?\d|\d+\.\d\d\b(?! on Google)", "prices"), (r"github\.io", "github.io in visible copy"), (r"since (19|20)\d\d|award|voted|#1 ", "years/awards"),
                 (r"\bchef\b|\bowner\b|family[- ]owned", "staff/owner claims"), (r"\bstock (image|photo)", "'stock' wording"), (r"open (now|today|daily|7 days)", "invented hours"), (r"\bhalal\b|\bfree\b", "invented claims")]:
    ok(not re.search(pat, vis, re.I), f"no {why} in visible text")
ok(all(TEL in p.read_text() for p in pages), "tap-to-call on every page")
idx = H.unescape((D / "index.html").read_text())
ok("4.0 on Google from 416 reviews" in re.sub(r"<[^>]+>", "", idx), "rating as visible text on Home")
ok("Reviews to confirm" in vis or "reviews to confirm" in vis, "'Reviews to confirm' placeholder")
ok(all(re.search(r"google\.com/maps/search/\?api=1&(amp;)?query=Chicken\+N\+Tings", (D / f).read_text()) for f in ["index.html", "reviews.html", "visit.html"]), "Leave us a Google review -> Maps search (Home, Reviews, Visit)")
ok("Leave us a Google review" in idx, "review button label")
for k in ["Malton", "Brandon Gate", "Mississauga"]:
    ok(k in idx, f"local copy mentions {k}")
menu = H.unescape((D / "menu.html").read_text())
ok("Sample menu, prices to confirm" in menu, "menu labelled 'Sample menu, prices to confirm'")
n_items = menu.count('class="menu-item"')
ok(n_items >= 8 and menu.count('<mark class="ph-inline">To confirm</mark>') == n_items, f"every menu price shown as 'To confirm' ({n_items})")
for d in ["Jerk chicken", "Oxtail", "Curry goat", "Rice and peas", "patty", "Festival"]:
    ok(d.lower() in menu.lower(), f"menu has {d}")
od = (D / "order-catering.html").read_text()
ok("<fieldset disabled>" in od and "This form is disabled in this demo" in od, "order form disabled with note")
for fid in ["o-name", "o-phone", "o-date", "o-people", "o-msg"]:
    ok(f'<label for="{fid}"' in od, f"order form field {fid} labelled")
ok('value="pickup"' in od and 'value="catering"' in od, "pickup or catering choice")
vi = (D / "visit.html").read_text()
ok(re.search(r'<iframe src="https://maps\.google\.com/maps\?q=[^"]+output=embed" title="[^"]+" loading="lazy"', vi) is not None, "keyless map embed, titled, lazy")
ok("google.com/maps/dir/?api=1&amp;destination=" in vi, "directions link")
ok("data-status" not in alltext and "open now" not in low, "no live open/closed badge")
ok("Opening hours to confirm" in vis or "opening hours" in vis.lower(), "hours To-confirm placeholder")
ok((D / ".nojekyll").exists(), ".nojekyll present")
for f in pages:
    s = f.read_text(); u = H.unescape(s); n = f.name
    ok('<meta name="robots" content="noindex, nofollow">' in s, f"{n}: noindex")
    ok(BANNER in u and s.index('class="demo-banner"') < s.index('class="skip-link"'), f"{n}: demo banner")
    ok(FOOTER in u, f"{n}: footer disclaimer")
    for k in ("og:title", "twitter:title", "og:site_name"):
        m = re.search(rf'(?:property|name)="{k}" content="([^"]+)"', s)
        ok(m and "(demo concept)" in m.group(1), f"{n}: {k} has '(demo concept)'")
    ok("(demo concept)" in re.search(r"<title>(.*?)</title>", s).group(1), f"{n}: <title> has '(demo concept)'")
    refs = re.findall(r'(?:href|src|poster)="([^"]+)"', s) + [u2.split()[0] for ss in re.findall(r'srcset="([^"]+)"', s) for u2 in ss.split(",")]
    bad = [r for r in refs if r.startswith("/") or (not re.match(r"^(https?:|tel:|#)", r) and not (D / r.split("#")[0].split("?")[0]).exists())]
    ok(not bad, f"{n}: all refs relative and resolvable {bad[:3]}")
    for img in re.findall(r"<img\b[^>]*>", s):
        ok(re.search(r'\swidth="\d+"', img) and re.search(r'\sheight="\d+"', img), f"{n}: img has width/height")
    photos = [i for i in re.findall(r'<img\b[^>]*src="img/([^"]+)"', s) if not i.startswith("logo")]
    medias = re.findall(r'<div class="media[^"]*"[^>]*>(.*?)</div>', s, re.S)
    ok(len(photos) == len(medias) and all(BADGE in H.unescape(m) for m in medias), f"{n}: every photo badged ({len(photos)})")
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        d = json.loads(ld)
        ok(d["@type"] == ["Restaurant"] and set(d) <= {"@context", "@type", "name", "address", "telephone", "image", "servesCuisine", "sameAs", "hasMap"} and d["image"].endswith("img/logo.png") and d["address"]["streetAddress"] == "4025 Brandon Gate Dr", f"{n}: JSON-LD keys {sorted(d)}")
big = [(f.name, f.stat().st_size) for f in D.rglob("*") if f.suffix in (".webp", ".jpg", ".png") and f.stat().st_size >= 150_000]
ok(not big, f"all images under 150 KB {big}")
print("\n".join(lines)); print(f"\n{len(lines) - len(fails)} passed, {len(fails)} failed")
