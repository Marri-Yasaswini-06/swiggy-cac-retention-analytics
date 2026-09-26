"""
SIMULATED data for a case study modeled on Swiggy Instamart's publicly disclosed problem
(rising customer acquisition cost, competitive pressure from Blinkit/Zomato, strategic pivot
to retention via the Swiggy One loyalty program). This is NOT real Swiggy data -- Swiggy's
actual CRM/order data is private. The data below is synthetic, but its scale and benchmarks
(CAC ~Rs 400-500, Swiggy One ARPU ~Rs 1,200/yr, ~20% lower churn for members) are calibrated
to match numbers Swiggy has disclosed publicly (earnings calls, investor decks, published
case studies) -- see docs/problem_statement.md for sources. It is DELIBERATELY messy so the
data-quality / governance work in this project is real, not decorative.
"""
import random
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent  # project root, regardless of where this is run from
(BASE_DIR / "data/raw").mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)

N_CUSTOMERS = 6000
N_INTERACTIONS = 42000

first_names = ["Aarav","Vivaan","Aditya","Ishaan","Arjun","Reyansh","Kabir","Sai","Ayaan","Krishna",
               "Ananya","Diya","Saanvi","Aadhya","Myra","Pari","Anika","Navya","Riya","Ira",
               "Rohan","Sneha","Karthik","Priya","Rahul","Neha","Vikram","Pooja","Nikhil","Divya"]
last_names = ["Sharma","Verma","Gupta","Reddy","Iyer","Nair","Patel","Singh","Rao","Menon",
              "Khan","Das","Chatterjee","Mehta","Joshi","Kapoor","Malhotra","Bose","Pillai","Shetty"]

# Real Swiggy Instamart service cities (publicly known; used only as realistic labels)
cities = ["Bengaluru","Mumbai","Delhi","Hyderabad","Chennai","Pune","Kolkata","Gurugram",
          "Nellore","Vijayawada","Ahmedabad","Jaipur","Kochi","Noida","Lucknow"]

# Channels reflecting how Swiggy actually markets (per public case studies / earnings calls)
channels = ["Performance Ads (Search/Display)","Paid Social","Push Notification (App)",
            "Organic App / SEO","Referral","IPL / Sponsorship","Swiggy One Emailer"]

campaigns = [
    ("IPL_2025_SPONSORSHIP","IPL / Sponsorship"),("IPL_2025_SPONSORSHIP","Push Notification (App)"),
    ("SWIGGY_ONE_LAUNCH","Swiggy One Emailer"),("SWIGGY_ONE_LAUNCH","Paid Social"),
    ("INSTAMART_10MIN_PUSH","Performance Ads (Search/Display)"),("INSTAMART_10MIN_PUSH","Push Notification (App)"),
    ("FESTIVE_LAXMI_CAMPAIGN","Paid Social"),("FESTIVE_LAXMI_CAMPAIGN","Performance Ads (Search/Display)"),
    ("WINBACK_DORMANT_USERS","Push Notification (App)"),("WINBACK_DORMANT_USERS","Swiggy One Emailer"),
    ("REFERRAL_GROWTH_DRIVE","Referral"),("NEW_CITY_LAUNCH_PUSH","Organic App / SEO"),
]
segments = ["New","Frequent Orderer","Swiggy One Member","Dormant","Churned"]

def messy_phone():
    n = "".join([str(random.randint(0,9)) for _ in range(10)])
    fmt = random.choice([
        f"+91-{n[:5]}-{n[5:]}", f"{n[:5]} {n[5:]}", f"({n[:3]}) {n[3:6]}-{n[6:]}",
        n, f"91{n}", None
    ])
    return fmt

def messy_email(fn, ln):
    domains = ["gmail.com","yahoo.com","outlook.com","gmail.co","hotmail.com"]
    base = f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@{random.choice(domains)}"
    if random.random() < 0.03:
        base = base.upper()
    return base

