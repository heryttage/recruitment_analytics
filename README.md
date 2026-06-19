# Recruitment Funnel Analytics — Helios Technologies

End-to-end analysis of a talent-acquisition funnel: where candidates come from, where they drop off, how much each hire costs, and how long it takes. Built to mirror a real client engagement for a mid-sized technology employer.

> **Stack:** Python (pandas, NumPy, Matplotlib) · SQL (PostgreSQL) · Power BI-ready outputs
> **Role:** Data Analyst / People Analytics
> **Data:** 1,800 cleaned applications across 7 departments and 6 sourcing channels (Jan 2024 – Dec 2025)

---

## 1. Business context

Helios Technologies (a fictional 900-person software company) runs all hiring through a six-stage funnel — **Applied → Screened → Assessment → Interview → Offer → Hired**. Talent Acquisition spends roughly **$4.6M a year** on sourcing but the Head of People can't answer three questions with confidence:

1. Which sourcing channels are actually worth the money?
2. Where in the funnel are we losing good candidates?
3. Why does a hire take so long, and what does one cost us?

This project rebuilds the answer from raw application data.

## 2. Business problem statement

> *Recruiting spend has grown faster than headcount, time-to-hire is creeping up, and leadership suspects budget is being wasted on low-yield channels. Talent Acquisition needs an evidence base to reallocate spend, fix funnel leaks, and set realistic hiring SLAs.*

## 3. Project objectives

- Quantify conversion at every funnel stage and isolate the largest drop-off.
- Rank sourcing channels by **hire rate** and **cost per hire**, not vanity volume.
- Establish baseline KPIs: time-to-hire, cost-per-hire, offer-acceptance rate.
- Recommend a concrete budget reallocation and process changes with an estimated dollar impact.

## 4. Key business questions

1. What is the end-to-end conversion rate and where is the biggest leak?
2. Which channels deliver hires most cost-effectively?
3. How long does hiring take by department and seniority?
4. Why are candidates rejected, and at which stage?
5. Are offers being declined more from some channels (e.g. agencies)?
6. Is the skills assessment actually predictive of who gets hired?
7. How is gender representation tracking through the funnel?

## 5. Dataset

`data/recruitment_applications.csv` — raw, deliberately imperfect (duplicates, casing/whitespace noise, missing values, a few impossible dates and negative experience values) so the cleaning work is real. `data/recruitment_clean.csv` is the analysis-ready output. See [`docs/data_dictionary.md`](docs/data_dictionary.md) for every field.

Generated reproducibly with a fixed seed: `python src/generate_dataset.py`.

## 6. Data cleaning

Handled in `src/analysis.py`:

- Removed 22 exact-duplicate applications (1,822 → 1,800 rows).
- Standardised `source_channel` and `department` casing/whitespace (e.g. `linkedin` → `LinkedIn`).
- Parsed `application_date`; coerced 5 malformed dates (`2026-13-05`) to null.
- Replaced negative `years_experience` entry errors with the **median for that job level**.
- Filled missing `region` and `education_level` with `Unknown` rather than dropping rows.

## 7. Headline findings

| KPI | Value |
|---|---|
| Applications analysed | 1,800 |
| Overall applied → hired | **9.4%** (169 hires) |
| Median time-to-hire | **46 days** (p90 = 60) |
| Cost per hire (blended) | **$27,432** |
| Offer acceptance rate | **81.2%** |

**The funnel (applied → hired):**

| Stage | Candidates | % of applied |
|---|---|---|
| Applied | 1,800 | 100% |
| Screened | 1,041 | 57.8% |
| Assessment | 632 | 35.1% |
| Interview | 408 | 22.7% |
| Offer | 208 | 11.6% |
| Hired | 169 | 9.4% |


**Biggest leak:** the **Applied → Screened** step rejects 42% of all applicants — more than any other stage. A large share of that is low-quality inbound from job boards (see below).

**Channel efficiency** is where the money story lives:

| Channel | Apps | Hire rate | Cost per hire |
|---|---|---|---|
| Employee Referral | 335 | **15.5%** | **$6,959** |
| Recruitment Agency | 194 | 10.8% | **$63,136** |
| LinkedIn | 434 | 10.1% | $32,189 |
| University/Campus | 145 | 7.6% | $25,361 |
| Company Website | 265 | 6.8% | $8,131 |
| Job Board | 427 | **5.4%** | $48,115 |


Employee referrals are **the best hire on every axis**: highest hire rate at roughly one-ninth the cost of an agency hire. Job boards and agencies generate huge volume and spend for the weakest yield.

## 8. Business insights

1. **Referrals are dramatically under-leveraged.** They convert 3× better than job boards at ~14% of the cost, yet make up under a fifth of applications.
2. **Job boards flood the top of the funnel with low-fit candidates.** They drive the 42% screening rejection rate and consume recruiter time for a 5.4% yield.
3. **Agencies are the most expensive hire by far** ($63K each) and their offers are declined more often — poor value unless used surgically for hard-to-fill senior roles.
4. **Time-to-hire is consistent (~46 days)** across departments, so process — not any single team — is the constraint; senior/lead roles run longest.
5. **The assessment is predictive** — hire rate climbs sharply with score band — validating it as a screening gate worth keeping.

## 9. Recommendations

- **Launch a referral incentive program.** Shifting even 10% of job-board spend to referrals could lower blended cost-per-hire materially while improving quality. *Illustrative: moving ~$120K of job-board budget to a referral bonus pool could fund ~17 additional referral hires at the current referral cost-per-hire.*
- **Add an automated pre-screen on job-board applications** (knockout questions + assessment gate earlier) to cut the 42% manual screening load.
- **Cap agency usage** to senior/lead roles open >45 days; renegotiate fees.
- **Set hiring SLAs at 46 days** (median) with escalation at p90 (60 days).
- **Keep and standardise the skills assessment** as the primary early filter.

## 10. Executive summary

Helios spends $4.6M/year recruiting and converts 9.4% of applicants into hires at a blended $27K each. The data shows the spend is misallocated: **employee referrals are the cheapest and highest-converting channel, while job boards and agencies absorb the most budget for the weakest results.** The single biggest funnel leak is the initial screening step, driven by low-fit job-board volume. Rebalancing spend toward referrals, automating early screening, and restricting agency use to hard-to-fill roles would reduce cost-per-hire and recruiter load without sacrificing hire quality. Full detail in [`docs/executive_summary.md`](docs/executive_summary.md).

## 11. Repository structure

```
01_recruitment_analytics/
├── data/
│   ├── recruitment_applications.csv   # raw (with quality issues)
│   └── recruitment_clean.csv          # analysis-ready
├── sql/
│   ├── 01_schema.sql                  # table definition + load
│   └── 02_analysis_queries.sql        # 9 business queries
├── src/
│   ├── generate_dataset.py            # reproducible data generator
│   └── analysis.py                    # cleaning, EDA, KPIs, charts
├── docs/
│   ├── data_dictionary.md
│   ├── executive_summary.md
│   └── dashboard_recommendations.md
├── reports/
└── README.md
```


## ## 12. How to run

### Option A: Run Interactively in Your Web Browser (Recommended)
You can run individual code sections and view the interactive charts instantly without installing anything locally:

[![Open In Colab](https://google.com)](https://github.com/heryttage/recruitment_analytics/blob/main/src/analysis.ipynb)

---

### Option B: Run Locally on Your Machine
If you prefer to download and run the project locally, open your terminal and run the following commands:

```bash
# 1. Install necessary dependencies
pip install pandas numpy matplotlib notebook

# 2. Generate the underlying dataset 
python src/generate_dataset.py       # creates data/recruitment_applications.csv

# 3. Open and run the interactive notebook
jupyter notebook src/analysis.ipynb   # launches interface to execute cells and view charts

# SQL: load data/recruitment_clean.csv then run sql/02_analysis_queries.sql
```

## 13. Dashboard

A Power BI design (pages, visuals, and DAX measures) is specified in [`docs/dashboard_recommendations.md`](docs/dashboard_recommendations.md): an executive funnel page, a channel-ROI page, and a recruiter/time-to-hire operations page.

---

*Data is synthetic. Helios Technologies is fictional.*
