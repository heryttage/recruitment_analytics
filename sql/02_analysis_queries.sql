-- =====================================================================
-- Helios Technologies | Recruitment Analytics
-- Business analysis queries. Each block answers a stated business question.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Q1. What does the end-to-end hiring funnel look like, and where do we
--     lose the most candidates?
-- ---------------------------------------------------------------------
SELECT
    COUNT(*)                                                   AS applied,
    COUNT(*) FILTER (WHERE passed_screening)                   AS screened,
    COUNT(*) FILTER (WHERE final_stage IN
        ('Assessment','Interview','Offer','Hired'))            AS assessed,
    COUNT(*) FILTER (WHERE final_stage IN
        ('Interview','Offer','Hired'))                         AS interviewed,
    COUNT(*) FILTER (WHERE offer_extended)                     AS offers,
    COUNT(*) FILTER (WHERE hired)                              AS hires,
    ROUND(100.0 * COUNT(*) FILTER (WHERE hired) / COUNT(*), 2) AS applied_to_hire_pct
FROM recruitment_applications;

-- Stage-to-stage conversion (how many survive each step)
WITH f AS (
    SELECT
        COUNT(*)::numeric AS applied,
        COUNT(*) FILTER (WHERE passed_screening)::numeric AS screened,
        COUNT(*) FILTER (WHERE final_stage IN ('Assessment','Interview','Offer','Hired'))::numeric AS assessed,
        COUNT(*) FILTER (WHERE final_stage IN ('Interview','Offer','Hired'))::numeric AS interviewed,
        COUNT(*) FILTER (WHERE offer_extended)::numeric AS offers,
        COUNT(*) FILTER (WHERE hired)::numeric AS hires
    FROM recruitment_applications
)
SELECT ROUND(100*screened/applied,1)     AS applied_to_screen_pct,
       ROUND(100*assessed/screened,1)    AS screen_to_assess_pct,
       ROUND(100*interviewed/assessed,1) AS assess_to_interview_pct,
       ROUND(100*offers/interviewed,1)   AS interview_to_offer_pct,
       ROUND(100*hires/offers,1)         AS offer_to_hire_pct
FROM f;

-- ---------------------------------------------------------------------
-- Q2. Which sourcing channels deliver the best hires for the money?
--     (hire rate + cost per hire). Drives budget reallocation.
-- ---------------------------------------------------------------------
SELECT
    source_channel,
    COUNT(*)                                              AS applications,
    SUM(CASE WHEN hired THEN 1 ELSE 0 END)                AS hires,
    ROUND(100.0*SUM(CASE WHEN hired THEN 1 ELSE 0 END)/COUNT(*),1) AS hire_rate_pct,
    ROUND(SUM(cost_per_applicant),0)                      AS total_spend,
    ROUND(SUM(cost_per_applicant)/NULLIF(SUM(CASE WHEN hired THEN 1 ELSE 0 END),0),0) AS cost_per_hire
FROM recruitment_applications
GROUP BY source_channel
ORDER BY hire_rate_pct DESC;

-- ---------------------------------------------------------------------
-- Q3. How fast do we hire, by department and seniority? (time-to-hire KPI)
-- ---------------------------------------------------------------------
SELECT
    department,
    job_level,
    COUNT(*) FILTER (WHERE hired)                         AS hires,
    ROUND(AVG(time_to_hire_days) FILTER (WHERE hired),1)  AS avg_days_to_hire,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY time_to_hire_days)
        FILTER (WHERE hired)                              AS median_days_to_hire
FROM recruitment_applications
GROUP BY department, job_level
ORDER BY department, avg_days_to_hire DESC;

-- ---------------------------------------------------------------------
-- Q4. Where exactly are candidates being rejected? (drop-off diagnosis)
-- ---------------------------------------------------------------------
SELECT
    COALESCE(rejection_reason, 'Hired')                   AS outcome,
    COUNT(*)                                              AS candidates,
    ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (), 1)        AS pct_of_total
FROM recruitment_applications
GROUP BY COALESCE(rejection_reason, 'Hired')
ORDER BY candidates DESC;

-- ---------------------------------------------------------------------
-- Q5. Offer acceptance rate by channel - are agency offers being declined?
-- ---------------------------------------------------------------------
SELECT
    source_channel,
    COUNT(*) FILTER (WHERE offer_extended)                AS offers,
    COUNT(*) FILTER (WHERE offer_accepted)                AS accepted,
    ROUND(100.0*COUNT(*) FILTER (WHERE offer_accepted)
          /NULLIF(COUNT(*) FILTER (WHERE offer_extended),0),1) AS acceptance_rate_pct
FROM recruitment_applications
GROUP BY source_channel
ORDER BY acceptance_rate_pct DESC;

-- ---------------------------------------------------------------------
-- Q6. Recruiter productivity scorecard (hires, avg time-to-hire, spend)
-- ---------------------------------------------------------------------
SELECT
    recruiter,
    COUNT(*)                                              AS reqs_handled,
    SUM(CASE WHEN hired THEN 1 ELSE 0 END)                AS hires,
    ROUND(AVG(time_to_hire_days) FILTER (WHERE hired),1)  AS avg_days_to_hire,
    ROUND(SUM(cost_per_applicant),0)                      AS spend
FROM recruitment_applications
GROUP BY recruiter
ORDER BY hires DESC;

-- ---------------------------------------------------------------------
-- Q7. Monthly application & hire trend (seasonality / pipeline health)
-- ---------------------------------------------------------------------
SELECT
    DATE_TRUNC('month', application_date)                 AS month,
    COUNT(*)                                              AS applications,
    SUM(CASE WHEN hired THEN 1 ELSE 0 END)                AS hires
FROM recruitment_applications
WHERE application_date IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------------
-- Q8. Assessment score vs outcome - is the test predictive of hiring?
-- ---------------------------------------------------------------------
SELECT
    CASE
        WHEN assessment_score IS NULL          THEN '0 - not assessed'
        WHEN assessment_score < 60             THEN '1 - below 60'
        WHEN assessment_score < 75             THEN '2 - 60-74'
        WHEN assessment_score < 90             THEN '3 - 75-89'
        ELSE                                        '4 - 90+'
    END                                                   AS score_band,
    COUNT(*)                                              AS candidates,
    ROUND(100.0*SUM(CASE WHEN hired THEN 1 ELSE 0 END)/COUNT(*),1) AS hire_rate_pct
FROM recruitment_applications
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------------
-- Q9. Diversity lens: gender representation across the funnel stages
-- ---------------------------------------------------------------------
SELECT
    gender,
    COUNT(*)                                              AS applied,
    COUNT(*) FILTER (WHERE offer_extended)                AS offers,
    COUNT(*) FILTER (WHERE hired)                         AS hires,
    ROUND(100.0*COUNT(*) FILTER (WHERE hired)/COUNT(*),1) AS hire_rate_pct
FROM recruitment_applications
GROUP BY gender
ORDER BY applied DESC;
