-- =====================================================================
-- Helios Technologies | Recruitment Analytics
-- Schema definition for the cleaned recruitment funnel dataset
-- Dialect: PostgreSQL (also runs on most ANSI-SQL engines)
-- =====================================================================

DROP TABLE IF EXISTS recruitment_applications;

CREATE TABLE recruitment_applications (
    application_id      VARCHAR(20) PRIMARY KEY,
    candidate_id        VARCHAR(20),
    department          VARCHAR(40),
    job_title           VARCHAR(60),
    job_level           VARCHAR(15),     -- Junior / Mid / Senior / Lead
    source_channel      VARCHAR(40),     -- LinkedIn, Employee Referral, ...
    region              VARCHAR(30),
    education_level     VARCHAR(20),
    gender              VARCHAR(20),
    recruiter           VARCHAR(40),
    application_date    DATE,
    years_experience    NUMERIC(4,1),
    passed_screening    BOOLEAN,
    assessment_score    NUMERIC(5,1),    -- 0-100, NULL if never assessed
    interview_rounds    INT,
    offer_extended      BOOLEAN,
    offer_accepted      BOOLEAN,
    hired               BOOLEAN,
    final_stage         VARCHAR(20),     -- Applied/Screened/Assessment/Interview/Offer/Hired
    rejection_reason    VARCHAR(40),
    time_to_hire_days   INT,             -- NULL unless hired
    cost_per_applicant  NUMERIC(10,2)
);

-- Load (PostgreSQL). Adjust the path to your local copy.
-- \copy recruitment_applications FROM 'data/recruitment_clean.csv' WITH (FORMAT csv, HEADER true);
