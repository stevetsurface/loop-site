import os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_site.py")
s = open(P).read()
def rep(old, new, count=1):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, count)

# 1. CSS for real images
rep(".photo .note{position:absolute;top:16px;right:16px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.8);background:rgba(0,0,0,.25);padding:4px 10px;border-radius:999px}",
    ".photo .note{position:absolute;top:16px;right:16px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.8);background:rgba(0,0,0,.25);padding:4px 10px;border-radius:999px}\n"
    ".photo.img{padding:0;min-height:0;background:var(--teal-soft);display:block;aspect-ratio:5/4}.photo.img::before{display:none}.photo.img img{width:100%;height:100%;object-fit:cover;display:block}\n"
    ".photo.img.contain{background:#fff;border:1px solid var(--line);aspect-ratio:auto;padding:28px}.photo.img.contain img{object-fit:contain;max-height:460px}\n"
    ".photo .float{position:absolute;left:18px;bottom:18px;background:#fff;color:var(--ink);border-radius:18px;padding:14px 16px;box-shadow:0 14px 40px rgba(15,42,58,.22);max-width:300px}.photo .float b{display:block;font-size:22px;letter-spacing:-.02em}.photo .float b small{font-size:12px;font-weight:600;color:var(--muted);margin-left:6px}.photo .float span{font-size:13px;color:var(--body)}\n"
    ".step.pic{display:grid;grid-template-columns:116px 1fr;gap:18px;align-items:center}.step.pic img{width:116px;height:96px;object-fit:cover;border-radius:16px;background:var(--mint);grid-row:1/3}.step.pic .n{margin-bottom:8px}@media (max-width:560px){.step.pic{grid-template-columns:1fr}.step.pic img{width:100%;height:150px;grid-row:auto}}\n"
    ".quote .av{width:56px;height:56px;border-radius:50%;object-fit:cover;display:block;margin-bottom:14px;border:3px solid rgba(255,255,255,.18);background:#fff}.quote .av.logo{border-radius:14px;object-fit:contain;padding:8px;width:96px;height:56px}\n"
    ".logos img{height:36px;width:auto;max-width:150px;opacity:.75;filter:grayscale(1) contrast(1.05);transition:.2s}.logos img:hover{opacity:1;filter:none}.logos{align-items:center;gap:18px 36px}\n"
    ".stores{display:flex;gap:12px;margin-top:18px}.stores img{height:42px}")

# 2. helpers
rep('def photo(tagkey, notekey="photo.note"):\n    return f\'<div class="photo" aria-hidden="true"><span class="note" data-i18n="{notekey}"></span><div class="tag" data-i18n="{tagkey}"></div></div>\'',
    'def photo(tagkey, notekey="photo.note"):\n    return f\'<div class="photo" aria-hidden="true"><span class="note" data-i18n="{notekey}"></span><div class="tag" data-i18n="{tagkey}"></div></div>\'\n'
    'def pic(src, alt="", cls="", inner=""):\n    return f\'<div class="photo img {cls}"><img src="img/{src}" alt="{alt}" loading="lazy">{inner}</div>\'\n'
    'def av(src, alt="", logo=False):\n    return f\'<img class="av{" logo" if logo else ""}" src="img/{src}" alt="{alt}" loading="lazy">\'\n'
    'LOGOS = [("mqare.svg","mQare"),("sinocare.svg","Sinocare"),("equira.png","Equira Life"),("rumat.svg","Rumat"),("lontar.svg","Lontar Papyrus"),("ikpp.svg","Indah Kiat Pulp & Paper"),("fwd.svg","FWD"),("marsh.svg","Marsh"),("prodia.svg","Prodia"),("sampoerna.svg","Sampoerna"),("suzuki.svg","Suzuki"),("roche.svg","Roche"),("sehatq.svg","SehatQ"),("ugm.svg","UGM")]\n'
    'def logos_row():\n    return \'<div class="logos"><span class="k" data-i18n="a.logos"></span>\' + "".join(f\'<img src="img/{f}" alt="{n}" title="{n}" loading="lazy">\' for f,n in LOGOS) + \'</div>\'')

# 3. home hero: Sadimin photo with floating result badge (preview card moves to personal page only)
rep("<div class=\"trust\"><div><b data-i18n=\"h.t1b\"></b><span data-i18n=\"h.t1s\"></span></div><div><b data-i18n=\"h.t2b\"></b><span data-i18n=\"h.t2s\"></span></div><div><b data-i18n=\"h.t3b\"></b><span data-i18n=\"h.t3s\"></span></div></div></div>\n{preview_card()}</div></section>",
    "<div class=\"trust\"><div><b data-i18n=\"h.t1b\"></b><span data-i18n=\"h.t1s\"></span></div><div><b data-i18n=\"h.t2b\"></b><span data-i18n=\"h.t2s\"></span></div><div><b data-i18n=\"h.t3b\"></b><span data-i18n=\"h.t3s\"></span></div></div></div>\n{pic('hero-sadimin.png','Sadimin, member Loop', inner='<div class=\"float\"><b>9% → 6,4% <small>HbA1c</small></b><span>Sadimin · <span data-i18n=\"h.photo\"></span></span></div>')}</div></section>")