rows = []
customer_pool = []
for i in range(N_CUSTOMERS):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    cust_id = f"SWGY{10000+i}"
    city = random.choice(cities)
    signup = datetime(2023,6,1) + timedelta(days=random.randint(0, 730))
    segment = random.choices(segments, weights=[22,30,18,20,10])[0]
    is_one_member = segment == "Swiggy One Member" or random.random() < 0.12
    # inject a real CRM sync bug: ~4% of records have a stale/contradictory membership flag
    # relative to their segment label (two systems of record disagreeing)
    if random.random() < 0.04:
        is_one_member = not is_one_member
    rec = {
        "customer_id": cust_id,
        "full_name": f"{fn} {ln}",
        "email": messy_email(fn, ln),
        "phone": messy_phone(),
        "city": random.choice([city, city.upper(), city.lower(), f" {city} "]),
        "signup_date": signup.strftime(random.choice(["%Y-%m-%d","%d/%m/%Y","%m-%d-%Y"])),
        "segment": segment,
        "swiggy_one_member": is_one_member,
        "marketing_opt_in": random.choice(["Yes","No","Y","N","yes","1","0", None]),
    }
    customer_pool.append((cust_id, fn, ln, segment, signup, is_one_member))
    rows.append(rec)

for _ in range(int(N_CUSTOMERS * 0.04)):
    base = random.choice(rows).copy()
    base["customer_id"] = f"SWGY{10000+random.randint(0,N_CUSTOMERS-1)}X"
    base["full_name"] = base["full_name"].upper() if random.random()<0.5 else base["full_name"] + " "
    rows.append(base)

customers_df = pd.DataFrame(rows)

for col in ["email","phone","city","segment"]:
    idx = customers_df.sample(frac=0.05, random_state=random.randint(1,999)).index
    customers_df.loc[idx, col] = None

customers_df.to_csv(BASE_DIR / "data/raw/crm_customers_raw.csv", index=False)

interactions = []
for i in range(N_INTERACTIONS):
    cust_id, fn, ln, segment, signup, is_one_member = random.choice(customer_pool)
    campaign, channel = random.choice(campaigns)
    event_date = signup + timedelta(days=random.randint(0, 600))
    if event_date > datetime(2025,6,30):
        event_date = datetime(2025,6,30) - timedelta(days=random.randint(0,30))

    member_boost = 1.35 if is_one_member else 1.0
    ipl_boost = 1.18 if campaign == "IPL_2025_SPONSORSHIP" else 1.0

    sent = 1
    opened = 1 if random.random() < 0.50 * member_boost else 0
    clicked = 1 if (opened and random.random() < 0.35 * member_boost) else 0
    converted = 1 if (clicked and random.random() < 0.20 * member_boost * ipl_boost) else 0
    order_value = round(np.random.gamma(2, 95) * (1 if converted else 0), 2) if converted else 0.0

    base_spend = {
        "Performance Ads (Search/Display)": 5.2, "Paid Social": 4.6, "Push Notification (App)": 0.4,
        "Organic App / SEO": 0.6, "Referral": 1.8, "IPL / Sponsorship": 3.1, "Swiggy One Emailer": 0.3
    }[channel]
    spend = round(base_spend * random.uniform(0.7, 1.3), 2)

    interactions.append({
        "interaction_id": f"INT{100000+i}",
        "customer_id": cust_id,
        "campaign_name": campaign,
        "channel": channel,
        "event_date": event_date.strftime("%Y-%m-%d"),
        "sent": sent,
        "opened": opened,
        "clicked": clicked,
        "converted": converted,
        "order_value": order_value,
        "spend": spend,
    })

interactions_df = pd.DataFrame(interactions)
dupes = interactions_df.sample(frac=0.015, random_state=7)
interactions_df = pd.concat([interactions_df, dupes], ignore_index=True)

interactions_df.to_csv(BASE_DIR / "data/raw/marketing_interactions_raw.csv", index=False)

print("customers_raw:", customers_df.shape)
print("interactions_raw:", interactions_df.shape)
