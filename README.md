# Interview Prep 2026 — SQL, Python & Power BI Practice Log

A daily practice log built over 6 days to prepare for **Data Analyst interviews**.

Each day covers the same three core skills — **SQL, Python, and Power BI** — applied to a consistent synthetic e-commerce dataset containing orders and customers. The goal is to solve the same business problems (funnel conversion, customer segmentation, retention, etc.) in three different ways.

## Why This Exists

Rather than practicing SQL, Python, and Power BI in isolation, this repository tracks how the **same analytical problems can be solved across all three tools** — similar to how a real Data Analyst works.

The practice is built around problems that mirror:

* My professional experience at **GoodSpace AI**, particularly recruiter funnel analysis and reporting
* My existing projects involving **RFM segmentation**
* **E-commerce order and customer behavior analysis**
* Common Data Analyst interview questions involving SQL, Python, and Power BI

The focus is on developing **analytical thinking and tool versatility**, rather than simply memorizing syntax.

## Repository Structure

```text
interview-prep-2026/
│
├── day1/
│   ├── sql_practice_day1.sql
│   │   └── Joins, aggregation, subqueries, funnel queries
│   │
│   ├── rfm_starter.py
│   │   └── RFM segmentation rebuilt from scratch in Pandas
│   │
│   └── powerbi_dashboard.pbix
│       └── Order fulfillment & customer behavior dashboard
│
├── day2/
│   ├── sql_practice_day2_window_functions.sql
│   │   └── Window functions: ROW_NUMBER, RANK/DENSE_RANK, LAG/LEAD, running totals, NTILE
│   │
│   ├── python_day2_starter.py
│   │   └── Cohort/retention analysis, funnel math in Pandas (cross-checked against SQL)
│   │
│   └── powerbi_time_intelligence.pbix
│       └── Date table + YTD/MoM measures, matrix by month x channel
│
├── day3/
│   ├── build_olist_db.py
│   │   └── Loads real Olist Kaggle CSVs into a queryable SQLite DB
│   │
│   ├── sql_practice_day3_olist.sql
│   │   └── Multi-table CTEs on real data: repeat customers, on-time delivery by state,
│   │       delivery speed vs review score, seller-level funnel
│   │
│   ├── python_day3_olist_starter.py
│   │   └── Delivery performance, repeat customer rate (customer_id vs customer_unique_id
│   │       data quality catch), revenue analysis, geography insights
│   │
│   └── powerbi_olist_dashboard.pbix
│       └── Repeat Customer %, review score by delivery bucket, on-time % by state,
│           top categories by revenue — built on real Olist data
│
├── data/
│   ├── practice_orders_with_status.csv       # synthetic dataset, days 1-2
│   ├── practice_customers.csv                # synthetic dataset, days 1-2
│   └── olist/                                # NOT committed — see note below
│
└── README.md
```

## Dataset

All exercises use the same **synthetic e-commerce dataset** consisting of:

* **846 orders**
* **300 customers**
* Varied acquisition channels
* Realistic customer purchase frequency
* Order statuses including:

  * Delivered
  * Cancelled
  * Returned

The dataset is intentionally designed to have realistic patterns, including a small number of high-frequency customers, varied acquisition sources, and different order outcomes — similar to the structure of real-world **product, growth, and e-commerce analytics data**.

Using the same dataset across multiple tools makes it possible to compare how the same business question can be approached using SQL, Python, and Power BI.

## Skills Covered

### SQL

* Joins
* Aggregations
* `GROUP BY` and `HAVING`
* Subqueries
* Common Table Expressions (CTEs)
* Window functions
* Funnel analysis
* Conversion-rate calculations
* Customer and order analysis

### Python

* Pandas
* Data cleaning and transformation
* RFM segmentation
* Cohort analysis
* Retention analysis
* Funnel calculations
* Correlation analysis
* Customer-level analysis
* Business insight generation

### Power BI

* Data modeling
* Power Query
* DAX
* Measures
* Calculated columns
* Time intelligence
* KPI analysis
* Interactive dashboards
* Customer and order behavior analysis

## Related Work

**E-commerce Order Fulfillment & Customer Behavior Analysis**
A full project referenced on my resume, focused on analyzing order fulfillment, customer behavior, and business performance using SQL, Python, and Power BI.

**Professional Experience — Data Analyst @ GoodSpace AI (Mar–Aug 2025)**

Worked on:

* Recruiter funnel analysis
* Power BI dashboards
* User engagement and platform KPIs
* Automated reporting using SQL and Python
* Analysis of behavioral patterns across 22,000+ user records

## Practice Philosophy

The goal of this repository is not to create a polished production project.

Instead, it documents **active interview preparation and daily analytical practice**.

The same business problem is intentionally approached from multiple perspectives:

```text
Business Problem
       │
       ├── SQL
       │
       ├── Python / Pandas
       │
       └── Power BI / DAX
```

This helps strengthen both **technical execution** and the ability to translate a business question into an analytical solution.

## Progress

This repository is actively being updated as part of a focused **6-day interview preparation sprint**.

Each day's commits represent the problems solved, concepts practiced, and insights generated during that day's preparation.

---

**Focus:** SQL • Python • Power BI • Business Analytics
**Goal:** Become faster and more confident at solving real-world Data Analyst interview problems.
