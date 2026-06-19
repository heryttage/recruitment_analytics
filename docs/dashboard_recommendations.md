# Dashboard Recommendations (Power BI)

A three-page Power BI report for the Talent Acquisition team. Source: `data/recruitment_clean.csv`.

## Page 1 — Executive Funnel (leadership view)

- **KPI cards:** Total applications, Hires, Applied→Hire %, Median time-to-hire, Cost per hire, Offer acceptance %.
- **Funnel visual:** Applied → Screened → Assessment → Interview → Offer → Hired.
- **Line chart:** Monthly applications vs hires.
- **Slicers:** Department, Region, Date range.

## Page 2 — Channel ROI (budget view)

- **Scatter:** Hire rate (y) vs Cost per hire (x), bubble = applications, by `source_channel`.
- **Clustered bar:** Total spend by channel with hires overlaid.
- **Matrix:** Channel × Department hire rate heatmap.
- **Card:** Cheapest and most expensive cost-per-hire channel.

## Page 3 — Operations (recruiter view)

- **Bar:** Time-to-hire by department and job level.
- **Table:** Recruiter scorecard (reqs, hires, avg days-to-hire, spend).
- **Stacked bar:** Rejection reason distribution by stage.
- **Column:** Hire rate by assessment score band.

## Suggested DAX measures

```DAX
Total Applications = COUNTROWS('recruitment')

Hires = CALCULATE(COUNTROWS('recruitment'), 'recruitment'[hired] = TRUE())

Hire Rate % =
DIVIDE([Hires], [Total Applications])

Offers = CALCULATE(COUNTROWS('recruitment'), 'recruitment'[offer_extended] = TRUE())

Offer Acceptance % =
DIVIDE(
    CALCULATE(COUNTROWS('recruitment'), 'recruitment'[offer_accepted] = TRUE()),
    [Offers]
)

Total Spend = SUM('recruitment'[cost_per_applicant])

Cost per Hire = DIVIDE([Total Spend], [Hires])

Avg Time to Hire =
AVERAGEX(FILTER('recruitment', 'recruitment'[hired] = TRUE()),
         'recruitment'[time_to_hire_days])

Median Time to Hire =
MEDIANX(FILTER('recruitment', 'recruitment'[hired] = TRUE()),
        'recruitment'[time_to_hire_days])
```

## Power Query notes

- Set `application_date` to Date type; mark a Date table for time intelligence.
- Trim/clean `source_channel` and `department` (already handled in Python, but replicate in Power Query if loading the raw file).
- Create a `Stage Order` index column so the funnel sorts Applied→Hired rather than alphabetically.
