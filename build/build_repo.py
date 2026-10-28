"""Build the loop-site repo for one environment.

  python3 _funnel_build/build_repo.py staging   -> loop-site/staging/  (banner, noindex)
  python3 _funnel_build/build_repo.py prod      -> loop-site/          (live site)
  python3 _funnel_build/build_repo.py promote   -> copy loop-site/staging/ over the live site

Sources: _funnel_build/build_site.py (six site pages), the three project-root funnel
pages, Loop_MCU_Analyzer_Oct2026.html, and _site/img/.
"""
import os, sys, shutil, subprocess, re

B = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(B); REPO = os.path.join(PROJ, "loop-site")
PAGES = ["index.html", "personal.html", "perusahaan.html", "asuransi.html", "membership.html", "konsultasi.html"]
FUNNELS = [("Loop_Cek_MCU_Funnel.html", "cek-mcu.html"), ("Loop_Bisnis_MCU_Funnel.html", "bisnis-mcu.html"), ("Loop_Asuransi_MCU_Funnel.html", "asuransi-mcu.html")]
LINKS = {"https://claude.ai/artifact/BiNbJRigeW9wxaFn868gxr/": "", "https://claude.ai/artifact/BiNbJRigeW9wxaFn868gxr": "./",
         "https://claude.ai/artifact/GMJzuH59Gv79aCw3kMP15J": "cek-mcu.html", "https://claude.ai/artifact/GBqfAzzt5GfEVJ9bWPYVws": "bisnis-mcu.html",
         "https://claude.ai/artifact/52LhmaY3Z9J8yU6hdAU3A3": "asuransi-mcu.html"}
HEAD = '<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
BANNER = ('<div style="position:sticky;top:0;z-index:9999;background:#7c3aed;color:#fff;font:600 13px/1.4 system-ui,sans-serif;'
          'text-align:center;padding:7px 12px">STAGING · belum live · '
          '<a href="https://stevetsurface.github.io/loop-site/" style="color:#fff;text-decoration:underline">lihat situs live →</a></div>')

def wrap(src, dst, prefix=""):
    s = open(os.path.join(PROJ, src)).read()
    for k, v in LINKS.items(): s = s.replace(k, prefix + v)
    i = s.find("</style>"); j = s.find(">", i) + 1
    open(dst, "w").write(HEAD + s[:j] + "</head><body>" + s[j:].rstrip() + "\n</body></html>\n")

def mark_staging(path):
    s = open(path).read()
    if 'name="robots"' not in s:
        s = s.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
    if "STAGING · belum live" not in s:
        s = re.sub(r"<body([^>]*)>", lambda m: "<body" + m.group(1) + ">" + BANNER, s, count=1)
    open(path, "w").write(s)

def build(out, staging):
    os.makedirs(os.path.join(out, "analyzer"), exist_ok=True)
    env = dict(os.environ, SITE_OUT=out, SITE_LOCAL="1")
    subprocess.run([sys.executable, os.path.join(B, "build_site.py")], env=env, check=True, stdout=subprocess.DEVNULL)
    for src, dst in FUNNELS: wrap(src, os.path.join(out, dst))
    wrap("Loop_MCU_Analyzer_Oct2026.html", os.path.join(out, "analyzer", "index.html"), "../")
    shutil.copytree(os.path.join(PROJ, "_site", "img"), os.path.join(out, "img"), dirs_exist_ok=True)
    if staging:
        for root, _, files in os.walk(out):
            for f in files:
                if f.endswith(".html"): mark_staging(os.path.join(root, f))
    print("built", "staging" if staging else "prod", "->", os.path.relpath(out, PROJ))

def promote():
    st = os.path.join(REPO, "staging")
    for root, _, files in os.walk(st):
        rel = os.path.relpath(root, st)
        for f in files:
            d = os.path.join(REPO, rel); os.makedirs(d, exist_ok=True)
            s = os.path.join(root, f); t = os.path.join(d, f)
            if f.endswith(".html"):
                h = open(s).read().replace('<meta name="robots" content="noindex,nofollow">', "").replace(BANNER, "")
                open(t, "w").write(h)
            else:
                shutil.copy2(s, t)
    print("promoted staging -> live")

if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["staging"])[0]
    if cmd == "staging": build(os.path.join(REPO, "staging"), True)
    elif cmd == "prod": build(REPO, False)
    elif cmd == "promote": promote()
    else: sys.exit(__doc__)
