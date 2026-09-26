# Problem Statement — Swiggy Instamart: Customer Acquisition Cost & Retention

## Important note on data
This is a **case study modeled on a real, publicly disclosed business problem**, not an
engagement with Swiggy and not built on Swiggy's actual internal data (which is private).
Everything below the line is public information with sources. The customer- and
transaction-level data used for the analysis (`data/`) is **synthetic**, generated to match
the scale and shape of Swiggy's disclosed metrics, so the analytical techniques and
conclusions are real even though the specific rows are simulated. This distinction is stated
plainly here, in the README, and in every data file's provenance so nothing in this repo could
be mistaken for actual Swiggy data.

---

## The real, public situation

Swiggy — India's largest food-delivery platform and owner of the quick-commerce service
Instamart — has told investors directly that customer acquisition is getting more expensive.
On its **Q3 FY25 earnings call (Feb 2025)**, the company disclosed that performance and brand
marketing costs were rising, attributing it to heightened competitive intensity, and that
Instamart's contribution margin per order dropped more than rival Blinkit's during the same
quarter while both companies scaled up dark-store expansion.

Independent analysis of Swiggy's public filings puts its **CAC at roughly Rs 400-500 per
customer**, competitive with but not clearly better than Zomato's ~Rs 500-600, despite Swiggy
operating as a multi-service "super app" that in theory should lower acquisition costs through
cross-service conversion.

At the same time, Swiggy has been public about the strategic response: its loyalty program,
**Swiggy One**, had over 5 million active subscribers as of FY2025, with management reporting
it lifted subscriber ARPU to roughly Rs 1,200/year and **cut churn by an estimated 20% versus
non-subscribers**. Swiggy has also publicized that high-visibility sponsorships (e.g. its 2025
IPL cricket sponsorship) **cut CAC by roughly 18%** while driving 1.4 million net new app
installs.

Put together, this is a real, current strategic question every quick-commerce operator in this
market is facing: **acquisition is getting structurally more expensive, and the public signal
from the market leader is a pivot toward retention and loyalty rather than pure acquisition
spend.**

## The business question this project answers

> Using marketing interaction and CRM data, does Swiggy One membership measurably reduce
> customer acquisition cost and improve retention — and if so, by how much, and which
> acquisition channels and customer segments should get budget priority?

This is the exact kind of question a strategy/analytics team (internal or a consulting
engagement) would be asked to answer with data, and it's why this project builds:
1. A **CRM data-quality pipeline** first (real CRM data would need this before any of the above
   could be trusted),
2. A **CAC and retention comparison by membership status** (the core question),
3. A **channel- and campaign-level CAC breakdown** (where to reallocate acquisition budget),
4. An **RFM customer segmentation** (who to target for win-back and Swiggy One upsell), and
5. A **dashboard and executive memo** that state the recommendation in one page, the way a
   consulting team would hand it to a client.

## Sources
- Swiggy Q3 FY25 Earnings Conference Call transcript (Feb 5, 2025), swiggy.com/corporate
- "Swiggy Earnings Call: Increased customer acquisition costs..." — MediaNama, Feb 2025
- "Swiggy's IPO Decoded" — Medium (Ashish Paikray), Nov 2024 (CAC benchmark figures)
- "Marketing Mix Analysis of Swiggy" — businessmodelcanvastemplate.com (Swiggy One ARPU/churn,
  IPL sponsorship CAC-reduction figures)
- "Swiggy Digital Marketing Strategies 2025" — digitalmarketacademy.in

All figures attributed to Swiggy above are as publicly reported by these sources at the time of
writing; treat them as directional, not audited financial figures.
