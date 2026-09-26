# Interview Q&A — Swiggy Instamart CAC & Retention Analytics

Practice answers. Say them in your own words, not word-for-word.

---

**Q1. Walk me through this project in two minutes.**
Swiggy has publicly disclosed that customer acquisition costs are rising amid competition from
Blinkit and Zomato, and that it's leaning on its Swiggy One loyalty program to fight churn. I
built a case study to quantify that: cleaned a simulated but realistically messy CRM + campaign
dataset with every rule logged for auditability, then compared CAC and repeat-purchase rate for
Swiggy One members vs non-members, broke CAC down by channel and campaign, and segmented
customers with RFM. The finding — members cost 54% less to acquire and repeat-purchase almost
2x more — became a one-page recommendation memo, an Excel dashboard with live formulas, and an
interactive web dashboard.

**Q2. This isn't real Swiggy data — why should that matter to me as an interviewer?**
Because the problem is real even though the data is simulated. Swiggy's actual CRM data is
private, so I couldn't use it — but I calibrated the simulated data to match numbers Swiggy
itself disclosed publicly (CAC ~Rs 400-500, Swiggy One ARPU ~Rs 1,200, ~20% lower churn for
members), so the analysis answers a question a real Swiggy strategy team is actually facing,
using realistic magnitudes, not made-up ones. I was upfront about this distinction everywhere
in the repo rather than letting it look like real internal data.

**Q3. What's the headline finding and why does it matter commercially?**
Swiggy One members convert at roughly half the CAC of non-members and repeat-purchase at
nearly double the rate. Commercially, that means the highest-leverage lever isn't spending more
on top-of-funnel acquisition ads — it's converting existing, already-acquired customers into
loyalty members, which is cheaper and compounds through repeat purchases.

**Q4. Isn't that comparison unfair — of course existing/engaged customers convert cheaper?**
That's exactly the caveat I flagged in the executive memo: this is an observational comparison,
not a controlled experiment. Customers who were always going to stick around might just be more
likely to become members anyway (a selection effect), so the honest next step before committing
real budget would be a randomized test — offer Swiggy One upsell to a matched sample of
similar new customers and measure the actual lift, rather than trusting the raw comparison.

**Q5. Why did you separate "acquisition channels" from "retention channels" in the CAC-by-channel analysis?**
Because comparing the Swiggy One emailer (which only reaches existing members) to Performance
Ads (which acquires brand-new customers) on CAC is apples-to-oranges — of course a channel that
only messages people who already signed up looks cheaper. I explicitly excluded retention-only
channels from the "reallocate acquisition budget" recommendation and said why, because a
recommendation built on a flawed comparison would fall apart under scrutiny.

**Q6. What data-quality issues did you find and how did you handle them?**
An 8.6% customer duplicate rate (handled with an exact-email match, then a composite key of
name+city+signup date — tightened after an early version matched on name alone and over-merged
different people who shared a name), inconsistent phone/date formats, missing consent flags
(defaulted to opt-out per a real compliance principle: no consent on file means no contact),
and 48 records where the membership flag contradicted the customer's segment label — a
realistic "two systems of record disagreeing" bug that I reconciled rather than ignored.

**Q7. Where's the "advanced Excel" — isn't it just data in a spreadsheet?**
No hardcoded numbers. The dashboard tab uses `INDEX`/`MATCH` to pull the CAC for named channels
and for members vs non-members live from the raw tabs, `IFERROR` to guard divide-by-zero,
conditional formatting (data bars on CAC columns, color rules on RFM tiers), a data-validation
dropdown, and a what-if cell — type a hypothetical acquisition-budget shift and the projected
extra conversions recalculate live. I verified it with a headless recalculation and it returns
zero formula errors.

**Q8. Why isn't the dashboard a real Power BI file?**
Power BI Desktop is Windows-only desktop software, not available in the environment I built
this in. I documented the exact data model, relationships, and DAX measures needed to rebuild
it natively in Power BI Desktop (`docs/powerbi_build_guide.md`) in about 15-20 minutes, so the
analytical logic transfers directly — only the rendering tool changes.

**Q9. Why SQLite and not PostgreSQL or MySQL?**
Portfolio-project pragmatism: SQLite is a real, production-grade SQL engine — not a toy — it
just doesn't need a separate server process, so anyone who clones the repo can query it
immediately with zero setup. Every query in `scripts/06_sql_analysis.sql` is standard SQL and
would run against PostgreSQL or MySQL with only trivial syntax changes (e.g. `NTILE` and
`CASE WHEN` are supported identically; date-diff syntax is the main thing that'd need adjusting).

**Q10. What would you do differently with real production data or more time?**
Run an actual randomized controlled test for the membership-CAC claim instead of relying on an
observational comparison, use a proper fuzzy-matching library for de-duplication instead of
exact composite keys, validate phone numbers against a real numbering plan, and add
statistical-significance testing before declaring one campaign or channel definitively "better."

**Q11. How does this connect to the BCG role specifically?**
The role calls for Power BI/Excel reporting, large-dataset analysis, actionable insights, and
CRM data-quality comfort. Rather than demonstrate those skills on a generic dataset, I anchored
the whole project to a real, cited strategic question a company is actually facing right now,
and structured the output the way a consulting team would — a one-page memo with situation,
complication, and a ranked recommendation, backed by the underlying analysis and a real SQL
data layer underneath it.
