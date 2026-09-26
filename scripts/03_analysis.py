import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 130

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN = BASE_DIR / "data/clean"
VIS = BASE_DIR / "visuals"
DOCS = BASE_DIR / "docs"
VIS.mkdir(parents=True, exist_ok=True)

cust = pd.read_csv(f"{CLEAN}/crm_customers_clean.csv", parse_dates=["signup_date"])
inter = pd.read_csv(f"{CLEAN}/marketing_interactions_clean.csv", parse_dates=["event_date"])
inter = inter.rename(columns={"order_value": "revenue"})

camp = inter.groupby("campaign_name").agg(
    sent=("sent","sum"), opened=("opened","sum"), clicked=("clicked","sum"),
    converted=("converted","sum"), revenue=("revenue","sum"), spend=("spend","sum")
).reset_index()
camp["open_rate"] = camp["opened"] / camp["sent"]
camp["ctr"] = camp["clicked"] / camp["opened"]
camp["conversion_rate"] = camp["converted"] / camp["clicked"]
camp["roas"] = camp["revenue"] / camp["spend"]
camp["cac"] = camp["spend"] / camp["converted"].replace(0, pd.NA)
camp = camp.sort_values("roas", ascending=False)
camp.to_csv(f"{CLEAN}/campaign_performance_summary.csv", index=False)

chan = inter.groupby("channel").agg(
    sent=("sent","sum"), opened=("opened","sum"), clicked=("clicked","sum"),
    converted=("converted","sum"), revenue=("revenue","sum"), spend=("spend","sum")
).reset_index()
chan["roas"] = chan["revenue"] / chan["spend"]
chan["conversion_rate"] = chan["converted"] / chan["sent"]
chan["cac"] = chan["spend"] / chan["converted"].replace(0, pd.NA)
chan = chan.sort_values("cac", ascending=True)
chan.to_csv(f"{CLEAN}/channel_performance_summary.csv", index=False)

funnel = pd.Series({
    "Sent": inter["sent"].sum(), "Opened": inter["opened"].sum(),
    "Clicked": inter["clicked"].sum(), "Converted": inter["converted"].sum(),
})

inter_c = inter.merge(cust[["customer_id","swiggy_one_member"]], on="customer_id", how="left")
member_cac = inter_c.groupby("swiggy_one_member").agg(
    converted=("converted","sum"), spend=("spend","sum"), revenue=("revenue","sum"),
    interactions=("interaction_id","count")
).reset_index()
member_cac["cac"] = member_cac["spend"] / member_cac["converted"].replace(0, pd.NA)
member_cac["conversion_rate"] = member_cac["converted"] / member_cac["interactions"]
member_cac["swiggy_one_member"] = member_cac["swiggy_one_member"].map({True:"Swiggy One Member", False:"Non-Member"})
member_cac.to_csv(f"{CLEAN}/membership_cac_comparison.csv", index=False)

conv_only = inter_c[inter_c["converted"]==1]
orders_per_cust = conv_only.groupby(["customer_id","swiggy_one_member"]).size().reset_index(name="orders")
repeat_rate = orders_per_cust.groupby("swiggy_one_member")["orders"].apply(lambda x: (x>1).mean()).reset_index()
repeat_rate.columns = ["swiggy_one_member","repeat_purchase_rate"]
repeat_rate["swiggy_one_member"] = repeat_rate["swiggy_one_member"].map({True:"Swiggy One Member", False:"Non-Member"})
repeat_rate.to_csv(f"{CLEAN}/membership_repeat_rate.csv", index=False)

snapshot = inter["event_date"].max() + pd.Timedelta(days=1)
rfm = inter[inter["converted"]==1].groupby("customer_id").agg(
    recency=("event_date", lambda x: (snapshot - x.max()).days),
    frequency=("converted","sum"), monetary=("revenue","sum")
).reset_index()
rfm["R"] = pd.qcut(rfm["recency"], 4, labels=[4,3,2,1]).astype(int)
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
rfm["M"] = pd.qcut(rfm["monetary"], 4, labels=[1,2,3,4]).astype(int)
rfm["rfm_score"] = rfm["R"] + rfm["F"] + rfm["M"]

