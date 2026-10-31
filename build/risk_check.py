# Cek Risiko — one free risk check that routes to Loop's three programs (DMP, DPP, HMP).
# Executed inside build_site.py (shares page(), WA, FUNNEL) only when SITE_STAGING=1.
# Diabetes part: FINDRISC, eight items, Asia-Pacific BMI and waist cut-offs (BMI 23/25; waist M 90/100, F 80/90).
# Blood-pressure part: last known reading + diagnosis + medication. Nothing is stored or sent; WhatsApp is opt-in.
# Clinical thresholds need dr. William's sign-off before this leaves staging.

RISK_CSS = r"""<style>
.rq-wrap{max-width:720px;margin:0 auto}
.rq-prog{height:6px;background:var(--line);border-radius:3px;overflow:hidden;margin:6px 0 22px}.rq-prog i{display:block;height:100%;background:var(--teal);border-radius:3px;transition:width .25s}
.rq-meta{display:flex;justify-content:space-between;font-size:13px;color:var(--muted);font-weight:700}
.rq-q{font-family:'Fraunces',Georgia,serif;font-size:clamp(24px,3.4vw,32px);line-height:1.2;color:var(--ink);font-weight:600;margin:0 0 8px}
.rq-hint{font-size:14px;margin:0 0 20px}
.rq-opts{display:grid;gap:10px}.rq-opts.two{grid-template-columns:1fr 1fr}@media (max-width:560px){.rq-opts.two{grid-template-columns:1fr}}
.rq-opt{font:inherit;font-size:16px;font-weight:600;text-align:left;color:var(--ink2);background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:15px 18px;cursor:pointer;display:flex;gap:12px;align-items:center;transition:border-color .12s,background .12s}
.rq-opt:hover{border-color:var(--teal)}.rq-opt[aria-pressed="true"]{border-color:var(--teal);background:var(--teal-soft);color:var(--navy)}
.rq-opt .bx{flex:0 0 20px;height:20px;border-radius:6px;border:2px solid var(--line);display:grid;place-items:center;font-size:12px;color:#fff}.rq-opt[aria-pressed="true"] .bx{background:var(--teal);border-color:var(--teal)}
.rq-opt.radio .bx{border-radius:50%}
.rq-nav{display:flex;justify-content:space-between;gap:12px;margin-top:24px}
.rq-nums{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.rq-err{color:var(--bad);font-size:14px;min-height:1.4em;margin-top:8px}
.rq-res .verdict{font-family:'Fraunces',Georgia,serif;font-size:clamp(26px,3.8vw,36px);color:var(--ink);font-weight:600;line-height:1.15;margin:0 0 10px}
.rq-urgent{background:var(--bad-soft);border:1px solid #f3b7b4;color:#8a1f1b;border-radius:16px;padding:14px 16px;font-weight:600;margin:0 0 18px}
.rq-pg{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start;padding:18px;border:1px solid var(--line);border-radius:18px;background:#fff;margin-bottom:10px}
.rq-pg .ic{width:48px;height:48px;border-radius:14px;background:var(--navy);color:#fff;display:grid;place-items:center;font-weight:800;font-size:12px}
.rq-pg.no .ic{background:var(--line);color:var(--muted)}.rq-pg.no b{color:var(--muted)}
.rq-pg b{display:block;color:var(--ink);font-size:17px}.rq-pg p{margin:4px 0 0;font-size:14px}
.rq-pg .st{font-size:12px;font-weight:800;padding:4px 10px;border-radius:999px;white-space:nowrap}
.st.fit{background:var(--teal-soft);color:var(--teal-deep)}.st.check{background:var(--warn-soft);color:#8a6100}.st.no{background:var(--sand);color:var(--muted)}
.rq-gauge{margin:22px 0 6px}.rq-gauge .bar{display:flex;height:10px;border-radius:5px;overflow:hidden}.rq-gauge .bar i{display:block;height:100%}
.rq-gauge .pin{position:relative;height:18px}.rq-gauge .pin b{position:absolute;top:2px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:#fff;border:3px solid var(--navy);box-shadow:0 1px 3px rgba(0,0,0,.25)}
.rq-gauge .lbl{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);font-weight:700}
.rq-small{font-size:13px;color:var(--muted);margin-top:14px}
</style>"""

