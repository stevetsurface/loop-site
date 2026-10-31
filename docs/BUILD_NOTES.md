# Cek Hasil MCU · top-of-funnel build notes

14 Oct 2026 · Steve + Claude · companion to `Loop_Cek_MCU_Funnel.html` (prototype) and `Loop_MCU_Analyzer_Oct2026.html` (clinical tool)

## What exists today

- **loophealth.id is a Webflow site** (site id `6604e317c246f4f15374dce0`). There is no code repo for it. Pages are edited in the Webflow Designer; custom code goes in Project Settings → Custom Code or a page-level Embed element. The current top funnel is `/diabetes-calculator` (Typeform FINDRISC embed) → "Konsultasi Gratis" → WhatsApp +62 811 1258 8833 → `/loop-membership`.
- **Prototype funnel page** (Claude artifact): upload PDF/photo → Claude reads the values → plain-Bahasa result + matching Loop program → WhatsApp consult with a prefilled summary. It runs the same rule engine as the clinical analyzer (Eligibility v3, protocol 2.2, 5-tier wellness).
- The prototype's upload works only inside the Claude viewer (it uses the viewer's Claude account). It cannot be embedded on loophealth.id as-is.

## Production architecture (recommended)

| Layer | Choice | Why |
|---|---|---|
| Page | Webflow page `/cek-mcu` with an Embed element holding the HTML/JS of the funnel page (engine + UI). | No repo needed, same look as the site, marketing can edit copy. |
| Extraction | Small serverless endpoint (Supabase Edge Function or Vercel) that receives the file, calls the Claude API with the same extraction prompt, returns the JSON. | Keeps the API key off the page; same prompt as the prototype; images and PDFs handled server-side with `pdf-parse`. |
| Leads | Supabase table `mcu_leads` (name, WA number, employer, tier, programs, summary values, consent timestamp, UTM). Edge Function writes it, then pings the sales WhatsApp / CRM. | Loop already has a Supabase connector; one table is enough for V1. |
| Hand-off | WhatsApp deep link with prefilled summary (as in the prototype) plus the row in Supabase. | Zero friction for the member; sales gets structured context. |
| Analytics | Events: `mcu_upload`, `mcu_result_<tier>`, `mcu_program_<code>`, `mcu_wa_click`, `mcu_lead_saved`. GA4 via Webflow. | Measures the funnel step by step. |

Estimated build: 2–3 days for an engineer who has the two artifact files. The engine (`analyze()`) is copied verbatim; only the upload and lead calls change.

## Compliance before launch

- MCU results are **sensitive personal data under UU PDP (Law 27/2022)**. Explicit consent text, purpose limitation (analysis + contact), retention policy (delete the file after extraction; keep only the extracted values and the lead), and a privacy-policy update are required. The prototype's consent checkbox wording is a starting point for legal review.
- The result page must say it is not a diagnosis (already in the footer). Red-tier results should push to a doctor the same day, not to a sales conversation first.
- dr. William signs off the thresholds in the rule book tab of the clinical analyzer before the public page goes live; the funnel uses the same constants.

## Funnel copy decisions to make

1. Which programs are marketed publicly now. The prototype names all six v3 programs; the live site only sells the diabetes program. Hide CMP/LKMP/WMP cards and route them to "Konsultasi dokter Loop" if those are not sellable yet.
2. Whether B2B HR gets its own entry ("Upload the whole cohort") on the Bisnis page, pointing at the cohort mode of the clinical analyzer.
3. Whether the Typeform FINDRISC stays as the no-lab path (recommended: "Belum punya hasil MCU? Cek risiko diabetes" link under the upload box).

## Update 15 Oct 2026 · two funnels on one page

