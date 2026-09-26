# Swiggy Instamart — CAC & Retention Analytics (Case Study)

A real-world-style analytics project built to close specific skill gaps identified against a
BCG data-analyst job description — **CRM data quality/governance**, **marketing/communications
analytics**, **advanced Excel**, and **dashboard design & storytelling** — by solving an
actual, publicly disclosed business problem instead of a toy dataset.

> **⚠️ Data note:** Swiggy's real CRM/order data is private. This project is a case study
> *modeled on* a real problem Swiggy has discussed publicly (see below), using **simulated**
> customer and transaction data calibrated to Swiggy's own disclosed benchmarks. It is not, and
> does not claim to be, Swiggy's actual data. Full sourcing in `docs/problem_statement.md`.

---

## 1. The real business problem

Swiggy told investors on its **Q3 FY25 earnings call** that customer acquisition costs are
rising amid intensifying competition from Blinkit and Zomato, and that it's leaning on its
**Swiggy One loyalty program** (5M+ subscribers, ~Rs 1,200 ARPU, ~20% lower churn per public
disclosures) as the retention-side answer to that cost pressure.

**The question this project answers:** *Does Swiggy One membership measurably lower customer
acquisition cost and improve retention — and if so, where should marketing budget move next?*

Full sourcing and caveats: `docs/problem_statement.md`. The headline answer, in one line:
**Swiggy One members cost 54% less to convert and repeat-purchase almost 2x more often than
non-members** — see `docs/executive_summary.md` for the full recommendation memo.

---

## 2. What's in this repo

| Folder / file | What it is |
|---|---|
| `docs/problem_statement.md` | The real, cited business problem this project solves |
| `docs/executive_summary.md` | A one-page, BCG-style recommendation memo (situation → complication → answer) |
| `data/raw/` | Simulated but realistically messy CRM + campaign export |
| `data/clean/` | Cleaned, de-duplicated, analysis-ready CSVs |
| `scripts/01_generate_data.py` | Generates the messy raw data, calibrated to Swiggy's public benchmarks |
| `scripts/02_clean_and_govern.py` | The **data quality & governance** pipeline — every rule logged |
| `scripts/03_analysis.py` | The **marketing analytics** layer — funnel, CAC, membership comparison, RFM |
| `scripts/04_build_excel.py` | Builds the **advanced Excel** workbook (live formulas, not static numbers) |
| `scripts/05_load_sql_db.py` | Loads the cleaned data into a real **SQL database** (SQLite) with proper schema, primary/foreign keys and indexes |
| `scripts/06_sql_analysis.sql` | The core business questions answered in **pure SQL** — joins, `GROUP BY`, `CASE WHEN`, window functions (`NTILE`) for RFM |
| `database/swiggy_analytics.db` | The SQL database itself — open with any SQLite client (e.g. DB Browser for SQLite) or `sqlite3` |
| `excel/Swiggy_CAC_Retention_Analytics.xlsx` | Excel deliverable — SUMIFS, INDEX/MATCH, what-if lever |
| `dashboard.html` | Interactive, Power-BI-style **storytelling dashboard** (open in any browser) |
| `docs/data_quality_report.md` | Governance report: every cleaning rule + before/after numbers |
| `docs/key_insights.md` | The written business story — 5 insights a manager could act on |
| `docs/powerbi_build_guide.md` | Exact DAX + steps to rebuild this as a real `.pbix` |
| `docs/INTERVIEW_QA.md` | Practice Q&A for talking about this project in an interview |
| `visuals/` | Chart PNGs used in the analysis |

---

## 3. How each resume gap gets covered

