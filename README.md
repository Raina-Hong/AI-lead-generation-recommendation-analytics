# 🚀 AI-Powered Lead Generation & Recommendation Analytics Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-lightgrey.svg)
![DuckDB](https://img.shields.io/badge/SQL-DuckDB-yellow.svg)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)
![Tableau](https://img.shields.io/badge/BI-Tableau-blueviolet.svg)
![A/B Testing](https://img.shields.io/badge/Experiment-A%2FB%20Testing-green.svg)

> **TL;DR:** I built an end-to-end lead generation and recommendation analytics workflow on **96K+ e-commerce orders** from the Olist public dataset. The project combines transaction analysis, a synthetic behavioural event pipeline, rule-based intent classification, lead scoring automation, recommendation ranking, and Tableau dashboards. In the simulated experiment, the intent-aware recommendation strategy delivered a **+44.9% incremental lift in Revenue per User** and a **+31.4% increase in Purchase Rate** compared with a popularity-based baseline.

📚 **[Read the Full Project Report](report/project_report.md)** | 📊 **[View Interactive Tableau Dashboards](dashboard/tableau_links.md)** | 📖 **[Data Dictionary](report/data_dictionary.md)** | 📂 **[Browse Notebooks](notebook/)**

---

## Project Overview

This project explores how an e-commerce marketplace can identify high-intent customers and recommend products more effectively than a simple popularity-based strategy.

The raw Olist dataset provides historical transactions, customer reviews, delivery information, products, sellers, and payments. To turn these static transaction records into a fuller product analytics workflow, I designed a **business-driven synthetic event pipeline** that reconstructs user engagement stages such as view, click, add-to-cart, inquiry, and purchase. This makes it possible to analyse the customer funnel, generate lead quality signals, and evaluate recommendation strategies in a structured way.

The final workflow connects four layers:

1. **Marketplace performance analysis** using Python and DuckDB SQL;
2. **Synthetic event engineering** to create full-funnel behavioural signals;
3. **Intent and lead scoring logic** to identify high-priority customers;
4. **Recommendation and experiment evaluation** to compare popularity-based and intent-aware strategies.

The project is designed for data analytics, product analytics, growth analytics, and AI product roles, especially where business teams need both technical execution and commercial interpretation.

---

## Business Problem

Small and medium-sized sellers on marketplace platforms often struggle with three practical questions:

1. Which customers are most likely to purchase?
2. Which categories, sellers, and customer segments create the strongest commercial value?
3. Can a more personalised recommendation strategy generate incremental growth beyond a basic popularity-based ranking?

This project turns those questions into an analytical workflow that connects user intent, product relevance, seller reliability, and experiment measurement.

---

## Dataset

The project uses the public **Olist Brazilian E-Commerce Dataset**. The raw data includes orders, customers, sellers, products, order items, payments, reviews, geolocation information, and product category translations.

Main raw tables used:

- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`
- `olist_geolocation_dataset.csv`

After cleaning and feature engineering, the raw tables were transformed into analytical datasets for SQL reporting, intent classification, lead scoring, recommendation evaluation, and Tableau dashboards.

---

## Project Workflow

### 1. Data Cleaning and Feature Engineering

The raw Olist tables were merged into a cleaned order-level dataset. The cleaning process included:

- standardising product categories;
- calculating GMV and average order value;
- creating delivery delay and late-delivery indicators;
- joining customer, product, seller, payment, and review information;
- preparing analytical tables for SQL analysis and downstream modelling.

### 2. SQL Business Analysis with DuckDB

I used **DuckDB** for the SQL layer because it supports fast local analytical querying without the overhead of setting up a traditional database server. This made it a good fit for portfolio-scale data engineering and repeatable business KPI generation.

The SQL analysis generated outputs for:

- overall marketplace KPIs;
- monthly GMV trends;
- top categories and sellers;
- payment method analysis;
- review score patterns;
- delivery delay impact;
- category and seller performance.

### 3. Synthetic Event Pipeline Construction

The original transaction data does not include frontend event logs, so I engineered a **synthetic event pipeline** to bridge the gap between static order records and dynamic user behaviour.

The pipeline creates five funnel stages:

- `view`
- `click`
- `add_to_cart`
- `inquiry`
- `purchase`

This is not treated as a claim of real clickstream access. Instead, it demonstrates how transaction data can be extended into a full-funnel analytics layer using transparent business assumptions. The event pipeline supports lead generation analysis, behavioural segmentation, and recommendation evaluation.

### 4. Rule-Based Intent Classification Engine

I built a transparent intent classification engine using review text, review score, delivery delay, behavioural signals, purchase value, and user segment information.

The engine assigns users to interpretable business categories such as:

- `ready_to_purchase`
- `price_sensitive`
- `delivery_concern`
- `product_quality_concern`
- `after_sales_issue`
- `general_negative`
- `comparison_shopping`
- `neutral_or_unclear`

This approach keeps the logic explainable for business stakeholders. Instead of using a black-box API, the rules make it clear why a user is classified as high-intent, price-sensitive, or delivery-concerned.

### 5. Lead Score Automation and Feature Importance Analysis

Logistic Regression and Random Forest models were used as a **proxy model for rule automation** and feature importance analysis.

The purpose of this stage is not to claim a standalone production conversion model. Since the target labels are derived from explicit business rules, the near-perfect model performance is expected. The useful result is that the machine learning pipeline can capture and automate complex business logic, which could later be converted into a real-time lead scoring service if real behavioural labels were available.

### 6. Recommendation Strategy Design

Three recommendation strategies were designed and compared:

1. **Popularity-based recommendation**  
   Recommends products mainly based on historical popularity.

2. **Category-preference recommendation**  
   Recommends products based on the user's preferred category.

3. **Intent-aware recommendation**  
   Combines user lead score, product high-intent rate, product review quality, seller review quality, and delivery reliability.

The intent-aware strategy was designed to move beyond “what is popular” and prioritise products that better match user intent and seller fulfilment quality.

### 7. Simulated AB Test Evaluation

A simulated experiment compared:

- **Control group:** popularity-based recommendation;
- **Treatment group:** intent-aware recommendation.

The evaluation measured CTR, inquiry rate, purchase rate, revenue per user, total revenue, and statistical significance.

In short: **intent-aware ranking drives deeper conversions, not just superficial clicks.**

---

## Key Results

### Marketplace Scale

| Metric | Value |
|---|---:|
| Completed Orders | **96,478** |
| Unique Users | **93,358** |
| Unique Products | **32,216** |
| Sellers | **2,970** |
| Total GMV | **BRL 15.42M** |
| Average Order Value | **BRL 139.93** |
| Average Review Score | **4.09** |

### Top GMV Categories

| Rank | Category | GMV |
|---:|---|---:|
| 1 | Health Beauty | **BRL 1.41M** |
| 2 | Watches Gifts | **BRL 1.26M** |
| 3 | Bed Bath Table | **BRL 1.23M** |
| 4 | Sports Leisure | **BRL 1.12M** |
| 5 | Computers Accessories | **BRL 1.03M** |

### Delivery Experience Impact

Delivery reliability is a clear customer experience bottleneck. Late deliveries had a much lower average review score and a much higher negative review rate.

| Delivery Group | Orders | Avg Review Score | Negative Review Rate |
|---|---:|---:|---:|
| Non-late Delivery | 89,936 | **4.21** | **11.32%** |
| Late Delivery | 6,534 | **2.33** | **61.32%** |

Business implication: recommendation ranking should not only optimise for product popularity. Seller delivery reliability should also be included as a ranking signal.

### 🏆 AB Test Results: Intent-Aware vs. Popularity Baseline

The intent-aware strategy generated statistically significant full-funnel growth.

| Metric | Control: Popularity | Treatment: Intent-Aware | Incremental Lift | Significance |
|---|---:|---:|---:|:---:|
| **CTR** | 19.42% | 22.76% | **+17.2%** | ✅ p < 0.05 |
| **Inquiry Rate** | 12.70% | 16.32% | **+28.5%** | ✅ p < 0.05 |
| **Purchase Rate** | 10.32% | 13.56% | **+31.4%** | ✅ p < 0.05 |
| **Revenue / User** | 9.10 | 13.18 | **+44.9%** | ✅ p < 0.05 |

The strongest lift appeared in revenue per user, which suggests that the treatment strategy did more than generate extra clicks. It improved deeper funnel outcomes and commercial value.

---

## Tableau Dashboards

Three Tableau dashboards were created to present the final results as stakeholder-facing outputs.

| Dashboard | Purpose | Link |
|---|---|---|
| **Dashboard 1: Executive Overview** | Marketplace KPIs, GMV trend, top categories, top sellers, and AB test uplift | [View Dashboard](https://public.tableau.com/views/AI-lead-generation-recommendation-analytics/Dashboard1ExecutiveOverviewDashboard?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) |
| **Dashboard 2: User Intent & Lead Quality** | Intent distribution, sentiment, lead score distribution, and high-intent rate by category and user segment | [View Dashboard](https://public.tableau.com/views/AI-lead-generation-recommendation-analytics/UserIntentLeadQuality?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) |
| **Dashboard 3: Recommendation AB Test Performance** | Control vs. treatment comparison, uplift metrics, purchase rate by user segment, and product diversity trade-off | [View Dashboard](https://public.tableau.com/views/AI-lead-generation-recommendation-analytics/Dashboard3RecommendationABTestPerformance?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) |

Dashboard screenshots are stored in:

```text
dashboard/tableau_screenshots/
```

All Tableau Public links are also listed in [`dashboard/tableau_links.md`](dashboard/tableau_links.md).

---

## Project Structure

```text
AI-lead-generation-recommendation-analytics/
│
├── data/
│   ├── raw/                         # Original Olist datasets
│   ├── processed/                   # Cleaned order-level dataset
│   └── final/                       # Final analytical tables
│
├── notebook/
│   ├── 01_data_understanding_and_cleaning.ipynb
│   ├── 02_sql_business_analysis.ipynb
│   ├── 03_user_funnel_analysis.ipynb
│   ├── 04_llm_intent_classification.ipynb
│   ├── 05_lead_scoring_model.ipynb
│   ├── 06_recommendation_strategy.ipynb
│   └── 07_ab_test_evaluation.ipynb
│
├── src/
│   ├── data_pipeline.py             # Reusable data cleaning and synthetic funnel generation logic
│   ├── intent_engine.py             # Intent feature extraction and lead scoring model module
│   ├── recommendation_strategy.py   # Popularity-based and intent-aware recommendation logic
│   └── utils.py                     # Shared logging and utility functions
│
├── outputs/
│   ├── tables/                      # SQL, funnel, intent, recommendation, and A/B test outputs
│   └── model_results/               # Lead scoring model metrics and feature importance
│
├── dashboard/
│   ├── tableau_screenshots/          # Tableau dashboard screenshots
│   └── tableau_links.md              # Tableau Public dashboard links
│
├── report/
│   ├── executive_summary.md
│   ├── project_report.md
│   └── data_dictionary.md
│
├── sql/
│   └── business_kpi_queries.sql
│
├── main.py                          # Lightweight entry point showing how src modules are organised
├── README.md
├── requirements.txt
└── .gitignore
```

The `notebook/` folder documents the full analytical workflow, including data exploration, SQL analysis, funnel construction, LLM-style intent classification, lead scoring, recommendation strategy design, and A/B test evaluation.

The `src/` folder contains modular Python implementations of the core pipeline components. These scripts refactor the main logic into reusable modules, including transaction cleaning, synthetic behavioural event generation, intent feature extraction, lead scoring, and recommendation ranking.

The `main.py` file acts as a lightweight project entry point. It shows how the core modules are organised, while the full reproducible analysis and output generation are maintained in the notebooks.

In this project, the notebooks demonstrate the end-to-end analytical process and generate final outputs, while the `src/` modules and `main.py` show how the same logic can be organised into a more production-style Python structure.

---

## Documentation

- [Executive Summary](report/executive_summary.md)
- [Full Project Report](report/project_report.md)
- [Data Dictionary](report/data_dictionary.md)
- [Tableau Dashboard Links](dashboard/tableau_links.md)

---


## Production Considerations

This project uses synthetic data generation techniques to bridge the gap between public transaction records and dynamic user behaviour. In a real production environment, the same workflow could be extended with live clickstream data, impression logs, non-converted sessions, and real recommendation exposure data.

Several production topics would need further work:

- **Cold-start handling:** new users, new sellers, and new products would need fallback strategies.
- **Latency:** lead scoring and recommendation ranking would need to run fast enough for real-time or near-real-time use cases.
- **Data drift:** user behaviour, seller reliability, and product demand may change over time.
- **Catalog exposure and seller fairness:** relevance should be balanced with product diversity and fair exposure across sellers.
- **Cannibalization risk:** incremental lift should be measured against whether recommendations shift demand from already high-performing products instead of creating new value.
- **Model governance:** if LLM-based review classification is added, cost, privacy, consistency, and auditability would need to be managed.

---

## Skills Demonstrated

- Python data cleaning and feature engineering
- SQL business analysis with DuckDB
- Synthetic event pipeline design
- Funnel analysis
- Customer intent segmentation
- Lead scoring framework design
- Machine learning for rule automation and feature importance analysis
- Recommendation strategy design
- AB test design and statistical testing
- Tableau dashboard design
- Business reporting and analytical storytelling
