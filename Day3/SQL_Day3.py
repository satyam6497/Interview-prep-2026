import os
import sqlite3
import pandas as pd

# Lock paths to the exact folder containing SQL_Day3.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "olist.db")

files_to_tables = {
    "olist_orders_dataset.csv": "orders",
    "olist_customers_dataset.csv": "customers",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
}

conn = sqlite3.connect(DB_PATH)

# Check if data directory actually exists before running
# if not os.path.exists(DATA_DIR):
#     print(f"ERROR: Could not find folder at: {DATA_DIR}")
#     print("Please make sure your 'data' folder is placed directly inside 'Day 3'.")
# else:
#     for filename, table_name in files_to_tables.items():
#         path = os.path.join(DATA_DIR, filename)
#         if not os.path.exists(path):
#             print(f"SKIPPED (not found): {path}")
#             continue
#         df = pd.read_csv(path)
#         df.to_sql(table_name, conn, if_exists="replace", index=False)
#         print(f"Loaded {table_name}: {df.shape}")
    

# --- 1. BASIC MULTI-TABLE JOIN (with customer_state corrected) ---
query1 = """
WITH order_payments_summary AS (
    SELECT 
        order_id,
        SUM(payment_value) AS total_payment_value
    FROM payments
    GROUP BY order_id
)
SELECT 
    o.order_id,
    c.customer_state,
    o.order_status,
    p.total_payment_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_payments_summary p ON o.order_id = p.order_id;
"""

# print("\n--- Query 1 Output ---")
# print(pd.read_sql_query(query1, conn).head())





# -- 2. THE customer_id vs customer_unique_id CHECK (same trap as your Python exercise)
# -- Using a CTE, count orders per customer_unique_id. Then write the outer query to show:
# -- how many unique customers have more than 1 order (repeat customers), in SQL this time.
query2 = '''
WITH customer_orders AS (
    SELECT 
        c.customer_unique_id,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT 
    customer_unique_id,
    order_count
FROM customer_orders
WHERE order_count > 1
ORDER BY order_count DESC;
'''
# print("\n--- Query 2 Output ---")
# print(pd.read_sql_query(query2, conn).head())

# -- 3. ON-TIME DELIVERY RATE BY STATE
# -- Using a CTE, flag each delivered order as on-time or late
# -- (order_delivered_customer_date <= order_estimated_delivery_date).
# -- Then in the outer query, calculate % on-time per customer_state, only for states
# -- with at least 50 delivered orders .
query3 = '''
WITH delivery AS (
    SELECT 
        o.order_id,
        o.customer_id,
        o.order_status,
        CASE 
            WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1.0
            ELSE 0.0
        END AS is_on_time
    FROM orders o
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
)
SELECT 
    c.customer_state,
    COUNT(d.order_id) AS total_delivered_orders,
    ROUND(AVG(d.is_on_time) * 100.0, 2) AS on_time_rate_pct
FROM delivery d
JOIN customers c ON d.customer_id = c.customer_id
GROUP BY c.customer_state
HAVING COUNT(d.order_id) >= 50
ORDER BY on_time_rate_pct DESC;
'''
# print("\n ---- Output 3 ----")
# print(pd.read_sql_query(query3, conn).head())

# -- 4. TOP PRODUCT CATEGORIES BY REVENUE
# -- Join order_items -> products -> orders, calculate total revenue 
# -- per product_category_name. Show top 10, only for 'delivered' orders.
query4 = '''
SELECT p.product_category_name,  (oi.price + oi.freight_value) as total_value 
FROM order_items as oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
GROUP by p.product_category_name
HAVING o.order_status = 'delivered'
ORDER BY total_value DESC;
'''
# print("\n ---- Output 4 ----")
# print(pd.read_sql_query(query4, conn).head(10))