| Resume gap | How this project closes it | Where to look |
|---|---|---|
| **Advanced Excel** | `SUMIFS`-style aggregation, `INDEX`/`MATCH` lookups by name, `IFERROR` guards, conditional formatting (data bars, tier colors), a data-validation dropdown, and a what-if budget-reallocation lever — verified to recalculate with **zero formula errors** | `excel/...xlsx` → `Dashboard` tab |
| **Dashboard design / storytelling** | The dashboard leads with the *decision-relevant* number (CAC reduction from membership) instead of burying it; every chart sorted by the metric that matters; one written insight per chart | `dashboard.html`, `docs/key_insights.md` |
| **CRM / data quality / governance** | A logged, auditable cleaning pipeline: de-duplication, phone/email/date standardization, a documented consent-default rule, a caught two-systems-of-record membership-flag bug, and a referential-integrity check | `docs/data_quality_report.md`, `scripts/02_clean_and_govern.py` |
| **Marketing / communications analytics** | Full funnel, CAC by channel and by membership status, RFM segmentation — anchored to a real, cited business problem rather than a generic dataset | `scripts/03_analysis.py`, `docs/problem_statement.md` |
| **SQL** | A real relational schema (primary keys, a foreign key, indexes) loaded into SQLite, with the core business questions answered in pure SQL — joins, `GROUP BY`, `CASE WHEN`, and window functions (`NTILE`) for RFM scoring — not just pandas | `scripts/05_load_sql_db.py`, `scripts/06_sql_analysis.sql` |

---

## 4. What I actually did, in plain English

**Step 1 — Started from a real problem, not a dataset.** Instead of picking a random public
dataset, I found a business problem Swiggy has *actually told investors about* — rising
acquisition costs and a stated pivot to loyalty — and built the project to answer the exact
question that problem raises.

**Step 2 — Simulated data calibrated to reality.** Swiggy's actual data is private, so I
generated realistic CRM and campaign data at a similar scale, deliberately messy (duplicates,
inconsistent formats, a membership-flag bug) and calibrated so the resulting CAC and retention
numbers land near what Swiggy has publicly disclosed — not just plausible-looking, benchmarked.

**Step 3 — Cleaned it like a governance-minded analyst.** Every cleaning decision is logged in
`docs/data_quality_report.md` with a before/after count, including a real compliance call
(missing consent defaults to opt-out) and a caught data-integrity bug (48 records where the
membership flag contradicted the segment label — a classic two-systems-of-record problem).

**Step 4 — Answered the business question with numbers, not vibes.** I compared CAC and
repeat-purchase rate for Swiggy One members vs non-members, broke down CAC by channel and
campaign, and segmented customers with RFM — then wrote the answer as five sentences a manager
could act on (`docs/key_insights.md`) and a one-page recommendation memo in BCG memo style
(`docs/executive_summary.md`), including the honest caveat that this is observational, not
a controlled experiment.

**Step 5 — Built the Excel and dashboard around the answer, not the data.** Nothing in the
Excel workbook is a typed-in number — the dashboard tab calculates the membership CAC gap live
with `INDEX`/`MATCH`, and a what-if cell lets you type a hypothetical acquisition-budget shift
and see the projected extra conversions calculated live. The HTML dashboard leads with the same
number as the biggest, first thing on the page.

---

## 5. How to run it yourself

```bash
pip install pandas numpy matplotlib seaborn openpyxl
python scripts/01_generate_data.py       # data/raw/*.csv
python scripts/02_clean_and_govern.py    # data/clean/*.csv + docs/data_quality_report.md
python scripts/03_analysis.py            # visuals/*.png + docs/key_insights.md
python scripts/04_build_excel.py         # excel/Swiggy_CAC_Retention_Analytics.xlsx
python scripts/05_load_sql_db.py         # database/swiggy_analytics.db
sqlite3 database/swiggy_analytics.db < scripts/06_sql_analysis.sql   # run the SQL queries
```
Then open `dashboard.html` directly in a browser, open the Excel file, or open
`database/swiggy_analytics.db` in any SQLite client / `sqlite3` CLI / DB Browser for SQLite.

---

## 6. Tech stack
Python (pandas, numpy, matplotlib, seaborn), **SQL** (SQLite — real schema with primary/foreign
keys and indexes, queried with joins/`GROUP BY`/window functions), openpyxl (Excel
formula/formatting automation), HTML/CSS/JavaScript + Chart.js (dashboard prototype), and a
documented path to Power BI Desktop (`docs/powerbi_build_guide.md`) with exact DAX measures.