# 4. logos
rep('<div class="logos"><span class="k" data-i18n="a.logos"></span><span>mQare</span><span>Sinocare</span><span>Equiralife</span><span>Rumat</span><span>Lontar Papyrus</span><span>Indah Kiat</span></div></section>',
    '{logos_row()}</section>')

# 5. home how-it-works pictures
rep('<div class="grid3" style="grid-template-columns:1fr"><div class="card step"><div class="n">1</div><h3 data-i18n="w.1h"></h3><p data-i18n="w.1p"></p></div><div class="card step"><div class="n">2</div><h3 data-i18n="w.2h"></h3><p data-i18n="w.2p"></p></div><div class="card step"><div class="n">3</div><h3 data-i18n="w.3h"></h3><p data-i18n="w.3p"></p></div></div>',
    '<div class="grid3" style="grid-template-columns:1fr"><div class="card step pic"><img src="img/app.png" alt="" loading="lazy"><div class="n">1</div><div><h3 data-i18n="w.1h"></h3><p data-i18n="w.1p"></p></div></div><div class="card step pic"><img src="img/chat.png" alt="" loading="lazy"><div class="n">2</div><div><h3 data-i18n="w.2h"></h3><p data-i18n="w.2p"></p></div></div><div class="card step pic"><img src="img/loop-kit.png" alt="" loading="lazy"><div class="n">3</div><div><h3 data-i18n="w.3h"></h3><p data-i18n="w.3p"></p></div></div></div>')

# 6. home quotes avatars
rep('<div class="card quote"><span class="badge" data-i18n="r.1b"></span>', '<div class="card quote">{av("hero-sadimin.png","Sadimin")}<span class="badge" data-i18n="r.1b"></span>')
rep('<div class="card quote"><span class="badge" data-i18n="r.2b"></span>', '<div class="card quote">{av("member-hendry.png","Hendry")}<span class="badge" data-i18n="r.2b"></span>')
rep('<div class="card quote"><span class="badge" data-i18n="r.3b"></span>', '<div class="card quote">{av("member-lenny.png","Lenny Kristiani")}<span class="badge" data-i18n="r.3b"></span>')

# 7. audience pages: hero + quote avatars per page
rep('{preview_card() if key=="per" else photo(key+".photo")}</div></section>',
    '{preview_card() if key=="per" else pic(HERO_PIC[key][0], HERO_PIC[key][1], HERO_PIC[key][2])}</div></section>')
rep('def audience(filename, active, key, funnel, title):',
    'HERO_PIC = {"cor": ("loop-kit.png","Loop Kit untuk karyawan","contain"), "ins": ("mockup.png","Aplikasi Loop: data gula darah member","contain")}\n'
    'QUOTE_AV = {"per": [("member-lilis.png","Lilis Suryani",False),("member-zulkarnain.png","Zulkarnain",False),("member-lenny.png","Lenny Kristiani",False)],\n'
    '            "cor": [("lontar.svg","Lontar Papyrus",True),("ikpp.svg","Indah Kiat",True),("mqare.svg","mQare",True)], "ins": [None,None,None]}\n'
    'def audience(filename, active, key, funnel, title):')
for i in (1,2,3):
    rep(f'<div class="card quote"><span class="badge" data-i18n="{{key}}.q.{i}b"></span>',
        f'<div class="card quote">{{av(*QUOTE_AV[key][{i-1}]) if QUOTE_AV[key][{i-1}] else ""}}<span class="badge" data-i18n="{{key}}.q.{i}b"></span>')

# 8. membership page: app mockup + store badges instead of a second price card
rep('<div class="mcard"><div><div class="brand">loop</div><div class="l" data-i18n="m.l"></div></div><div><div class="p" data-i18n="m.p"></div><div class="l" data-i18n="m.s"></div></div></div></div></section>\n<div class="wrap">',
    '<div>{pic("mockup.png","Aplikasi Loop","contain")}<div class="stores"><a href="https://apps.apple.com/id/app/loop-health/id6474244184" target="_blank" rel="noopener"><img src="img/appstore.svg" alt="App Store"></a><a href="https://play.google.com/store/apps/details?id=id.loophealth.app" target="_blank" rel="noopener"><img src="img/googleplay.svg" alt="Google Play"></a></div></div></div></section>\n<div class="wrap">')
rep('<div class="card quote"><span class="badge" data-i18n="mb.q.1b"></span>', '<div class="card quote">{av("member-sugianto.png","Sugianto")}<span class="badge" data-i18n="mb.q.1b"></span>')
rep('<div class="card quote"><span class="badge" data-i18n="mb.q.3b"></span>', '<div class="card quote">{av("member-lilis.png","Lilis Suryani")}<span class="badge" data-i18n="mb.q.3b"></span>')

# 9. i18n for the hero float
rep('"photo.note":"Foto: ganti dengan member Loop",', '"photo.note":"Foto: ganti dengan member Loop","h.photo":"member Loop, 37 tahun",')
rep('"photo.note":"Photo: replace with a Loop member",', '"photo.note":"Photo: replace with a Loop member","h.photo":"Loop member, age 37",')

open(P,"w").write(s)
print("patched")
