import os, re
B = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(B)
def sub_all(s, pairs, label):
    for old, new in pairs:
        n = s.count(old); s = s.replace(old, new)
        print(f"  {label}: {n:3d} × {old[:60]!r}")
    return s
# ---- site builder
p = os.path.join(B, "build_site.py"); s = open(p).read()
s = sub_all(s, [
 ("Program Manajemen Diabetes + Program Tekanan Darah & Kolesterol", "Program Manajemen Diabetes + Program Hipertensi"),
 ("Diabetes Management + Blood Pressure & Cholesterol Program", "Diabetes Management + Hypertension Program"),
 ('"p.3f":"Hipertensi & kolesterol"', '"p.3f":"Hipertensi"'), ('"p.3f":"Hypertension & cholesterol"', '"p.3f":"Hypertension"'),
 ('"p.3h":"Program Tekanan Darah & Kolesterol"', '"p.3h":"Program Hipertensi"'), ('"p.3h":"Blood Pressure & Cholesterol Program"', '"p.3h":"Hypertension Program"'),
 ("Pantau tekanan darah dari rumah, kolesterol ke target, obat yang tepat sampai terkendali.", "Pantau tekanan darah dari rumah, obat yang tepat, dokter yang sama sampai terkendali."),
 ("Home blood-pressure monitoring, cholesterol to target, the right medication until controlled.", "Home blood-pressure monitoring, the right medication, the same doctor until controlled."),
 ("tingkat diabetes, tekanan darah, dan kolesterol", "tingkat diabetes dan tekanan darah"), ("your diabetes, blood pressure and cholesterol levels", "your diabetes and blood pressure levels"),
 ("diabetes, hipertensi, dan kolesterol", "diabetes dan hipertensi"), ("diabetes, hypertension and cholesterol", "diabetes and hypertension"),
 ("diabetes, prediabetes, hipertensi, atau kolesterol tinggi", "diabetes, prediabetes, atau hipertensi"), ("diabetes, prediabetes, hypertension or high cholesterol", "diabetes, prediabetes or hypertension"),
 ('"ko.o2":"Tekanan darah / kolesterol saya"', '"ko.o2":"Tekanan darah saya"'), ('"ko.o2":"My blood pressure / cholesterol"', '"ko.o2":"My blood pressure"'),
], "site")
open(p, "w").write(s)
# ---- funnel pages (source of truth at project root)
for f in ["Loop_Cek_MCU_Funnel.html", "Loop_Bisnis_MCU_Funnel.html", "Loop_Asuransi_MCU_Funnel.html"]:
    fp = os.path.join(PROJ, f); t = open(fp).read()
    t = sub_all(t, [
     ("Program Tekanan Darah & Kolesterol", "Program Hipertensi"), ("Blood Pressure & Cholesterol Program", "Hypertension Program"),
     ("<strong>Tekanan Darah & Kolesterol</strong>", "<strong>Hipertensi</strong>"), ("<strong>Blood Pressure & Cholesterol</strong>", "<strong>Hypertension</strong>"),
     ("Tekanan Darah & Kolesterol", "Hipertensi"), ("Blood Pressure & Cholesterol", "Hypertension"),
     ("diabetes, hipertensi, dan kolesterol", "diabetes dan hipertensi"), ("diabetes, hypertension and cholesterol", "diabetes and hypertension"),
     ("diabetes / hipertensi / kolesterol", "diabetes / hipertensi"), ("diabetes / hypertension / cholesterol", "diabetes / hypertension"),
     ("Pantau tekanan darah dari rumah, kolesterol ke target, obat generik", "Pantau tekanan darah dari rumah, obat generik"),
     ("Monitor blood pressure at home, bring cholesterol to target, the right generic", "Monitor blood pressure at home, the right generic"),
     ("// Loop sells three programs; cholesterol/heart is part of the blood-pressure program", "// Loop sells three programs (DMP, DPP, HMP); there is no cholesterol program — CMP routes to doctor review"),
     ("const PROG_ALIAS={CMP:'HMP'};", "const PROG_ALIAS={};"),
     ("const hasLK=R=>R.enrolled.concat(R.candidates).some(c=>c==='LKMP'||c==='WMP');", "const hasLK=R=>R.enrolled.concat(R.candidates).some(c=>c==='LKMP'||c==='WMP'||c==='CMP');"),
     ("'r.lk':'Ada temuan lain (fungsi hati, ginjal, tiroid, pernapasan, atau suasana hati).", "'r.lk':'Ada temuan lain (kolesterol, fungsi hati, ginjal, tiroid, pernapasan, atau suasana hati)."),
     ("'r.lk':'There is another finding (liver, kidney, thyroid, respiratory or mood).", "'r.lk':'There is another finding (cholesterol, liver, kidney, thyroid, respiratory or mood)."),
    ], f[:14])
    open(fp, "w").write(t)
print("ok")
