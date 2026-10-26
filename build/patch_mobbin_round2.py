import os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_site.py")
s = open(P).read()
def rep(old, new, count=1):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new, count)

# ---- 1. fonts: Fraunces display serif next to Plus Jakarta Sans
rep('family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap',
    'family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fraunces:ital,opsz,wght@0,9..144,500..700;1,9..144,400..600&display=swap')

# ---- 2. italic accent phrases in headlines (data-i18n sets innerHTML)
ACCENT = {"h.h1": ["dokter dan coach yang sama", "the same doctor and coach"],
          "a.h": ["Satu mesin yang sama", "One engine"],
          "w.h": ["Tiga langkah", "Three steps"],
          "p.h": ["satu tim", "one team"],
          "r.h": ["sebelum dan sesudah", "before and after"],
          "s.h": ["merawat diri", "self-care"],
          "per.h1": ["Pahami", "Understand"],
          "mb.i.h": ["membantu Anda", "helps you"],
          "mb.c.h": ["satu membership", "one membership"]}
for key, phrases in ACCENT.items():
    for ph in phrases:
        pat = re.compile(r'("%s":")([^"]*?)(%s)([^"]*")' % (re.escape(key), re.escape(ph)))
        s, n = pat.subn(lambda m: m.group(1)+m.group(2)+"<em>"+m.group(3)+"</em>"+m.group(4), s, count=1)
        print(key, ph, "->", n)

# ---- 3. CSS
rep("h1{font-size:clamp(36px,5.4vw,58px);line-height:1.08;font-weight:800;color:var(--ink);letter-spacing:-.025em;margin:0 0 20px;text-wrap:balance}",
    "h1{font-family:'Fraunces',Georgia,serif;font-variation-settings:\"opsz\" 144,\"SOFT\" 40;font-size:clamp(40px,6vw,66px);line-height:1.04;font-weight:600;color:var(--ink);letter-spacing:-.02em;margin:0 0 22px;text-wrap:balance}\nh1 em,h2 em{font-style:italic;font-weight:500;color:var(--teal-deep)}")
rep("h2{font-size:clamp(28px,4vw,40px);line-height:1.12;font-weight:800;color:var(--ink);letter-spacing:-.02em;margin:0 0 12px;text-wrap:balance}",
    "h2{font-family:'Fraunces',Georgia,serif;font-variation-settings:\"opsz\" 144,\"SOFT\" 40;font-size:clamp(30px,4.4vw,46px);line-height:1.1;font-weight:600;color:var(--ink);letter-spacing:-.015em;margin:0 0 12px;text-wrap:balance}")
rep(".hero{background:var(--mint);padding-block:72px 64px}", ".hero{background:var(--sand);padding-block:64px 72px}")
rep(".trust{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:40px;padding-top:24px;border-top:1px solid rgba(15,42,58,.12)}",
    ".trust{display:flex;flex-wrap:wrap;gap:12px 0;margin-top:40px}.trust>div{padding:2px 24px;border-left:1px solid rgba(15,42,58,.18)}.trust>div:first-child{padding-left:0;border-left:0}")
rep("@media (max-width:560px){.trust{grid-template-columns:1fr;gap:10px}}",
    "@media (max-width:560px){.trust{flex-direction:column}.trust>div{padding:10px 0 0;border-left:0;border-top:1px solid rgba(15,42,58,.12)}.trust>div:first-child{border-top:0;padding-top:0}}")
rep(".nav{height:84px;display:flex;align-items:center;justify-content:space-between;gap:16px}",
    ".navwrap{position:sticky;top:10px;z-index:50;padding-top:10px}.nav{height:64px;display:flex;align-items:center;justify-content:space-between;gap:16px;background:rgba(255,255,255,.86);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid var(--line);border-radius:999px;padding:0 10px 0 22px;box-shadow:0 10px 32px rgba(15,42,58,.08)}")
