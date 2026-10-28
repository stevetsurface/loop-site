# Loop Health · site prototype + MCU analyzer

Static prototype of the loophealth.id redesign (Loop 2.0 design system) together with the
"Cek Hasil MCU" top-of-funnel pages and the internal clinical MCU analyzer. Plain HTML, no
build server needed: open `index.html` or host the folder on GitHub Pages.

## Pages

| Path | What it is | Works without Claude? |
|---|---|---|
| `index.html` | Home (bilingual ID/EN) | yes |
| `personal.html`, `perusahaan.html`, `asuransi.html` | Audience pages | yes |
| `membership.html`, `konsultasi.html` | Membership value page, free-consult form (opens WhatsApp) | yes |
| `cek-mcu.html` | **Personal funnel**: upload MCU PDF/photo → plain-Bahasa result → report gate | PDF/photo reading needs the Claude viewer (see below). "Lihat contoh" example buttons and the example report work everywhere. |
| `bisnis-mcu.html` | **Corporate funnel**: employee MCU Excel/CSV → risk distribution, who needs a doctor, per-employee table | yes (Excel/CSV is parsed in the browser). PDFs need Claude. |
| `asuransi-mcu.html` | **Insurer/TPA funnel**: ICD-10 claims CSV/XLSX → 4-bucket segmentation, cost attribution | yes, fully client-side |
| `analyzer/index.html` | **Internal clinical analyzer** for dr. William's review: member form, cohort CSV, rule book tab with every threshold | yes (manual entry is allowed here; it is an internal tool) |

Nothing is sent to a server. Claims and MCU spreadsheets are processed in the browser.

## Testing the analyzer

1. **Rules and thresholds**: open `analyzer/index.html` → *Rule book* tab. The *Member* tab has sample
   patients (`SAMPLES`) and a form; the *Cohort* tab takes a CSV with one row per member.
2. **Corporate upload**: open `bisnis-mcu.html` and drop any MCU Excel/CSV with Indonesian or English
   headers (nama, usia, jenis kelamin, HbA1c, GDP, tekanan darah "120/80" or sistolik/diastolik,
   kolesterol total, LDL, HDL, TG, kreatinin, …). Or click the synthetic 60-employee example.
3. **Claims upload**: open `asuransi-mcu.html` and drop a claims file with member id, ICD-10 code,
   amount, age, date columns (auto-detected, manual override available). Or use the synthetic
   1,200-member example.
4. **Personal PDF/photo**: extraction uses the Claude artifact runtime, so it only runs inside the
   published artifact at https://claude.ai/artifact/GMJzuH59Gv79aCw3kMP15J. On GitHub Pages the page
   says so and offers the example instead. Production replaces this with a small serverless endpoint
   (see `docs/BUILD_NOTES.md`).

All example data on the pages is synthetic and labelled as such.

## Rebuilding the six site pages

```bash
SITE_OUT="$(pwd)" SITE_LOCAL=1 python3 build/build_site.py
```

`build/build_site.py` holds the shared CSS, header/footer, copy (ID + EN dictionaries) and page
bodies. `SITE_LOCAL=1` points the upload buttons at the local funnel pages instead of the Claude
artifacts. The `patch_*.py` scripts are the one-off patches that were applied to the funnel pages
and are kept for reference. Photos and logos in `img/` come from loophealth.id's own Webflow CDN.

## Clinical sources (precedence)

Eligibility Criteria v3 → Deltamas Clinical Protocol 2.2 → Clinical Reference Jun 2026 →
NCD Guidelines SOP v1 → MCU Scanner May 2026. Public pages show only the three programs Loop
sells (DMP, DPP, HMP). There is no cholesterol program; the internal analyzer still shows the full v3 grid.

The result is not a diagnosis. Thresholds must be signed off by dr. William before anything goes live
(see the proof pack, item 2).

## Staging

| Environment | URL | Purpose |
|---|---|---|
| Live | https://stevetsurface.github.io/loop-site/ | What you share |
| Staging | https://stevetsurface.github.io/loop-site/staging/ | Try changes first. Purple "STAGING" banner, `noindex` on every page. |

Workflow, run from the project folder (the one that contains `loop-site/`):

```bash
python3 _funnel_build/build_repo.py staging   # rebuild loop-site/staging/ from the sources
python3 _funnel_build/build_repo.py promote   # copy staging over the live pages, minus banner and noindex
```

Commit and push `loop-site/` after either step; GitHub Pages redeploys in about 30 seconds.
Staging is unlisted, not private: anyone with the URL can open it.