- **Individual funnel is upload-only.** The manual entry form was removed. Values Claude reads from the PDF/photo are shown as chips under the drop zone so the visitor can sanity-check them before the result. A "see a sample result" button remains for demos.
- **Payer / employer funnel added** (`#payer` section, linked from the Bisnis nav item and the hero's second button). Visitor uploads a claims CSV/XLSX with ICD-10 codes; the page runs Loop's 4-bucket segmentation from `Loop_ICD_Codes_for_Partner_Analysis_Jun2026` entirely in the browser (Bucket A primary NCD, B complications-only, C both, D healthy; waterfall assignment; members aged ≤21 excluded; per-claim cost attribution; optional J42–J47 respiratory sensitivity). Output: addressable cohort % of members and % of spend against the ~20% / ~34% benchmark, per-bucket table with cost multiple vs healthy, top conditions by spend with the Loop program each maps to (v3 grid Appendix A), and a WhatsApp CTA carrying the headline numbers. No data leaves the device, which is the pitch for insurers nervous about sharing claims.
- Column mapping auto-detects Indonesian and English headers (peserta/member, kode ICD/diagnosis, biaya/klaim/amount, usia/age, tanggal/date) with manual override. Amounts accept Rp 1.250.000 and 1,250,000.50 formats; codes accept E119 or E11.9.
- Bilingual ID/EN toggle covers both funnels, including dynamic results and WhatsApp messages.
- Production note: the payer analysis needs no backend at all (pure client-side JS), so it can go into the Webflow Embed as-is. Only the individual upload needs the serverless extraction endpoint.

## Update 15 Oct 2026 (later) · two pages, one source, report gate

- **Two pages now**, built from one source (`scratchpad/funnel_src.html` + `build.py`): the Personal page `Loop_Cek_MCU_Funnel.html` and the Business page `Loop_Bisnis_MCU_Funnel.html`. Markers `<!--PERSONAL-->` / `<!--B2B-->` select sections; a `PAGE` constant switches copy (hero, drop-zone text, "not a diagnosis" line, report CTA). The two pages cross-link.
- **Personal**: free upload (one PDF/photo, or several pages). Excel/CSV is redirected to the Business page. No manual entry.
- **Business**: free upload of an employee MCU Excel/CSV (auto-detected columns in Indonesian or English, combined "120/80" blood-pressure cells handled), ICD-10 claims data (4-bucket segmentation), or several MCU PDFs (one per employee). Outputs risk-level distribution, who needs a doctor now, programs needed, per-employee table, or the claims buckets.
- **"Not a diagnosis" positioning** sits under the drop zone on both pages: it helps the visitor understand the level of diabetes, hypertension and cholesterol (their own or their employees') and which Loop program to enter.
- **Report gate**: results show on the page; the shareable report is unlocked by name + email (+ WhatsApp, company) and a consent tick. The report is a self-contained HTML document (personal summary, employee summary, or claims analysis) rendered inline and saved via the viewer's download prompt. In production the same HTML is emailed by the backend and the lead row is written to Supabase; that email is the hand-off that lets Loop follow up.
- Synthetic demo data on the Business page: 60-employee MCU sheet and 1,200-member claims file, both labelled synthetic.

## Update 15 Oct 2026 (evening) · three pages + example report

- **Three pages from one source** (`build.py`, markers `<!--PERSONAL-->`, `<!--CORPORATE-->`, `<!--INSURER-->`, comma-combinable): Personal (`Loop_Cek_MCU_Funnel.html`), Corporate for HR (`Loop_Bisnis_MCU_Funnel.html`: employee MCU Excel/CSV, several PDFs, photos), Insurer / TPA (`Loop_Asuransi_MCU_Funnel.html`: ICD-10 claims, 4-bucket). Each page redirects the wrong file type to the right sibling page with a one-line message, and the three cross-link in the nav and in a card near the footer.
- **Example report on every page.** A section titled "The report you get back" renders the actual report document (same `reportHTML()` used after the contact form) from synthetic data: Budi's personal report, a 60-employee company report, a 1,200-member claims report. Labelled synthetic. This is the lead-gen asset shown before the gate.
- Report generation and claims segmentation are now pure functions (`reportHTML(state)`, `segmentRows(rows, map, resp)`) so the examples and the real run share code.

## Update 23 Oct 2026 · Loop 2.0 site prototype (whole website)

- **Six-page site prototype** built by `_funnel_build/build_site.py` into `_site/` and published as one artifact (main page = home; personal, perusahaan, asuransi, membership, konsultasi as supporting files): https://claude.ai/artifact/BiNbJRigeW9wxaFn868gxr. Bilingual, one shared header/footer, one CSS block (Loop 2.0 tokens: mint ground #f2f9f8, deep navy #0f2a3a, teal #2fb8ab, 24px cards, 58px display type). Photo placeholders are teal gradient frames labelled "Foto: ganti dengan member Loop".
- Audience pages are marketing wrappers whose primary button opens the matching upload page (the upload pages keep their own artifacts because the Claude extraction capability only runs on an artifact's main page). In production both merge into one page per audience.
- The three upload pages got the same tokens (`_funnel_build/patch_loop2_tokens.py`) and a nav-button contrast fix (`.nav .links a.btn{color:#fff}`), which also applied to the earlier homepage draft.
- Research: Mobbin sections and screens from Hims, Hers, Superpower, Function, Headspace, Oura, Grammarly, Intercom, Perplexity Health; links in the redesign brief doc.
- Still needed from Loop: hero photos (3), partner logos, membership price (card and comparison table carry placeholders), FAQ answers confirmed by the team, counsel sign-off before the funnel pages go live.

## Update 23 Oct 2026 (later) · real pictures on the site prototype

- Photos and logos now come from loophealth.id's own Webflow CDN (downloaded into `_site/img/`, published as artifact files under `img/`): Sadimin hero photo with a floating "9% → 6,4% HbA1c" badge; member portraits (Hendry, Lenny, Lilis, Zulkarnain, Sugianto) as avatars on the quote cards; app, coach-chat and Loop Kit images on the home "how it works" steps; Loop Kit in the corporate hero; the two-phone app mockup in the insurer hero and on the membership page with the real App Store / Google Play links; partner logo SVGs (mQare, Sinocare, Equira Life, Rumat, Lontar Papyrus, Indah Kiat, FWD, Marsh, Prodia, Sampoerna, Suzuki, Roche, SehatQ, UGM) in the "Dipercaya oleh" row and as badges on the corporate quote cards.
- Patch script: `_funnel_build/patch_site_images.py` (applied once to `build_site.py`; helpers `pic()`, `av()`, `logos_row()`, tables `HERO_PIC`, `QUOTE_AV`, `LOGOS`). Rebuild with `python3 _funnel_build/build_site.py`; the main artifact page is `index.html` stripped of its doctype/head wrapper.
- Still placeholder: Lanny Santosa (no photo on the site), a corporate-site photo for the Perusahaan hero (Loop Kit used for now), and the Konsultasi page has no picture by design.

## Update 26 Oct 2026 · Mobbin round 2 (Loop 2.1) and no cholesterol program

- **Loop 2.1 design pass** (`_funnel_build/patch_mobbin_round2.py`, references: Function, Superpower, Hims, Ease, Headspace on Mobbin): Fraunces serif display headlines with one italic teal accent phrase per headline; floating white pill nav (sticky, blurred); hero on sand with a divider-style trust strip; "how it works" as three Function-style cards with mini UI (upload drop zone, range-bar reading, plan list); bento "what you get" grid (Loop Kit, coach chat, app, member photo, navy checklist tile); result cards with full-width member photos; Function-style membership price card (price left, checklist right); footer as a card with logo, tagline and App Store / Google Play badges.
- **No cholesterol program** (Steve, 26 Oct): HMP is the hypertension program only. Program names and offers no longer mention cholesterol anywhere on the site or the three upload pages; cholesterol stays as a lab marker in readings. In the funnel engine `PROG_ALIAS` is empty and CMP joins LKMP/WMP in the doctor-review note (`r.lk`), so a cholesterol-only finding is reviewed by the Loop doctor rather than mapped to a program. Patch: `_funnel_build/patch_no_cholesterol.py`.
- Repo `stevetsurface/loop-site` is public with GitHub Pages at https://stevetsurface.github.io/loop-site/ (site, `cek-mcu.html`, `bisnis-mcu.html`, `asuransi-mcu.html`, `analyzer/`). Funnel pages there are wrapped copies of the project-root files with artifact links rewritten to relative paths and a plain-browser download fallback for the report.

## Backlog · parked behind the proof gate (28 Oct 2026, from a review of lif.id)

LIF (PT Living Fitness Indonesia) is a corporate-wellness competitor: smart ring + app, gamified challenges, sold on engagement. Loop sells clinical outcomes for the NCD cohort. Ideas worth borrowing, in priority order. None ship until the five proof items exist.

1. **HR risk quiz (no data needed).** "Seberapa besar risiko diabetes & hipertensi di perusahaan Anda?" About 10 questions, one per screen, with a progress bar: age mix, shift work, last MCU date, known DM/HTN cases. Ends on an estimated at-risk share and a nudge to upload the MCU recap. Pattern: lif.id/insights/healthy-workspace-calculator (15 Likert questions in 3 stages).
2. **PMPM estimator on Perusahaan.** Employee count in; PMPM, monthly and contract totals out, compared against the NCD-cohort share of claims. Pattern: lif.id/wellness-program-pricing (team-size slider, 3/6/12-month picker, discount struck through). **Blocked on Loop's PMPM figure.**
3. **Gated case-study PDFs.** Lontar Papyrus, Indah Kiat, mQare as one-page before/after (HbA1c and BP control rates), unlocked by name + email.
4. **Gated guide.** "Panduan MCU untuk HR": reading the vendor recap, handling red-flag employees, UU PDP obligations. Doubles as SEO.
5. **One-question-per-screen** pattern for the personal funnel's contact gate.

Do not copy: app-review star carousels, "3X productivity" or engagement-percentage hero stats. These are wellness-marketing claims that weaken the "not a diagnosis, see a doctor" positioning.

## Update 31 Oct 2026 · unified risk check on staging

- **Why.** The live risk check is Typeform form `R7pHeBZ5`, embedded on loophealth.id/diabetes-calculator. It covers diabetes only. Known problems: European BMI/waist cut-offs, Q1 has no "Tidak" answer, no consent screen (see `loop-screening-vs-intake-comparison.md`). It is not in any GitHub repo.
- **What.** `cek-risiko.html`, staging only (`_funnel_build/risk_check.py`, built when `SITE_STAGING=1`): https://stevetsurface.github.io/loop-site/staging/cek-risiko.html. One check, three programs. Up to 12 questions, one per screen, bilingual.
  - Diabetes: FINDRISC's eight items with Asia-Pacific cut-offs (BMI 23/25; waist M 90/100 cm, F 80/90 cm). Score 0–26, bands <7 / 7–11 / 12–14 / 15–20 / >20.
  - Hypertension: diagnosis, BP medication, last reading in bands (incl. "don't know" and ≥180/110).
  - Routing: DMP fits if diagnosed or on diabetes medication (FINDRISC questions are then skipped, 7 questions total). DPP fits on known prediabetes or FINDRISC ≥12; "check first" at 7–11. HMP fits on diagnosis, BP medication or ≥140/90; "check first" at 130–139/80–89 or unknown reading. ≥180/110 shows a see-a-doctor-today banner.
  - Nothing stored; result CTAs are the MCU upload and a WhatsApp message carrying the summary. No personal data collected, so no PDP consent screen needed at this step.
- On staging the "Cek Risiko" buttons (home hero, footer) point here instead of the Typeform. Live site and Claude artifacts are unchanged.
- **Before promoting:** dr. William signs off the Asian cut-offs and routing thresholds (same sign-off as the proof pack's threshold table). Decide whether the Typeform's lead fields (name, WhatsApp, province) are still wanted; if so they go after the result, with consent.