rep(".quote .av{width:56px;height:56px;border-radius:50%;object-fit:cover;display:block;margin-bottom:14px;border:3px solid rgba(255,255,255,.18);background:#fff}.quote .av.logo{border-radius:14px;object-fit:contain;padding:8px;width:96px;height:56px}",
    ".quote .av{width:100%;height:auto;aspect-ratio:4/3;border-radius:16px;object-fit:cover;display:block;margin-bottom:16px;background:#fff}.quote .av.logo{aspect-ratio:auto;border-radius:14px;object-fit:contain;padding:8px;width:110px;height:60px;background:#fff}")
rep("@media (prefers-reduced-motion:reduce)", r"""
/* Loop 2.1 · Mobbin round 2 (Function / Superpower / Hims patterns) */
.how{position:relative;padding:28px 24px 24px;background:var(--sand);border-color:transparent}.how .num{font-family:'Fraunces',Georgia,serif;font-size:15px;font-weight:600;color:var(--teal-deep);letter-spacing:.06em;margin-bottom:10px}.how h3{font-size:21px;color:var(--ink)}.how p{font-size:15px;margin:0 0 18px;min-height:3.2em}
.mini{background:#fff;border:1px solid var(--line);border-radius:18px;padding:14px;min-height:150px}
.drop{border:1.5px dashed var(--teal);border-radius:14px;padding:12px;background:var(--teal-soft)}.fchip{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 10px;font-size:12px;font-weight:700;color:var(--ink2);margin:0 6px 8px 0}.bar{height:6px;border-radius:3px;background:#fff;overflow:hidden;margin-top:4px}.bar i{display:block;height:100%;background:var(--teal);border-radius:3px}
.mini .mk{margin-bottom:8px}.mini .mk:last-child{margin-bottom:0}
.plan .row{display:flex;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line)}.plan .row:last-child{border-bottom:0}.plan .row i{font-style:normal;width:36px;height:36px;border-radius:12px;background:var(--amber-soft);display:grid;place-items:center;font-size:16px;flex:0 0 36px}.plan .row b{display:block;font-size:14px;color:var(--ink)}.plan .row span{font-size:12px;color:var(--muted)}
.bento{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:260px 260px;gap:16px;margin-top:36px}.bento .b{position:relative;border-radius:24px;overflow:hidden;background:var(--mint);margin:0}.bento .b img{width:100%;height:100%;object-fit:cover;display:block}.bento .b.contain img{object-fit:contain;padding:22px}.bento .b figcaption{position:absolute;left:0;right:0;bottom:0;padding:16px 18px;background:linear-gradient(transparent,rgba(15,42,58,.78));color:#fff}.bento .b.contain figcaption{background:linear-gradient(transparent,rgba(242,249,248,.95));color:var(--ink)}.bento .b figcaption b{display:block;font-size:17px;font-weight:800}.bento .b figcaption span{font-size:13px;opacity:.9}
.bento .b.navy{background:var(--navy);color:#fff;padding:26px;grid-column:3;grid-row:1/3}.bento .b.navy h3{color:#fff;font-size:22px;margin-bottom:10px}.bento .b.navy .feats li{color:#fff;font-size:15px}.bento .b.navy .feats li::before{color:var(--teal)}
@media (max-width:860px){.bento{grid-template-columns:1fr 1fr;grid-template-rows:200px 200px auto}.bento .b.navy{grid-column:1/3;grid-row:3}}@media (max-width:560px){.bento{grid-template-columns:1fr;grid-template-rows:auto}.bento .b{height:220px}.bento .b.navy{grid-column:1;grid-row:auto;height:auto}}
.pcard{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:0;background:#fff;border:1px solid var(--line);border-radius:28px;box-shadow:0 24px 60px rgba(15,42,58,.10);text-align:left;margin:36px auto 0;max-width:960px;overflow:hidden}.pcard .pl{padding:34px 36px;border-right:1px solid var(--line)}.pcard .pname{font-family:'Fraunces',Georgia,serif;font-size:30px;color:var(--ink);font-weight:600;margin:4px 0 18px}.pcard .price{font-size:44px;font-weight:800;color:var(--ink);line-height:1;letter-spacing:-.02em}.pcard .price small{font-size:15px;font-weight:600;color:var(--muted);margin-left:6px}.pcard .l{font-size:13px;color:var(--muted);margin:8px 0 22px}.pcard .feats{padding:30px 36px;margin:0}.pcard .feats li{padding:9px 0;border-bottom:1px solid var(--line)}.pcard .feats li:last-child{border-bottom:0}
@media (max-width:760px){.pcard{grid-template-columns:1fr}.pcard .pl{border-right:0;border-bottom:1px solid var(--line)}}
footer{border-top:0;background:transparent;padding-block:0 32px}footer .wrap{background:var(--sand);border:1px solid var(--line);border-radius:28px;padding:40px 36px 28px;grid-template-columns:1.4fr repeat(auto-fit,minmax(180px,1fr))}footer .fbrand img{width:84px;height:39px;display:block;margin-bottom:12px}footer .fbrand p{margin:0 0 14px;font-size:14px;max-width:34ch}footer .fbrand .stores{margin-top:0}footer .fbrand .stores img{height:38px}@media (max-width:760px){footer .wrap{grid-template-columns:1fr;padding:28px 22px}}
@media (prefers-reduced-motion:reduce)""")

