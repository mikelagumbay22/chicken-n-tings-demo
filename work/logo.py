"""Demo wordmark for Chicken "N" Tings (concept for this demo only, not their logo). Text as outlines (Fraunces, SIL OFL)."""
import sys, io
sys.path.insert(0, '/workspace/sites/chicken-n-tings/work')
from textpath import path
import cairosvg
from PIL import Image
OUT = '/workspace/sites/chicken-n-tings/assets/'
GOLD, EMBER, RED, INK, CREAM, LEAF = '#F6B93B', '#F0714B', '#B8321A', '#17110D', '#FBF3E6', '#3E8E5A'
def f(v): return ('%.2f' % v).rstrip('0').rstrip('.')
FLAME = 'M24 4c3 8-6 11-6 19a8 8 0 0 0 16 0c0-4-2-6-3-9 4 2 9 7 9 14a16 16 0 0 1-32 0C8 18 20 13 24 4z'
def mark(x, y, s):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})"><path fill="{EMBER}" d="{FLAME}"/>'
            f'<path fill="{GOLD}" d="M24 22c2 4-2 6-2 9a4 4 0 0 0 8 0c0-3-2-5-6-9z"/>'
            f'<path d="M6 48h36" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/><path d="M10 54h28" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" opacity=".7"/></g>')
def word(fg):
    d1, a1, _ = path('fraunces-700.ttf', 'Chicken \u201cN\u201d Tings', 30, 58, 32, 0)
    d2, a2, _ = path('mulish-700-latin.ttf', 'JAMAICAN RESTAURANT \u00b7 MALTON', 8.6, 59, 48, 0.18)
    w = 58 + max(a1, a2) + 4
    return w, 56, mark(2, 0, 1) + f'<path fill="{fg}" d="{d1}"/><path fill="{GOLD}" d="{d2}"/>'
def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {h}" width="{w:.0f}" height="{h}" role="img" aria-labelledby="t">'
            f'<title id="t">Chicken N Tings</title><!-- Demo concept wordmark, not the business logo. -->{body}</svg>\n')
w, h, body = word(CREAM)
open(OUT + 'logo.svg', 'w').write(svg(w, h, body))
png = cairosvg.svg2png(bytestring=svg(w, h, f'<rect width="{f(w)}" height="{h}" fill="{INK}"/>' + body).encode(), output_width=round(w * 4))
Image.open(io.BytesIO(png)).convert('RGB').save(OUT + 'logo.png', optimize=True)
def icon(size):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><rect width="64" height="64" rx="14" fill="{INK}"/>{mark(8, 2, 1)}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=size, output_height=size)))
icon(512).save(OUT + 'favicon-512.png', optimize=True); icon(180).convert('RGB').save(OUT + 'apple-touch-icon.png', optimize=True)
icon(64).save(OUT + 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
cairosvg.svg2png(bytestring=open(OUT + 'logo.svg').read().encode(), write_to='/tmp/cnt_logo.png', output_width=700, background_color=INK)
print(w)
