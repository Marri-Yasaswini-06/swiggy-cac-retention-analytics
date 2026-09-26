# Rebuilding This Dashboard Natively in Power BI Desktop

Power BI Desktop is Windows-only desktop software, not available in the environment this
project was built in, so the dashboard here is an HTML/Chart.js prototype (`dashboard.html`)
and an Excel workbook with the same logic. To turn it into a real `.pbix` for your portfolio:

## 1. Import the data
**Get Data → Text/CSV**, import:
- `data/clean/crm_customers_clean.csv` (includes `swiggy_one_member`)
- `data/clean/marketing_interactions_clean.csv`
- `data/clean/customer_rfm_segments.csv`

## 2. Relationships
In **Model view**: `crm_customers_clean[customer_id]` → `marketing_interactions_clean[customer_id]`
and → `customer_rfm_segments[customer_id]` (both 1-to-many).

## 3. DAX measures
```DAX
Total Spend         = SUM(marketing_interactions_clean[spend])
Total Revenue        = SUM(marketing_interactions_clean[order_value])
Total Conversions    = SUM(marketing_interactions_clean[converted])
Blended ROAS         = DIVIDE([Total Revenue], [Total Spend], 0)
CAC                  = DIVIDE([Total Spend], [Total Conversions], 0)
Open Rate            = DIVIDE(SUM(marketing_interactions_clean[opened]), SUM(marketing_interactions_clean[sent]), 0)
Click-Through Rate   = DIVIDE(SUM(marketing_interactions_clean[clicked]), SUM(marketing_interactions_clean[opened]), 0)
Conversion Rate      = DIVIDE(SUM(marketing_interactions_clean[converted]), SUM(marketing_interactions_clean[clicked]), 0)

-- The headline finding: CAC split by membership. Needs a relationship to crm_customers_clean.
Member CAC     = CALCULATE([CAC], crm_customers_clean[swiggy_one_member] = TRUE)
Non-Member CAC = CALCULATE([CAC], crm_customers_clean[swiggy_one_member] = FALSE)
CAC Reduction from Membership = DIVIDE([Non-Member CAC] - [Member CAC], [Non-Member CAC], 0)
```

## 4. Report pages
- **Page 1 — Executive Summary**: 5 KPI cards (Spend, Revenue, ROAS, Conversions, distinct
  customer count) + a big callout card for `[CAC Reduction from Membership]` — this is the
  headline number, make it the largest visual on the page — + slicers for `channel` and
  `campaign_name`.
- **Page 2 — Acquisition Channel Performance**: horizontal bar of `[CAC]` by `channel`, sorted
  ascending (cheapest first); a matrix of open/click/conversion rate by `campaign_name`.
- **Page 3 — Retention & Loyalty**: clustered bar of `[CAC]` and repeat-purchase rate split by
  `swiggy_one_member`; donut of `customer_rfm_segments[tier]`.

## 5. Design/storytelling choices to carry over
- Swiggy's own brand orange (`#FC8019`) as the single accent color — consistent across Excel,
  the HTML dashboard, and this rebuild, so the deliverable reads as one coherent piece of work.
- The membership CAC comparison is the first thing on the page, not buried on page 3 of a
  "look how much I can build" dashboard — a dashboard built for a decision leads with the
  decision-relevant number.
- Channels sorted by CAC ascending (not alphabetically) so "which channel is cheapest" is
  answered by looking, not reading labels.
- One sentence of written takeaway under each chart (see `docs/key_insights.md`) rather than
  leaving the audience to interpret the chart unaided.

This gives you a real `.pbix`, built on the same business question and formulas as the rest of
this repo, that you can screenshot, publish to the Power BI service, and speak to directly in
an interview.
