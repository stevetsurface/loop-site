# Applies the branded report template to the built funnel pages (run from the project folder: python3 _funnel_build/patch_report_brand.py <files...>)
import sys
NEW=r'''  const logo=(document.querySelector('.nav img')||{}).src||'';
  const css=`@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
  :root{--navy:#313e72;--teal:#33c1b1;--teal-soft:#e6f7f5;--lav:#f6f6ff;--ink:#2a2a2a;--ink2:#363636;--body:#505454;--muted:#8a8f8f;--line:#e9e9ef;--bad:#d9534f;--bad-soft:#fde3e2}
  *{box-sizing:border-box}body{font-family:'Plus Jakarta Sans',Arial,sans-serif;color:var(--body);margin:0;background:#fff;line-height:1.55;font-size:14px}
  .page{max-width:820px;margin:0 auto;padding:0 28px 40px}
  .head{display:flex;align-items:center;gap:18px;padding:26px 0 18px;border-bottom:3px solid var(--teal)}
  .head img{width:78px;height:36px;display:block}.head .k{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);font-weight:700}
  .head h1{font-size:26px;line-height:1.2;margin:2px 0 4px;color:var(--ink);font-weight:800}.head .sub{font-size:13px;color:var(--body)}
  .meta{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:13px;color:var(--body);padding:12px 0 6px}.meta b{color:var(--ink2);font-weight:600}
  h2{font-size:19px;margin:30px 0 10px;color:var(--navy);font-weight:800;padding-left:12px;border-left:4px solid var(--teal)}
  h3{font-size:15px;margin:20px 0 8px;color:var(--ink2);font-weight:700}
  .band{color:#fff;padding:16px 18px;border-radius:16px;margin:12px 0 16px;font-size:14.5px}.band b{font-size:17px;display:block;margin-bottom:2px}
  table{border-collapse:collapse;width:100%;margin:8px 0 14px;font-size:13px}th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}th{background:var(--lav);color:var(--navy);font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;font-weight:700;border-bottom:0}tr:last-child td{border-bottom:0}
  ul{padding-left:0;list-style:none;margin:6px 0}li{border:1px solid var(--line);border-radius:14px;padding:11px 14px;margin:0 0 8px;background:#fff}li b{color:var(--ink2);display:block;margin-bottom:2px}
  .alert{border-left:4px solid var(--bad);background:var(--bad-soft);padding:10px 14px;border-radius:12px;color:var(--ink2)}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}.kpi{border:1px solid var(--line);border-radius:14px;padding:10px 12px;background:#fff}.kpi .l{font-size:11.5px;color:var(--muted);font-weight:600}.kpi .v{font-size:22px;font-weight:800;color:var(--ink)}.kpi .s{font-size:11.5px}
  .card{border:1px solid var(--line);border-radius:16px;padding:14px;margin-top:12px}.card h3{margin-top:0}.markers{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}.mk{border:1px solid var(--line);border-radius:14px;padding:10px}.mk .l{font-size:11.5px;color:var(--muted);font-weight:600}.mk .v{font-size:20px;font-weight:800;color:var(--ink)}.mk .n{font-size:11.5px}
  .chip{display:inline-block;font-size:11px;font-weight:700;padding:2px 9px;border-radius:999px;background:var(--lav);color:var(--navy)}.note{font-size:13px}.center{text-align:left}.tablewrap{overflow-x:auto}
  .cta{background:var(--lav);border-radius:18px;padding:20px 22px;margin:28px 0 0;display:grid;grid-template-columns:1fr auto;gap:14px;align-items:center}.cta h2{margin:0 0 4px;border:0;padding:0;font-size:18px}.cta p{margin:0;font-size:13.5px}
  .cta .btn{display:inline-block;background:var(--navy);color:#fff;font-weight:600;padding:12px 20px;border-radius:26px;text-decoration:none;font-size:14px;white-space:nowrap}
  .foot{margin-top:26px;border-top:1px solid var(--line);padding-top:14px;font-size:12px;color:var(--muted);display:grid;grid-template-columns:1fr 1fr;gap:12px 24px}.foot b{display:block;color:var(--ink2);font-size:12.5px;margin-bottom:2px}.foot .disc{grid-column:1/-1;margin-top:4px}
  @media (max-width:600px){.cta{grid-template-columns:1fr}.foot{grid-template-columns:1fr}.page{padding:0 16px 32px}}
  @media print{.page{max-width:none;padding:0}.cta .btn{border:1px solid var(--navy)}}`;
  const waLink='https://wa.me/6281112588833?text='+encodeURIComponent((d.rep.wamsg||'')+(name?' '+name:''));
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${d.rep.title} · Loop Health</title><style>${css}</style></head><body><div class="page"><div class="head">${logo?`<img src="${logo}" alt="Loop Health">`:'<b style="color:#33c1b1;font-size:26px">loop</b>'}<div><div class="k">Loop Health Indonesia</div><h1>${d.rep.title}</h1><div class="sub">${d.rep.sub}</div></div></div><div class="meta"><span><b>${d.rep.for}:</b> ${esc(name)}${co?' · '+esc(co):''}</span><span><b>${d.rep.date}:</b> ${date}</span></div>${body}<div class="cta"><div><h2>${d.rep.next}</h2><p>${d.rep.nextp}</p></div><a class="btn" href="${waLink}">${d.rep.cta}</a></div><div class="foot"><div><b>Loop Health Indonesia</b>PT Aplikasi Loop Health · GoWork Pacific Place, Lantai 1, Room 125, Jl. Jend. Sudirman Kav. 52-53, Jakarta Selatan 12190</div><div><b>${d.rep.contact}</b>hello@loophealth.id · WhatsApp +62 811 1258 8833 · loophealth.id</div><div class="disc">${d.rep.disc}</div></div></div></body></html>`; }'''
REPS=[
 ("rep:{title:'Laporan Hasil MCU',for:'Disiapkan untuk',date:'Tanggal',","rep:{title:'Laporan Hasil MCU',sub:'Penjelasan awal hasil pemeriksaan dan program Loop yang sesuai — bukan diagnosis',cta:'Konsultasi gratis via WhatsApp',contact:'Hubungi kami',wamsg:'Halo Loop, saya sudah menerima Laporan Hasil MCU dan ingin konsultasi gratis. Nama:',for:'Disiapkan untuk',date:'Tanggal',"),
 ("nextp:'Tim Loop akan menghubungi Anda untuk membahas laporan ini. Konsultasi pertama gratis. Hubungi hello@loophealth.id atau WhatsApp +62 811 1258 8833.'","nextp:'Tim Loop akan menghubungi Anda untuk membahas laporan ini bersama dokter dan coach. Konsultasi pertama gratis, tanpa kewajiban.'"),
 ("rep:{title:'MCU Results Report',for:'Prepared for',date:'Date',","rep:{title:'MCU Results Report',sub:'A first explanation of your check-up results and the Loop program that fits — not a diagnosis',cta:'Free consultation on WhatsApp',contact:'Contact us',wamsg:'Hi Loop, I received my MCU Results Report and would like a free consultation. Name:',for:'Prepared for',date:'Date',"),
 ("nextp:'The Loop team will contact you to walk through this report. The first consultation is free. Reach us at hello@loophealth.id or WhatsApp +62 811 1258 8833.'","nextp:'The Loop team will contact you to walk through this report with a doctor and a coach. The first consultation is free, no obligation.'"),
]
for f in sys.argv[1:]:
    s=open(f).read(); n0=len(s)
    a=s.index("  const css=`body{font-family:'Plus Jakarta Sans',Arial"); b=s.index("</body></html>`; }",a)+len("</body></html>`; }")
    s=s[:a]+NEW+s[b:]
    for x,y in REPS:
        assert x in s, (f,x[:50]); s=s.replace(x,y,1)
    open(f,'w').write(s); print('patched',f,n0,'->',len(s))
