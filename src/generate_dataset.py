"""
Recruitment Funnel Analytics - synthetic dataset generator
Company (fictional): Helios Technologies - Talent Acquisition team
Generates a realistic, messy-but-plausible recruitment dataset covering the
full hiring funnel: Applied -> Screened -> Assessment -> Interview -> Offer -> Hired.

Run:  python src/generate_dataset.py
Output: data/recruitment_applications.csv  (~1,800 rows)
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RNG = np.random.default_rng(42)
N = 1800
START = datetime(2024, 1, 1)
END = datetime(2025, 12, 31)

departments = {
    "Engineering":      {"weight": 0.34, "base_quality": 0.58, "cost": (3500, 1200)},
    "Sales":            {"weight": 0.20, "base_quality": 0.50, "cost": (2200, 800)},
    "Marketing":        {"weight": 0.13, "base_quality": 0.52, "cost": (2400, 700)},
    "Customer Success": {"weight": 0.12, "base_quality": 0.55, "cost": (1900, 600)},
    "Finance":          {"weight": 0.08, "base_quality": 0.60, "cost": (2600, 700)},
    "People & Culture": {"weight": 0.07, "base_quality": 0.57, "cost": (2100, 600)},
    "Data & Analytics": {"weight": 0.06, "base_quality": 0.62, "cost": (3200, 1000)},
}
dept_names = list(departments.keys())
dept_weights = np.array([departments[d]["weight"] for d in dept_names])
dept_weights = dept_weights / dept_weights.sum()

titles = {
    "Engineering": ["Software Engineer", "Senior Software Engineer", "DevOps Engineer", "QA Engineer", "Engineering Manager"],
    "Sales": ["Account Executive", "Sales Development Rep", "Sales Manager", "Solutions Consultant"],
    "Marketing": ["Marketing Specialist", "Content Strategist", "Growth Marketer", "Marketing Manager"],
    "Customer Success": ["Customer Success Manager", "Support Specialist", "Onboarding Specialist"],
    "Finance": ["Financial Analyst", "Accountant", "FP&A Manager"],
    "People & Culture": ["HR Business Partner", "Recruiter", "People Ops Specialist"],
    "Data & Analytics": ["Data Analyst", "Data Scientist", "Analytics Engineer"],
}
levels = ["Junior", "Mid", "Senior", "Lead"]
level_weights = [0.30, 0.40, 0.22, 0.08]

# Sourcing channels with relative volume and a quality multiplier (how strong candidates from
# that channel tend to be) and a cost-per-applicant profile.
sources = {
    "Employee Referral": {"vol": 0.18, "quality": 1.35, "cost_mult": 0.4},
    "LinkedIn":          {"vol": 0.26, "quality": 1.05, "cost_mult": 1.2},
    "Company Website":   {"vol": 0.16, "quality": 1.10, "cost_mult": 0.2},
    "Job Board":         {"vol": 0.22, "quality": 0.80, "cost_mult": 0.9},
    "Recruitment Agency":{"vol": 0.10, "quality": 1.15, "cost_mult": 2.6},
    "University/Campus": {"vol": 0.08, "quality": 0.90, "cost_mult": 0.7},
}
src_names = list(sources.keys())
src_vol = np.array([sources[s]["vol"] for s in src_names]); src_vol /= src_vol.sum()

regions = ["North America", "EMEA", "APAC", "LATAM"]
region_weights = [0.46, 0.30, 0.16, 0.08]
edu_levels = ["High School", "Diploma", "Bachelor's", "Master's", "PhD"]
edu_weights = [0.05, 0.14, 0.52, 0.25, 0.04]
genders = ["Female", "Male", "Non-binary", "Undisclosed"]
gender_weights = [0.43, 0.50, 0.02, 0.05]
recruiters = ["A. Mensah", "B. Owusu", "C. Adjei", "D. Boateng", "E. Sarpong", "F. Antwi"]

rows = []
for i in range(N):
    dept = RNG.choice(dept_names, p=dept_weights)
    title = RNG.choice(titles[dept])
    level = RNG.choice(levels, p=level_weights)
    source = RNG.choice(src_names, p=src_vol)
    region = RNG.choice(regions, p=region_weights)
    edu = RNG.choice(edu_levels, p=edu_weights)
    gender = RNG.choice(genders, p=gender_weights)
    recruiter = RNG.choice(recruiters)

    app_date = START + timedelta(days=int(RNG.integers(0, (END - START).days - 60)))

    exp_base = {"Junior": 1.5, "Mid": 4.5, "Senior": 8.5, "Lead": 12.0}[level]
    experience = max(0, round(RNG.normal(exp_base, 2.2), 1))

    # Candidate "fit" latent score drives the funnel
    q = departments[dept]["base_quality"] * sources[source]["quality"]
    fit = np.clip(RNG.normal(q, 0.16), 0.02, 0.98)

    # Stage 1: Screening
    screened = RNG.random() < (0.55 + 0.35 * (fit - 0.5))
    assessment_score = np.nan
    interview_rounds = 0
    offer = False
    accepted = False
    hired = False
    rejection_stage = None
    final_stage = "Applied"

    if screened:
        final_stage = "Screened"
        # Stage 2: Assessment (skills test)
        assessment_score = round(np.clip(RNG.normal(55 + 40 * (fit - 0.4), 12), 0, 100), 1)
        passed_assessment = assessment_score >= 60
        if passed_assessment:
            final_stage = "Assessment"
            # Stage 3: Interviews
            if RNG.random() < (0.62 + 0.3 * (fit - 0.5)):
                interview_rounds = int(RNG.integers(1, 4))
                final_stage = "Interview"
                # Stage 4: Offer
                if RNG.random() < (0.45 + 0.4 * (fit - 0.5)):
                    offer = True
                    final_stage = "Offer"
                    # Stage 5: Accept (declines happen, esp. agency/comp issues)
                    accept_p = 0.78 - (0.12 if source == "Recruitment Agency" else 0) + 0.1 * (fit - 0.5)
                    if RNG.random() < accept_p:
                        accepted = True
                        hired = True
                        final_stage = "Hired"
                    else:
                        rejection_stage = "Offer Declined"
                else:
                    rejection_stage = "Rejected at Interview"
            else:
                rejection_stage = "Rejected at Assessment"
        else:
            rejection_stage = "Failed Assessment"
    else:
        rejection_stage = "Rejected at Screening"

    # Time to hire (only meaningful when hired) - depends on level and rounds
    if hired:
        tth = int(np.clip(RNG.normal(28 + interview_rounds * 6 + {"Junior":0,"Mid":4,"Senior":10,"Lead":16}[level], 9), 9, 95))
    else:
        tth = np.nan

    base_cost, cost_sd = departments[dept]["cost"]
    cost = round(max(150, RNG.normal(base_cost, cost_sd) * sources[source]["cost_mult"]), 2)

    rows.append([
        f"APP-{100000+i}", f"CAND-{200000+int(RNG.integers(0,999999))}", dept, title, level,
        source, region, edu, gender, recruiter, app_date.date().isoformat(),
        experience, screened, assessment_score, interview_rounds, offer, accepted, hired,
        final_stage, rejection_stage, tth, cost,
    ])

cols = ["application_id","candidate_id","department","job_title","job_level","source_channel",
        "region","education_level","gender","recruiter","application_date","years_experience",
        "passed_screening","assessment_score","interview_rounds","offer_extended","offer_accepted",
        "hired","final_stage","rejection_reason","time_to_hire_days","cost_per_applicant"]
df = pd.DataFrame(rows, columns=cols)

# Inject realistic data-quality issues for the cleaning chapter --------------
# 1) duplicate applications (same candidate re-applies / dupe rows)
dupe = df.sample(22, random_state=7).copy()
df = pd.concat([df, dupe], ignore_index=True)
# 2) inconsistent source labels
mask = df.sample(frac=0.04, random_state=3).index
df.loc[mask, "source_channel"] = df.loc[mask, "source_channel"].str.lower()
# 3) some whitespace / casing noise in department
mask2 = df.sample(frac=0.03, random_state=5).index
df.loc[mask2, "department"] = " " + df.loc[mask2, "department"] + " "
# 4) missing region / education
df.loc[df.sample(frac=0.05, random_state=11).index, "region"] = np.nan
df.loc[df.sample(frac=0.03, random_state=13).index, "education_level"] = np.nan
# 5) a few negative / impossible experience values (entry errors)
df.loc[df.sample(8, random_state=17).index, "years_experience"] = -1
# 6) future-dated typo on a handful
df.loc[df.sample(5, random_state=19).index, "application_date"] = "2026-13-05"

df = df.sample(frac=1, random_state=99).reset_index(drop=True)
out = "data/recruitment_applications.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}: {len(df)} rows, {df.shape[1]} cols")
print("Hired:", int(df['hired'].sum()), "| Offers:", int(df['offer_extended'].sum()))
