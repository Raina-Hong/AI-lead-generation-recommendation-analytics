
-- SQL Business Analysis Queries
-- Project: AI-Powered Lead Generation & Recommendation Analytics Platform

-- 1. Overall KPI Summary
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT product_id) AS unique_products,
    COUNT(DISTINCT seller_id) AS unique_sellers,
    ROUND(SUM(gmv), 2) AS total_gmv,
    ROUND(AVG(gmv), 2) AS avg_order_value,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM orders
WHERE order_status = 'delivered';

-- 2. Monthly GMV Trend
SELECT
    order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_users,
    ROUND(SUM(gmv), 2) AS total_gmv,
    ROUND(AVG(gmv), 2) AS avg_order_value
FROM orders
WHERE order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;

-- 3. Category Performance
SELECT
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT seller_id) AS unique_sellers,
    ROUND(SUM(gmv), 2) AS total_gmv,
    ROUND(AVG(gmv), 2) AS avg_order_value,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM orders
WHERE order_status = 'delivered'
GROUP BY category
HAVING COUNT(DISTINCT order_id) >= 50
ORDER BY total_gmv DESC;

-- 4. Top Sellers by GMV
SELECT
    seller_id,
    seller_city,
    seller_state,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_buyers,
    ROUND(SUM(gmv), 2) AS total_gmv,
    ROUND(AVG(gmv), 2) AS avg_order_value,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM orders
WHERE order_status = 'delivered'
GROUP BY seller_id, seller_city, seller_state
HAVING COUNT(DISTINCT order_id) >= 20
ORDER BY total_gmv DESC
LIMIT 20;

-- 5. Payment Method Analysis
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_users,
    ROUND(SUM(gmv), 2) AS total_gmv,
    ROUND(AVG(gmv), 2) AS avg_order_value,
    ROUND(AVG(payment_installments), 2) AS avg_installments,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM orders
WHERE order_status = 'delivered'
  AND payment_type IS NOT NULL
GROUP BY payment_type
ORDER BY total_gmv DESC;

-- 6. Delivery Delay Impact
SELECT
    late_delivery_flag,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay_days,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS negative_review_rate
FROM orders
WHERE order_status = 'delivered'
  AND delivery_delay_days IS NOT NULL
GROUP BY late_delivery_flag
ORDER BY late_delivery_flag;