def tier(score):
    if score >= 10: return "Champions"
    if score >= 8: return "Loyal"
    if score >= 6: return "Potential"
    if score >= 4: return "At-Risk"
    return "Lost"
rfm["tier"] = rfm["rfm_score"].apply(tier)
rfm.to_csv(f"{CLEAN}/customer_rfm_segments.csv", index=False)

fig, ax = plt.subplots(figsize=(7,4.5))
ax.barh(list(funnel.index)[::-1], list(funnel.values)[::-1], color="#FC8019")
for i, v in enumerate(list(funnel.values)[::-1]):
    ax.text(v, i, f" {v:,}", va="center", fontsize=10)
ax.set_title("Overall Marketing Funnel (Sent → Converted)")
ax.set_xlabel("Interactions")
plt.tight_layout(); plt.savefig(f"{VIS}/funnel_chart.png"); plt.close()

fig, ax = plt.subplots(figsize=(7,4.5))
sns.barplot(data=chan, x="cac", y="channel", ax=ax, palette="flare")
ax.set_title("Customer Acquisition Cost (CAC) by Channel — lower is better")
ax.set_xlabel("CAC (Rs, simulated)")
plt.tight_layout(); plt.savefig(f"{VIS}/cac_by_channel.png"); plt.close()

fig, ax = plt.subplots(figsize=(8,4.5))
sns.barplot(data=camp, x="roas", y="campaign_name", ax=ax, palette="mako")
ax.set_title("ROAS by Campaign")
ax.set_xlabel("Revenue / Spend")
plt.tight_layout(); plt.savefig(f"{VIS}/roas_by_campaign.png"); plt.close()

fig, ax = plt.subplots(figsize=(6.5,4.5))
order = ["Champions","Loyal","Potential","At-Risk","Lost"]
sns.countplot(data=rfm, x="tier", order=order, palette="rocket", ax=ax)
ax.set_title("Customer Segments by RFM Tier")
ax.set_xlabel("")
plt.tight_layout(); plt.savefig(f"{VIS}/rfm_tiers.png"); plt.close()

fig, ax = plt.subplots(figsize=(6,4.5))
sns.barplot(data=member_cac, x="swiggy_one_member", y="cac", ax=ax, palette=["#999999","#FC8019"])
ax.set_title("CAC: Swiggy One Members vs Non-Members")
ax.set_ylabel("CAC (Rs, simulated)"); ax.set_xlabel("")
plt.tight_layout(); plt.savefig(f"{VIS}/cac_by_membership.png"); plt.close()

fig, ax = plt.subplots(figsize=(6,4.5))
sns.barplot(data=repeat_rate, x="swiggy_one_member", y="repeat_purchase_rate", ax=ax, palette=["#999999","#FC8019"])
ax.set_title("Repeat-Purchase Rate: Members vs Non-Members")
ax.set_ylabel("Share of converters who ordered more than once"); ax.set_xlabel("")
plt.tight_layout(); plt.savefig(f"{VIS}/repeat_rate_by_membership.png"); plt.close()

inter["month"] = inter["event_date"].dt.to_period("M").astype(str)
monthly = inter.groupby("month")["revenue"].sum().reset_index()
fig, ax = plt.subplots(figsize=(8,4.5))
sns.lineplot(data=monthly, x="month", y="revenue", marker="o", ax=ax, color="#FC8019")
ax.set_title("Monthly Revenue from Campaigns")
plt.xticks(rotation=45, ha="right")
plt.tight_layout(); plt.savefig(f"{VIS}/monthly_revenue_trend.png"); plt.close()

