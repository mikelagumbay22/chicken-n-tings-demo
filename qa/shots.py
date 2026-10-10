"""Lean viewport screenshots (JPG, under 1 MB): Home desktop + mobile."""
import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image
CHROME = "/usr/bin/google-chrome"
BASE = sys.argv[1]; OUT = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    for name, vp, dpr in [("home-desktop", {"width": 1440, "height": 900}, 1), ("home-mobile", {"width": 390, "height": 844}, 2)]:
        pg = b.new_page(viewport=vp, device_scale_factor=dpr, is_mobile=dpr > 1)
        pg.add_init_script("window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})")
        pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(2600)
        pg.screenshot(path="/tmp/_s.png"); im = Image.open("/tmp/_s.png").convert("RGB"); q = 84
        while True:
            im.save(f"{OUT}/{name}.jpg", quality=q, optimize=True)
            if os.path.getsize(f"{OUT}/{name}.jpg") < 1_000_000 or q < 50: break
            q -= 8
        print(f"{OUT}/{name}.jpg", os.path.getsize(f"{OUT}/{name}.jpg") // 1024, "KB  CLS", round(pg.evaluate("window.__cls"), 4))
    b.close()