# ---- 4. header: floating pill nav
rep('<div class="wrap"><nav class="nav"><a href="./" aria-label="Loop Health">', '<div class="wrap navwrap"><nav class="nav"><a href="./" aria-label="Loop Health">')

# ---- 5. footer: brand column with app badges
rep("""<footer class="bleed"><div class="wrap">
<div><b data-i18n="ft.sol"></b>""", """<footer class="bleed"><div class="wrap">
<div class="fbrand"><img alt="Loop Health" src="{LOGO}"><p data-i18n="ft.tag"></p><div class="stores"><a href="https://apps.apple.com/id/app/loop-diabetes-virtual-care/id6445804498" target="_blank" rel="noopener"><img src="img/appstore.svg" alt="App Store"></a><a href="https://play.google.com/store/apps/details?id=com.id.loophealth" target="_blank" rel="noopener"><img src="img/googleplay.svg" alt="Google Play"></a></div></div>
<div><b data-i18n="ft.sol"></b>""")
rep('"photo.note":"Foto: ganti dengan member Loop","h.photo":"member Loop, 37 tahun",', '"photo.note":"Foto: ganti dengan member Loop","h.photo":"member Loop, 37 tahun","ft.tag":"Klinik dan coach untuk diabetes, hipertensi, dan kolesterol. Satu dokter, satu coach, setiap hari.",')
rep('"photo.note":"Photo: replace with a Loop member","h.photo":"Loop member, age 37",', '"photo.note":"Photo: replace with a Loop member","h.photo":"Loop member, age 37","ft.tag":"Clinic and coaching for diabetes, hypertension and cholesterol. One doctor, one coach, every day.",')

