-- ============================================================================
-- Swiggy Instamart CAC & Retention Analytics — SQL Analysis
-- Run against database/swiggy_analytics.db (SQLite; standard ANSI SQL, would
-- run unchanged on PostgreSQL/MySQL with trivial syntax tweaks noted inline).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. THE CORE BUSINESS QUESTION: CAC and conversion rate, members vs non-members
-- ----------------------------------------------------------------------------
SELECT
    CASE WHEN c.swiggy_one_member = 1 THEN 'Swiggy One Member' ELSE 'Non-Member' END AS segment,
    COUNT(*)                                    AS total_interactions,
    SUM(i.converted)                            AS total_conversions,
    ROUND(SUM(i.spend), 2)                      AS total_spend,
    ROUND(SUM(i.spend) * 1.0 / NULLIF(SUM(i.converted), 0), 2) AS cac,
    ROUND(SUM(i.converted) * 1.0 / COUNT(*), 4) AS conversion_rate
FROM interactions i
JOIN customers c ON i.customer_id = c.customer_id
GROUP BY c.swiggy_one_member
ORDER BY cac;

-- ----------------------------------------------------------------------------
-- 2. Funnel: Sent -> Opened -> Clicked -> Converted
-- ----------------------------------------------------------------------------
SELECT
    SUM(sent)      AS sent,
    SUM(opened)    AS opened,
    SUM(clicked)   AS clicked,
    SUM(converted) AS converted,
    ROUND(SUM(opened) * 1.0 / NULLIF(SUM(sent), 0), 4)    AS open_rate,
    ROUND(SUM(clicked) * 1.0 / NULLIF(SUM(opened), 0), 4) AS click_through_rate,
    ROUND(SUM(converted) * 1.0 / NULLIF(SUM(clicked), 0), 4) AS conversion_rate
FROM interactions;

-- ----------------------------------------------------------------------------
-- 3. CAC by channel, split into acquisition vs retention channel type
--    (CASE/WHEN classification -- keeps the two from being compared unfairly,
--    same reasoning documented in docs/key_insights.md)
-- ----------------------------------------------------------------------------
SELECT
    channel,
    CASE
        WHEN channel IN ('Swiggy One Emailer', 'Push Notification (App)') THEN 'Retention'
        ELSE 'Acquisition'
    END AS channel_type,
    SUM(converted)                                           AS conversions,
    ROUND(SUM(spend), 2)                                     AS total_spend,
    ROUND(SUM(spend) * 1.0 / NULLIF(SUM(converted), 0), 2)   AS cac,
    ROUND(SUM(order_value) * 1.0 / NULLIF(SUM(spend), 0), 2) AS roas
FROM interactions
GROUP BY channel
ORDER BY cac;

-- ----------------------------------------------------------------------------
-- 4. Campaign performance ranked by ROAS
-- ----------------------------------------------------------------------------
SELECT
    campaign_name,
    SUM(converted) AS conversions,
    ROUND(SUM(order_value), 2) AS revenue,
    ROUND(SUM(spend), 2)       AS spend,
    ROUND(SUM(order_value) * 1.0 / NULLIF(SUM(spend), 0), 2) AS roas
FROM interactions
GROUP BY campaign_name
ORDER BY roas DESC;

-- ----------------------------------------------------------------------------
-- 5. RFM segmentation using window functions (NTILE for quartile scoring)
--    -- the SQL equivalent of the pandas qcut() used in scripts/03_analysis.py
-- ----------------------------------------------------------------------------
WITH converted_orders AS (
    SELECT
        customer_id,
        MAX(event_date)     AS last_order_date,
        COUNT(*)            AS frequency,
        SUM(order_value)    AS monetary
    FROM interactions
    WHERE converted = 1
    GROUP BY customer_id
),
snapshot AS (
    SELECT MAX(event_date) AS max_date FROM interactions
),
recency_calc AS (
    SELECT
        co.customer_id,
        CAST(julianday(s.max_date) - julianday(co.last_order_date) AS INTEGER) AS recency,
        co.frequency,
        co.monetary
    FROM converted_orders co
    CROSS JOIN snapshot s
),
scored AS (
    SELECT
        customer_id,
        recency, frequency, monetary,
        -- lower recency = more recent = higher score, so invert the tile
        (5 - NTILE(4) OVER (ORDER BY recency))            AS r_score,
        NTILE(4) OVER (ORDER BY frequency)                AS f_score,
        NTILE(4) OVER (ORDER BY monetary)                 AS m_score
    FROM recency_calc
)
SELECT
    customer_id, recency, frequency, monetary,
    r_score + f_score + m_score AS rfm_score,
    CASE
        WHEN r_score + f_score + m_score >= 10 THEN 'Champions'
        WHEN r_score + f_score + m_score >= 8  THEN 'Loyal'
        WHEN r_score + f_score + m_score >= 6  THEN 'Potential'
        WHEN r_score + f_score + m_score >= 4  THEN 'At-Risk'
        ELSE 'Lost'
    END AS tier
FROM scored
ORDER BY rfm_score DESC
LIMIT 20;   -- top 20 shown here; remove LIMIT to score the full customer base

-- ----------------------------------------------------------------------------
-- 6. Referential integrity check (should return 0 rows if the CRM governance
--    pipeline did its job -- this is the SQL-side equivalent of Rule 10 in
--    scripts/02_clean_and_govern.py)
-- ----------------------------------------------------------------------------
SELECT i.interaction_id, i.customer_id
FROM interactions i
LEFT JOIN customers c ON i.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