# -- 5. AVERAGE REVIEW SCORE BY DELIVERY SPEED (a real, interview-worthy insight)
# -- Using a CTE: calculate delivery_days = order_delivered_customer_date - order_purchase_timestamp
# -- for each order. In the outer query: join to reviews, bucket delivery_days into
# -- ranges (e.g. 0-5 days, 6-10, 11-20, 20+), and show AVERAGE review_score per bucket.
# -- Hypothesis to test: does slower delivery correlate with worse reviews?
query5 = '''
WITH delivery_times AS (
    SELECT 
        order_id,
        -- Calculate fractional day difference and round to an integer
        CAST(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) AS INTEGER) AS delivery_days
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
),
bucket_delivery_dates AS (
    SELECT 
    order_id,
    delivery_days,
    CASE 
        WHEN delivery_days <= 5 THEN '0-5 days'
        WHEN delivery_days <= 10 THEN '6-10 days'
        WHEN delivery_days <= 20 THEN '11-20 days'
        ELSE '20+ days'
    END AS delivery_bucket
    FROM delivery_times
)
SELECT d.delivery_bucket, ROUND(AVG(r.review_score),2) as average_review
FROM bucket_delivery_dates d
JOIN reviews r ON d.order_id = r.order_id
GROUP BY delivery_bucket;
'''
# print("\n ---- Output 5 ----")
# print(pd.read_sql_query(query5, conn).head())

# -- 6. FUNNEL-STYLE: ORDER STATUS BREAKDOWN BY SELLER (mirrors GoodSpace funnel logic)
# -- For each seller_id (via order_items), calculate: total orders, delivered orders,
# -- cancelled orders, and % delivered. Only show sellers with 20+ orders (HAVING).
# -- This is your GoodSpace funnel query pattern applied to a completely different entity (sellers, not channels) -
# -- prove to yourself you can adapt the pattern, not just recite it.

query6 = """
WITH seller_order_pairs AS (
    -- Deduplicate to (seller_id, order_id) because an order can have multiple items from the same seller
    SELECT DISTINCT
        oi.seller_id,
        oi.order_id,
        o.order_status
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
)
SELECT 
    seller_id,
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(100.0 * SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) / COUNT(order_id), 2) AS delivered_pct
FROM seller_order_pairs
GROUP BY seller_id
HAVING COUNT(order_id) >= 20
ORDER BY total_orders DESC;
"""

# print("\n--- Output 6 ---")
# print(pd.read_sql_query(query6, conn).head(10))

# -- 7. CTE CHAINING (multi-step CTE, real interview pattern)
# -- Build this in THREE chained CTEs:
# --   CTE 1: order-level total value (sum from order_items)
# --   CTE 2: customer-level total spend (sum of CTE 1, grouped by customer_unique_id)
# --   CTE 3 / final query: rank customers by total spend using RANK(), show top 20
query7 = """
WITH order_values AS (
    -- CTE 1: Order-level total value (price + freight_value)
    SELECT 
        order_id,
        SUM(price + freight_value) AS order_total_value
    FROM order_items
    GROUP BY order_id
),
customer_spend AS (
    -- CTE 2: Customer-level total spend aggregated by customer_unique_id
    SELECT 
        c.customer_unique_id,
        SUM(ov.order_total_value) AS total_spend,
        COUNT(ov.order_id) AS total_orders
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_values ov ON o.order_id = ov.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
customer_ranks AS (
    -- CTE 3: Rank customers by total spend using RANK() window function
    SELECT 
        customer_unique_id,
        total_orders,
        ROUND(total_spend, 2) AS total_spend,
        RANK() OVER (ORDER BY total_spend DESC) AS spend_rank
    FROM customer_spend
)
-- Final Query: Retrieve the Top 20 ranked spenders
SELECT 
    spend_rank,
    customer_unique_id,
    total_orders,
    total_spend
FROM customer_ranks
WHERE spend_rank <= 20
ORDER BY spend_rank ASC;
"""

print("\n--- Output 7 ---")
print(pd.read_sql_query(query7, conn))



conn.close()
# print(f"\nDone. Database saved as {DB_PATH}")