# ---- 6. home: how-it-works → Function-style cards with mini UI
rep('''<section class="sec"><div class="split"><div><span class="eyebrow" data-i18n="w.eye"></span><h2 data-i18n="w.h"></h2><p class="lead" data-i18n="w.p"></p></div>
<div class="grid3" style="grid-template-columns:1fr"><div class="card step pic"><img src="img/app.png" alt="" loading="lazy"><div class="n">1</div><div><h3 data-i18n="w.1h"></h3><p data-i18n="w.1p"></p></div></div><div class="card step pic"><img src="img/chat.png" alt="" loading="lazy"><div class="n">2</div><div><h3 data-i18n="w.2h"></h3><p data-i18n="w.2p"></p></div></div><div class="card step pic"><img src="img/loop-kit.png" alt="" loading="lazy"><div class="n">3</div><div><h3 data-i18n="w.3h"></h3><p data-i18n="w.3p"></p></div></div></div></div></section>''',
'''<section class="sec center"><span class="eyebrow" data-i18n="w.eye"></span><h2 data-i18n="w.h"></h2><p class="lead" data-i18n="w.p"></p>
<div class="grid3" style="text-align:left;margin-top:36px">
<div class="card how"><div class="num">01</div><h3 data-i18n="w.1h"></h3><p data-i18n="w.1p"></p><div class="mini"><div class="drop"><span class="fchip">📄 Prodia_MCU_2026.pdf</span><span class="fchip">🖼 <span data-i18n="how.photo"></span></span><div class="bar"><i style="width:72%"></i></div></div><div style="font-size:12px;color:var(--muted);margin-top:10px" data-i18n="how.reading"></div></div></div>
<div class="card how"><div class="num">02</div><h3 data-i18n="w.2h"></h3><p data-i18n="w.2p"></p><div class="mini"><div class="mk"><div class="l">HbA1c</div><div class="v">7,8% <span class="chip bad" data-i18n="pv.c1"></span></div><div class="rb"><div class="rbt"><i style="flex:0 0 21%;background:#2a9d6f"></i><i style="flex:0 0 10%;background:#d99a00"></i><i style="flex:0 0 38%;background:#e07a1f"></i><i style="flex:0 0 31%;background:#d9534f"></i></div><b style="left:47%"></b></div></div><div class="mk"><div class="l" data-i18n="pv.bp"></div><div class="v">152/96 <span class="chip bad" data-i18n="pv.c2"></span></div><div class="rb"><div class="rbt"><i style="flex:0 0 27%;background:#2a9d6f"></i><i style="flex:0 0 18%;background:#d99a00"></i><i style="flex:0 0 18%;background:#e07a1f"></i><i style="flex:0 0 37%;background:#d9534f"></i></div><b style="left:56%"></b></div></div></div></div>
<div class="card how"><div class="num">03</div><h3 data-i18n="w.3h"></h3><p data-i18n="w.3p"></p><div class="mini plan"><div class="row"><i>💊</i><div><b data-i18n="how.p1"></b><span data-i18n="how.p1s"></span></div></div><div class="row"><i>🥗</i><div><b data-i18n="how.p2"></b><span data-i18n="how.p2s"></span></div></div><div class="row"><i>🩺</i><div><b data-i18n="how.p3"></b><span data-i18n="how.p3s"></span></div></div></div></div>
</div><div class="cta" style="justify-content:center;margin-top:32px"><a class="btn primary" href="{FUNNEL['personal']}" data-i18n="h.cta1"></a><a class="btn ghost" href="konsultasi.html" data-i18n="m.cta2"></a></div></section>''')

# ---- 7. home: checklist → bento "what you get"
rep('''<div class="wrap"><section class="sec center"><h2 data-i18n="s.h"></h2><ul class="list2" style="text-align:left"><li data-i18n="s.1"></li><li data-i18n="s.2"></li><li data-i18n="s.3"></li><li data-i18n="s.4"></li><li data-i18n="s.5"></li></ul></section></div>''',
'''<div class="wrap"><section class="sec center"><span class="eyebrow" data-i18n="b.eye"></span><h2 data-i18n="s.h"></h2><p class="lead" data-i18n="b.p"></p>
<div class="bento" style="text-align:left"><figure class="b contain"><img src="img/loop-kit.png" alt="Loop Kit" loading="lazy"><figcaption><b data-i18n="b.1h"></b><span data-i18n="b.1p"></span></figcaption></figure><figure class="b contain"><img src="img/chat.png" alt="" loading="lazy"><figcaption><b data-i18n="b.2h"></b><span data-i18n="b.2p"></span></figcaption></figure>
<div class="b navy"><h3 data-i18n="b.4h"></h3><ul class="feats"><li data-i18n="s.1"></li><li data-i18n="s.2"></li><li data-i18n="s.3"></li><li data-i18n="s.4"></li><li data-i18n="s.5"></li></ul></div>
<figure class="b contain"><img src="img/app.png" alt="" loading="lazy"><figcaption><b data-i18n="b.3h"></b><span data-i18n="b.3p"></span></figcaption></figure><figure class="b"><img src="img/member-intan.png" alt="" loading="lazy"><figcaption><b data-i18n="b.5h"></b><span data-i18n="b.5p"></span></figcaption></figure></div></section></div>''')

