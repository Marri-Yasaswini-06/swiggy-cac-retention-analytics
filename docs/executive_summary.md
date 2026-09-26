# Executive Memo: Cutting Instamart's Acquisition Cost Through Loyalty

**To:** Growth & Marketing Leadership
**Re:** CAC efficiency and the Swiggy One retention lever
**Basis:** Simulated CRM + campaign data calibrated to Swiggy's public disclosures (see
`problem_statement.md` for sources and caveats)

---

## Situation
Swiggy has publicly disclosed rising customer acquisition costs amid intensifying competition
from Blinkit and Zomato, and has stated marketing spend is expected to keep rising as the
company chases new customers and higher order volumes.

## Complication
Spending more to acquire customers on the same channel mix simply compounds the problem —
paid acquisition costs rise with competitive intensity, and the newest, most price-sensitive
customers are also the ones most likely to churn to whichever competitor offers the next
discount.

## Question
Where should the next marginal rupee of marketing budget go: more acquisition spend on
existing paid channels, or the retention/loyalty lever the company has already signaled it's
leaning into?

## Answer
**Retention, specifically Swiggy One enrollment, first — acquisition-channel reallocation
second.** The data supports both moves, but the first is roughly 3x the size of the second:

| Lever | Quantified impact | Evidence |
|---|---|---|
| **1. Prioritize Swiggy One enrollment over pure acquisition spend** | Members convert at **54% lower CAC** (Rs 28 vs Rs 60) and repeat-purchase at **26% vs 14%** | `docs/key_insights.md` #1, `visuals/cac_by_membership.png` |
| **2. Reallocate acquisition budget from Performance Ads to Referral** | Same Rs 50,000 buys **~870 more conversions** shifted from the costliest paid channel to the cheapest true acquisition channel | `docs/key_insights.md` #2 |
| **3. Target Potential/At-Risk segments for win-back + Swiggy One upsell** | Most converting customers sit in these tiers, not "Champions" — the highest-leverage, lowest-cost group to move | `docs/key_insights.md` #4, `visuals/rfm_tiers.png` |

## Recommendation (in priority order)
1. **Shift a defined share of new-customer acquisition budget into Swiggy One conversion
   campaigns** (targeted at existing non-member customers who've already ordered at least
   once) rather than only spending it on colder, more expensive top-of-funnel channels.
2. **Reweight paid acquisition spend away from Performance Ads (Search/Display) toward
   Referral**, the cheapest true acquisition channel in this data, while monitoring for
   diminishing returns as referral volume scales.
3. **Fix the underlying CRM data quality issues before scaling any of the above** — this
   analysis found an 8.6% duplicate-customer rate and a membership-flag/segment mismatch on 48
   records; at scale, errors like these silently distort exactly the CAC and retention numbers
   this recommendation depends on.

## Risk / what this doesn't answer
This is a single-snapshot, simulated-data analysis, not a causal test. It doesn't control for
the possibility that customers who *already* intended to stick around are simply more likely to
become Swiggy One members (selection effect, not a pure treatment effect). Before committing
budget at scale, the natural next step is a controlled test — e.g. randomize Swiggy One upsell
offers across a matched sample of otherwise-similar new customers and measure CAC/retention
lift directly, rather than relying on an observational comparison.