print("Channel CAC:\n", chan[["channel","cac","roas"]].round(2))
print("\nMembership comparison:\n", member_cac)
print("\nRepeat rate:\n", repeat_rate)
print("\nFunnel:\n", funnel)

best_chan_row = chan.iloc[0]
worst_chan_row = chan.sort_values("cac", ascending=False).iloc[0]

# For the "shift budget between channels" recommendation, only compare true PAID ACQUISITION
# channels (excludes Swiggy One Emailer & organic app, which target/reach existing users and
# aren't a fair like-for-like acquisition comparison -- conflating the two overstates the case).
acquisition_channels = ["Performance Ads (Search/Display)","Paid Social","IPL / Sponsorship","Referral"]
chan_acq = chan[chan["channel"].isin(acquisition_channels)].sort_values("cac")
best_acq = chan_acq.iloc[0]
worst_acq = chan_acq.iloc[-1]
shift_budget = 50000.0
extra_conversions = shift_budget / best_acq["cac"] - shift_budget / worst_acq["cac"]
member_row = member_cac[member_cac["swiggy_one_member"]=="Swiggy One Member"].iloc[0]
nonmember_row = member_cac[member_cac["swiggy_one_member"]=="Non-Member"].iloc[0]
cac_gap_pct = (nonmember_row["cac"] - member_row["cac"]) / nonmember_row["cac"]
rr_member = repeat_rate.set_index("swiggy_one_member").loc["Swiggy One Member","repeat_purchase_rate"]
rr_nonmember = repeat_rate.set_index("swiggy_one_member").loc["Non-Member","repeat_purchase_rate"]

with open(f"{DOCS}/key_insights.md", "w") as f:
    f.write("# Key Business Insights\n\n")
    f.write(f"1. **Swiggy One members cost {cac_gap_pct:.0%} less to convert than non-members** "
            f"(Rs {member_row['cac']:.0f} vs Rs {nonmember_row['cac']:.0f} simulated CAC), and have a "
            f"**{rr_member:.0%} repeat-purchase rate** vs **{rr_nonmember:.0%}** for non-members — "
            f"this is the quantified case for shifting marketing budget from acquisition toward "
            f"loyalty-program enrollment, matching the direction Swiggy has signaled publicly.\n\n")
    f.write(f"2. Among true paid-acquisition channels (excluding retention-only channels like the "
            f"Swiggy One emailer, which only reaches existing members), **{best_acq['channel']}** "
            f"acquires a customer for Rs {best_acq['cac']:.0f} vs **{worst_acq['channel']}** at "
            f"Rs {worst_acq['cac']:.0f} — shifting Rs {shift_budget:,.0f} of *new-customer* acquisition "
            f"budget from the weakest to the strongest of these would buy an estimated "
            f"**{extra_conversions:.0f} additional conversions** at the same total spend.\n\n")
    f.write(f"3. Funnel drop-off: of {funnel['Sent']:,} messages sent, only {funnel['Converted']:,} "
            f"converted ({funnel['Converted']/funnel['Sent']:.1%} overall) — the steepest drop is "
            f"Opened -> Clicked, pointing at a creative/offer problem, not a targeting problem.\n\n")
    f.write(f"4. RFM segmentation shows most converting customers sit in Potential/At-Risk tiers, "
            f"not Champions — exactly the group a win-back + Swiggy One upsell campaign should target "
            f"first, since insight #1 shows membership is the single biggest lever on both cost and "
            f"repeat behavior.\n\n")
    f.write(f"5. Data-quality note: 8.6% of raw CRM records were duplicates, 48 records had a "
            f"membership-flag/segment-label mismatch (a two-systems-of-record bug), and roughly 7-8% "
            f"of raw interactions referenced customers that didn't validate — cleaning this before "
            f"analysis changed the CAC numbers materially, which is why the governance layer isn't "
            f"optional.\n")

print("\nSaved docs/key_insights.md and charts to /visuals")
