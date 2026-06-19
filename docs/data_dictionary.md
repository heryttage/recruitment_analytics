# Data Dictionary — Recruitment Applications

One row = one job application moving through the Helios hiring funnel.

| Field | Type | Description | Example / Values |
|---|---|---|---|
| `application_id` | string | Unique application key (primary key) | APP-100231 |
| `candidate_id` | string | Candidate identifier (a person may appear more than once) | CAND-204517 |
| `department` | string | Hiring department | Engineering, Sales, Marketing, Customer Success, Finance, People & Culture, Data & Analytics |
| `job_title` | string | Specific role applied for | Software Engineer, Account Executive |
| `job_level` | string | Seniority band | Junior, Mid, Senior, Lead |
| `source_channel` | string | How the candidate entered the funnel | Employee Referral, LinkedIn, Company Website, Job Board, Recruitment Agency, University/Campus |
| `region` | string | Candidate region | North America, EMEA, APAC, LATAM, Unknown |
| `education_level` | string | Highest education | High School, Diploma, Bachelor's, Master's, PhD, Unknown |
| `gender` | string | Self-reported gender (for diversity analysis) | Female, Male, Non-binary, Undisclosed |
| `recruiter` | string | Recruiter who owned the requisition | A. Mensah |
| `application_date` | date | Date application was submitted | 2024-07-14 |
| `years_experience` | numeric | Candidate's prior experience in years | 4.5 |
| `passed_screening` | boolean | Cleared the initial recruiter screen | TRUE / FALSE |
| `assessment_score` | numeric | Skills assessment result 0–100 (NULL if never assessed) | 78.0 |
| `interview_rounds` | int | Number of interview rounds reached (0 if none) | 2 |
| `offer_extended` | boolean | An offer was made | TRUE / FALSE |
| `offer_accepted` | boolean | Candidate accepted the offer | TRUE / FALSE |
| `hired` | boolean | Final outcome — joined the company | TRUE / FALSE |
| `final_stage` | string | Furthest stage reached | Applied, Screened, Assessment, Interview, Offer, Hired |
| `rejection_reason` | string | Why/where the candidate exited (NULL if hired) | Rejected at Screening, Failed Assessment, Offer Declined |
| `time_to_hire_days` | int | Days from application to hire (NULL unless hired) | 41 |
| `cost_per_applicant` | numeric | Sourcing + processing cost attributed to the application (USD) | 1,250.00 |

## Known data-quality issues in the raw file (resolved during cleaning)

- 22 exact-duplicate application rows.
- Mixed casing/whitespace in `source_channel` and `department`.
- 5 malformed `application_date` values (`2026-13-05`).
- 8 negative `years_experience` entry errors.
- ~5% missing `region`, ~3% missing `education_level`.