RISK_BODY = RISK_CSS + '''<section class="hero bleed" style="padding-block:56px 40px"><div class="wrap" style="grid-template-columns:1fr">
<div class="rq-wrap center"><span class="eyebrow" data-i18n="rk.eye"></span><h1 style="font-size:clamp(34px,5vw,52px)" data-i18n="rk.h1"></h1><p class="lead" style="margin-inline:auto" data-i18n="rk.lead"></p></div></div></section>
<div class="wrap"><section class="sec tight"><div class="rq-wrap"><div class="card" style="padding:28px" id="rq"></div>
<p class="rq-small center" data-i18n="rk.note"></p></div></section></div>'''

RISK_JS = r"""
const WA_NO='6281112588833', MCU_URL='""" + FUNNEL['personal'] + r"""';
const T={
id:{start:'Mulai cek risiko',back:'← Kembali',next:'Lanjut →',see:'Lihat hasil',of:'dari',q:'Pertanyaan',pick:'Pilih salah satu dulu.',pickm:'Pilih minimal satu.',hwErr:'Isi tinggi (100–220 cm) dan berat (30–250 kg).',
 intro:'<p class="rq-q">Tiga program, satu cek.</p><p class="rq-hint">Paling banyak 12 pertanyaan singkat, sekitar 2 menit. Hasilnya menunjukkan program Loop mana yang cocok: <b>Manajemen Diabetes</b>, <b>Pencegahan Diabetes</b>, atau <b>Hipertensi</b>. Jawaban dihitung di browser Anda dan tidak disimpan.</p>',
 qs:{dx:['Apakah dokter pernah mengatakan Anda punya salah satu kondisi ini?','Boleh pilih lebih dari satu.',{dm:'Diabetes',predm:'Prediabetes / gula darah agak tinggi',htn:'Hipertensi (tekanan darah tinggi)',none:'Tidak ada / tidak tahu'}],
  meds:['Apakah Anda sedang minum obat rutin untuk ini?','Boleh pilih lebih dari satu.',{dmMed:'Obat diabetes atau insulin',bpMed:'Obat tekanan darah',none:'Tidak minum obat rutin'}],
  age:['Berapa usia Anda?','',{a1:'Di bawah 35',a2:'35–44',a3:'45–54',a4:'55–64',a5:'65 atau lebih'}],
  sex:['Jenis kelamin','Dipakai untuk batas lingkar pinggang.',{m:'Laki-laki',f:'Perempuan'}],
  hw:['Tinggi dan berat badan','Perkiraan juga boleh.',{}],
  waist:['Lingkar pinggang Anda (setinggi pusar)','Kalau belum pernah mengukur, pilih "Tidak tahu".',{}],
  act:['Apakah Anda aktif bergerak minimal 30 menit hampir setiap hari?','Jalan cepat, bersepeda, olahraga, atau pekerjaan fisik.',{y:'Ya',n:'Tidak'}],
  veg:['Apakah Anda makan sayur atau buah setiap hari?','',{y:'Ya, setiap hari',n:'Tidak setiap hari'}],
  glu:['Pernahkah gula darah Anda tercatat tinggi?','Misalnya saat medical check-up, sakit, atau hamil.',{y:'Pernah',n:'Tidak pernah',u:'Tidak tahu'}],
  fam:['Adakah keluarga Anda yang punya diabetes?','',{n:'Tidak ada',d2:'Kakek/nenek, paman/bibi, atau sepupu',d1:'Orang tua, kakak/adik, atau anak'}],
  bp:['Hasil tekanan darah terakhir Anda','Dari pemeriksaan dalam 12 bulan terakhir.',{b0:'Di bawah 120/80',b1:'120–129, bawah di bawah 80',b2:'130–139 atau bawah 80–89',b3:'140/90 atau lebih',b4:'180/110 atau lebih',unk:'Tidak tahu / belum pernah cek'}],
  smoke:['Apakah Anda merokok?','Termasuk rokok elektrik.',{y:'Ya',n:'Tidak'}]},
 waistM:{w0:'Di bawah 90 cm',w1:'90–99 cm',w2:'100 cm atau lebih',unk:'Tidak tahu'},waistF:{w0:'Di bawah 80 cm',w1:'80–89 cm',w2:'90 cm atau lebih',unk:'Tidak tahu'},
 h:'Tinggi (cm)',w:'Berat (kg)',
 res:'Hasil cek risiko Anda',urgent:'Tekanan darah 180/110 atau lebih perlu diperiksa dokter hari ini. Hubungi dokter atau fasilitas kesehatan terdekat, atau chat dokter Loop sekarang.',
 v:{fit:'Cocok untuk Anda',check:'Perlu cek dulu',no:'Belum perlu',na:'Sudah tercakup'},
 pn:{DMP:'Program Manajemen Diabetes',DPP:'Program Pencegahan Diabetes',HMP:'Program Hipertensi'},
 why:{dmKnown:'Anda sudah terdiagnosis atau minum obat diabetes. Dokter tetap, coach, obat generik, dan HbA1c rutin.',dmNo:'Tidak ada diagnosis diabetes dari jawaban Anda.',
  dppNa:'Diabetes Anda ditangani lewat Program Manajemen Diabetes.',dppPre:'Dokter pernah menyebut prediabetes. Enam bulan untuk membalikkan arah sebelum jadi diabetes.',dppHigh:'Skor risiko diabetes Anda {s} dari 26: risiko 10 tahun sekitar {p}.',dppMid:'Skor {s} dari 26, sedikit di atas rata-rata. Cek HbA1c atau gula puasa untuk memastikan.',dppLow:'Skor {s} dari 26, risiko rendah. Pertahankan kebiasaan sehat.',
  hmpKnown:'Anda sudah terdiagnosis atau minum obat tekanan darah. Pantau dari rumah, dokter yang sama sampai terkendali.',hmpHigh:'Tekanan darah terakhir 140/90 atau lebih. Perlu dikonfirmasi dokter dan dikelola.',hmpMid:'Tekanan darah 130–139 / 80–89 sudah di atas normal. Ukur ulang dan bicarakan dengan dokter.',hmpUnk:'Anda belum tahu tekanan darah terakhir, dan usia atau berat badan menambah risiko. Ukur tekanan darah dulu.',hmpNo:'Tekanan darah terakhir dalam batas normal.'},
 band:['Rendah','Sedikit naik','Sedang','Tinggi','Sangat tinggi'],bandP:['±1%','±4%','±17%','±33%','±50%'],
 vAny:'Loop punya program yang cocok untuk Anda.',vCheck:'Ada yang perlu dicek dulu.',vNone:'Saat ini Anda belum memerlukan program Loop.',
 waistNote:'Lingkar pinggang belum diisi, jadi skor bisa lebih rendah dari sebenarnya.',
 ctaMcu:'Punya hasil MCU? Unggah untuk dibaca',ctaWa:'Chat dokter Loop (gratis)',again:'Ulangi',
 disc:'Bukan diagnosis. Skor diabetes memakai FINDRISC dengan batas BMI dan lingkar pinggang Asia. Keputusan medis tetap oleh dokter.',
 wa:'Halo Loop, saya baru cek risiko di web Loop. Hasil: {r}. Saya mau konsultasi gratis.'},
en:{start:'Start the risk check',back:'← Back',next:'Next →',see:'See my result',of:'of',q:'Question',pick:'Pick one first.',pickm:'Pick at least one.',hwErr:'Enter height (100–220 cm) and weight (30–250 kg).',
 intro:'<p class="rq-q">Three programs, one check.</p><p class="rq-hint">Up to 12 short questions, about 2 minutes. The result shows which Loop program fits: <b>Diabetes Management</b>, <b>Diabetes Prevention</b> or <b>Hypertension</b>. Your answers are computed in your browser and not stored.</p>',
 qs:{dx:['Has a doctor ever told you that you have any of these?','Pick all that apply.',{dm:'Diabetes',predm:'Prediabetes / slightly high blood sugar',htn:'Hypertension (high blood pressure)',none:'None / not sure'}],
  meds:['Do you take regular medication for any of these?','Pick all that apply.',{dmMed:'Diabetes medication or insulin',bpMed:'Blood-pressure medication',none:'No regular medication'}],
  age:['How old are you?','',{a1:'Under 35',a2:'35–44',a3:'45–54',a4:'55–64',a5:'65 or older'}],
  sex:['Sex','Used for the waist cut-off.',{m:'Male',f:'Female'}],
  hw:['Height and weight','An estimate is fine.',{}],
  waist:['Your waist circumference (at the navel)','If you have never measured it, pick "Not sure".',{}],
  act:['Are you active for at least 30 minutes on most days?','Brisk walking, cycling, sport or physical work.',{y:'Yes',n:'No'}],
  veg:['Do you eat vegetables or fruit every day?','',{y:'Yes, every day',n:'Not every day'}],
  glu:['Has your blood sugar ever been recorded as high?','For example at a check-up, during illness or pregnancy.',{y:'Yes',n:'Never',u:'Not sure'}],
  fam:['Does anyone in your family have diabetes?','',{n:'No one',d2:'Grandparent, aunt/uncle or cousin',d1:'Parent, sibling or child'}],
  bp:['Your most recent blood-pressure reading','From a check in the last 12 months.',{b0:'Below 120/80',b1:'120–129, lower number below 80',b2:'130–139 or lower number 80–89',b3:'140/90 or higher',b4:'180/110 or higher',unk:'Not sure / never checked'}],
  smoke:['Do you smoke?','Including e-cigarettes.',{y:'Yes',n:'No'}]},
 waistM:{w0:'Under 90 cm',w1:'90–99 cm',w2:'100 cm or more',unk:'Not sure'},waistF:{w0:'Under 80 cm',w1:'80–89 cm',w2:'90 cm or more',unk:'Not sure'},
 h:'Height (cm)',w:'Weight (kg)',
 res:'Your risk check result',urgent:'A blood pressure of 180/110 or higher needs a doctor today. Contact a doctor or the nearest health facility, or chat with a Loop doctor now.',
 v:{fit:'Fits you',check:'Check first',no:'Not needed yet',na:'Already covered'},
 pn:{DMP:'Diabetes Management Program',DPP:'Diabetes Prevention Program',HMP:'Hypertension Program'},
 why:{dmKnown:'You have a diagnosis or take diabetes medication. A fixed doctor, coach, generic medication and routine HbA1c.',dmNo:'No diabetes diagnosis in your answers.',
  dppNa:'Your diabetes is covered by the Diabetes Management Program.',dppPre:'A doctor has mentioned prediabetes. Six months to turn it around before it becomes diabetes.',dppHigh:'Your diabetes risk score is {s} of 26: about {p} risk over 10 years.',dppMid:'Score {s} of 26, slightly above average. Check HbA1c or fasting glucose to be sure.',dppLow:'Score {s} of 26, low risk. Keep the healthy habits.',
  hmpKnown:'You have a diagnosis or take blood-pressure medication. Home monitoring, the same doctor until controlled.',hmpHigh:'Your last reading was 140/90 or higher. A doctor should confirm and manage it.',hmpMid:'130–139 / 80–89 is already above normal. Re-measure and talk to a doctor.',hmpUnk:'You do not know your last reading, and your age or weight adds risk. Measure your blood pressure first.',hmpNo:'Your last reading was in the normal range.'},
 band:['Low','Slightly raised','Moderate','High','Very high'],bandP:['~1%','~4%','~17%','~33%','~50%'],
 vAny:'Loop has a program that fits you.',vCheck:'Something needs checking first.',vNone:'You do not need a Loop program right now.',
 waistNote:'Waist was not given, so the score may be lower than it really is.',
 ctaMcu:'Have MCU results? Upload them to be read',ctaWa:'Chat with a Loop doctor (free)',again:'Start again',
 disc:'Not a diagnosis. The diabetes score uses FINDRISC with Asian BMI and waist cut-offs. Medical decisions stay with a doctor.',
 wa:'Hi Loop, I just did the risk check on the Loop website. Result: {r}. I would like a free consultation.'}};
const MULTI={dx:1,meds:1};
let A={}, step=-1;
const tr=()=>T[lang];
function knownDM(){ return (A.dx||[]).includes('dm')||(A.meds||[]).includes('dmMed'); }
function steps(){ const s=['dx','meds','age','sex','hw']; if(!knownDM()) s.push('waist','act','veg','glu','fam'); s.push('bp','smoke'); return s; }
function opts(k){ const t=tr(); if(k==='waist') return A.sex==='f'?t.waistF:t.waistM; return t.qs[k][2]; }
function render(){
  const el=$('rq'), t=tr();
  if(step<0){ el.innerHTML=t.intro+'<div class="rq-nav" style="justify-content:flex-start"><button class="btn primary" id="rqGo">'+t.start+'</button></div>'; $('rqGo').onclick=()=>{step=0;render();}; return; }
  const S=steps(); if(step>=S.length){ return result(); }
  const k=S[step], q=t.qs[k], multi=!!MULTI[k];
  let h='<div class="rq-meta"><span>'+t.q+' '+(step+1)+' '+t.of+' '+S.length+'</span></div><div class="rq-prog"><i style="width:'+Math.round(step/S.length*100)+'%"></i></div>';
  h+='<p class="rq-q">'+q[0]+'</p>'+(q[1]?'<p class="rq-hint">'+q[1]+'</p>':'<div style="height:12px"></div>');
  if(k==='hw'){ h+='<div class="rq-nums"><div class="f"><label for="rqH">'+t.h+'</label><input id="rqH" type="number" inputmode="numeric" min="100" max="220" value="'+(A.h||'')+'"></div><div class="f"><label for="rqW">'+t.w+'</label><input id="rqW" type="number" inputmode="decimal" min="30" max="250" value="'+(A.w||'')+'"></div></div>'; }
  else { const o=opts(k), keys=Object.keys(o), cur=A[k]; h+='<div class="rq-opts'+(keys.length===2?' two':'')+'">'+keys.map(v=>{ const on=multi?(cur||[]).includes(v):cur===v; return '<button type="button" class="rq-opt'+(multi?'':' radio')+'" data-v="'+v+'" aria-pressed="'+on+'"><span class="bx">'+(on?'✓':'')+'</span>'+o[v]+'</button>'; }).join('')+'</div>'; }
  const last=step===S.length-1;
  h+='<div class="rq-err" id="rqErr"></div><div class="rq-nav"><button class="btn ghost sm" id="rqBack">'+t.back+'</button><button class="btn primary sm" id="rqNext">'+(last?t.see:t.next)+'</button></div>';
  el.innerHTML=h;
  el.querySelectorAll('.rq-opt').forEach(b=>b.onclick=()=>{ const v=b.dataset.v;
    if(multi){ let a=(A[k]||[]).slice(); if(v==='none') a=a.includes('none')?[]:['none']; else { a=a.filter(x=>x!=='none'); a=a.includes(v)?a.filter(x=>x!==v):a.concat(v); } A[k]=a; render(); }
    else { A[k]=v; render(); setTimeout(()=>{ if(A[k]===v) go(1); },180); } });
  $('rqBack').onclick=()=>go(-1); $('rqNext').onclick=()=>go(1);
}
function go(d){ const S=steps(), t=tr();
  if(d<0){ step=Math.max(-1,step-1); return render(); }
  const k=S[step];
  if(k==='hw'){ const hh=+$('rqH').value, ww=+$('rqW').value; if(!(hh>=100&&hh<=220&&ww>=30&&ww<=250)){ $('rqErr').textContent=t.hwErr; return; } A.h=hh; A.w=ww; }
  else if(MULTI[k]){ if(!(A[k]||[]).length){ $('rqErr').textContent=t.pickm; return; } }
  else if(!A[k]){ $('rqErr').textContent=t.pick; return; }
  step++; render(); window.scrollTo({top:$('rq').getBoundingClientRect().top+window.scrollY-110,behavior:'smooth'});
}
function score(){ // FINDRISC, Asian cut-offs; returns null when diabetes is already known
  if(knownDM()) return null;
  let s=0; s+={a1:0,a2:0,a3:2,a4:3,a5:4}[A.age]||0;
  const bmi=A.w/((A.h/100)**2); s+= bmi<23?0:bmi<25?1:3;
  s+={w0:0,w1:3,w2:4,unk:0}[A.waist]||0; s+=A.act==='n'?2:0; s+=A.veg==='n'?1:0;
  s+=(A.meds||[]).includes('bpMed')?2:0; s+=A.glu==='y'?5:0; s+={n:0,d2:3,d1:5}[A.fam]||0;
  return {s,bmi,band:s<7?0:s<12?1:s<15?2:s<21?3:4};
}
function result(){
  const t=tr(), F=score(), bmi=A.w/((A.h/100)**2), dx=A.dx||[], meds=A.meds||[];
  const P={};
  P.DMP=knownDM()?['fit',t.why.dmKnown]:['no',t.why.dmNo];
  if(knownDM()) P.DPP=['na',t.why.dppNa];
  else if(dx.includes('predm')) P.DPP=['fit',t.why.dppPre];
  else if(F.s>=12) P.DPP=['fit',t.why.dppHigh.replace('{s}',F.s).replace('{p}',t.bandP[F.band])];
  else if(F.s>=7) P.DPP=['check',t.why.dppMid.replace('{s}',F.s)];
  else P.DPP=['no',t.why.dppLow.replace('{s}',F.s)];
  if(dx.includes('htn')||meds.includes('bpMed')) P.HMP=['fit',t.why.hmpKnown];
  else if(A.bp==='b3'||A.bp==='b4') P.HMP=['fit',t.why.hmpHigh];
  else if(A.bp==='b2') P.HMP=['check',t.why.hmpMid];
  else if(A.bp==='unk'&&(['a3','a4','a5'].includes(A.age)||bmi>=25||A.smoke==='y')) P.HMP=['check',t.why.hmpUnk];
  else if(A.bp==='unk') P.HMP=['check',t.why.hmpUnk];
  else P.HMP=['no',t.why.hmpNo];
  const st=Object.values(P).map(x=>x[0]);
  const verdict=st.includes('fit')?t.vAny:st.includes('check')?t.vCheck:t.vNone;
  let h='<div class="rq-res"><span class="eyebrow">'+t.res+'</span><p class="verdict">'+verdict+'</p>';
  if(A.bp==='b4') h+='<div class="rq-urgent">'+t.urgent+'</div>';
  ['DMP','DPP','HMP'].forEach(c=>{ const [s,why]=P[c]; h+='<div class="rq-pg '+(s==='no'||s==='na'?'no':'')+'"><div class="ic">'+c+'</div><div><b>'+t.pn[c]+'</b><p>'+why+'</p></div><span class="st '+(s==='na'?'no':s)+'">'+t.v[s]+'</span></div>'; });
  if(F){ const segs=[[7,'#2a9d6f'],[5,'#9cc95a'],[3,'#d99a00'],[6,'#e07a1f'],[5,'#d9534f']];
    h+='<div class="rq-gauge"><div class="rq-meta"><span>FINDRISC '+F.s+' / 26 · '+t.band[F.band]+'</span><span>'+t.bandP[F.band]+'</span></div><div class="bar">'+segs.map(([w,c])=>'<i style="flex:0 0 '+(w/26*100)+'%;background:'+c+'"></i>').join('')+'</div><div class="pin"><b style="left:'+Math.min(98,Math.max(2,F.s/26*100))+'%"></b></div><div class="lbl"><span>0</span><span>7</span><span>12</span><span>15</span><span>21</span><span>26</span></div></div>';
    if(A.waist==='unk') h+='<p class="rq-small">'+t.waistNote+'</p>'; }
  const summary=['DMP','DPP','HMP'].map(c=>c+': '+t.v[P[c][0]]).join(', ')+(F?', FINDRISC '+F.s+'/26':'');
  h+='<div class="cta" style="margin-top:22px"><a class="btn primary" href="'+MCU_URL+'">'+t.ctaMcu+'</a><a class="btn wa" target="_blank" rel="noopener" href="https://wa.me/'+WA_NO+'?text='+encodeURIComponent(t.wa.replace('{r}',summary))+'">'+t.ctaWa+'</a></div>';
  h+='<p class="rq-small">'+t.disc+'</p><div class="rq-nav" style="justify-content:flex-start"><button class="btn ghost sm" id="rqAgain">'+t.again+'</button></div></div>';
  $('rq').innerHTML=h; $('rqAgain').onclick=()=>{A={};step=-1;render();};
}
const _apply=applyLang; applyLang=function(){ _apply(); render(); };
render();
"""

RISK_I18N = {"id": {"rk.eye": "Cek risiko gratis", "rk.h1": "Diabetes atau tekanan darah? <em>Satu cek</em>, tiga program.",
                    "rk.lead": "Jawab paling banyak 12 pertanyaan. Anda langsung melihat program Loop mana yang cocok, dan apa yang perlu dicek dulu.",
                    "rk.note": "Dihitung di browser Anda, tidak ada data yang disimpan. Bukan diagnosis."},
             "en": {"rk.eye": "Free risk check", "rk.h1": "Diabetes or blood pressure? <em>One check</em>, three programs.",
                    "rk.lead": "Answer up to 12 questions. You see straight away which Loop program fits, and what needs checking first.",
                    "rk.note": "Computed in your browser, no data is stored. Not a diagnosis."}}

page("cek-risiko.html", "Cek Risiko · Loop Health", "risk", RISK_BODY, RISK_I18N, RISK_JS)