# ---- 8. home: membership value → Function-style price card
rep('''<section class="value bleed" style="margin-top:88px"><div class="wrap box"><div class="mcard"><div><div class="brand">loop</div><div class="l" data-i18n="m.l"></div></div><div><div class="p" data-i18n="m.p"></div><div class="l" data-i18n="m.s"></div></div></div>
<div><h2 data-i18n="m.h"></h2><p class="lead" data-i18n="m.sub"></p><ul class="feats"><li data-i18n="m.1"></li><li data-i18n="m.2"></li><li data-i18n="m.3"></li><li data-i18n="m.4"></li><li data-i18n="m.5"></li></ul><div class="cta"><a class="btn primary" href="membership.html" data-i18n="m.cta"></a><a class="btn ghost" href="konsultasi.html" data-i18n="m.cta2"></a></div></div></div></section>''',
'''<section class="value bleed" style="margin-top:88px"><div class="wrap center"><h2 data-i18n="m.h"></h2><p class="lead" data-i18n="m.sub"></p>
<div class="pcard"><div class="pl"><span class="eyebrow">Loop</span><div class="pname" data-i18n="m.l"></div><div class="price" data-i18n="m.p"></div><div class="l" data-i18n="m.s"></div><div class="cta"><a class="btn primary" href="membership.html" data-i18n="m.cta"></a><a class="btn ghost" href="konsultasi.html" data-i18n="m.cta2"></a></div></div>
<ul class="feats"><li data-i18n="m.1"></li><li data-i18n="m.2"></li><li data-i18n="m.3"></li><li data-i18n="m.4"></li><li data-i18n="m.5"></li></ul></div></div></section>''')

# ---- 9. new copy keys (home)
rep('"a.eye":"Untuk siapa",', '"how.photo":"foto_hasil.jpg","how.reading":"Dibaca dalam ±40 detik. Tidak perlu mengetik angka.","how.p1":"Metformin 500 mg","how.p1s":"2× sehari, diingatkan lewat aplikasi","how.p2":"Porsi nasi ½, protein ditambah","how.p2s":"coach ahli gizi, chat 7 hari seminggu","how.p3":"Kontrol dokter bulan ke-1","how.p3s":"Klinik Loop atau video, dokter yang sama","b.eye":"Yang Anda dapat","b.p":"Semuanya dalam satu membership, dikirim ke rumah dan ada di aplikasi.","b.1h":"Loop Kit ke rumah","b.1p":"Glukometer Sinocare, strip, lancet","b.2h":"Coach yang bisa diajak bicara","b.2p":"Ahli gizi bersertifikat, bukan chatbot","b.3h":"Aplikasi Loop","b.3p":"Gula darah, tekanan darah, obat, makan","b.4h":"Perawatan yang terasa seperti merawat diri","b.5h":"Dokter yang sama","b.5p":"Klinik Loop, tanpa dokter berganti-ganti","a.eye":"Untuk siapa",')
rep('"a.eye":"Who it is for",', '"how.photo":"lab_photo.jpg","how.reading":"Read in about 40 seconds. No numbers to type.","how.p1":"Metformin 500 mg","how.p1s":"twice a day, reminded in the app","how.p2":"Half the rice, more protein","how.p2s":"nutrition coach, chat 7 days a week","how.p3":"Doctor check-up, month 1","how.p3s":"Loop clinic or video, the same doctor","b.eye":"What you get","b.p":"All in one membership, delivered to your home and in the app.","b.1h":"Loop Kit at home","b.1p":"Sinocare glucometer, strips, lancets","b.2h":"A coach you can talk to","b.2p":"Certified nutritionist, not a chatbot","b.3h":"The Loop app","b.3p":"Glucose, blood pressure, medication, meals","b.4h":"Healthcare that feels like self-care","b.5h":"The same doctor","b.5p":"Loop clinic, no doctor roulette","a.eye":"Who it is for",')

open(P, "w").write(s)
print("patched OK")
