# AI-Powered Lead Generation & Recommendation Analytics Platform

![Python](https://img.shields.io/badge/Python-Data%20Analytics-blue.svg)
![SQL](https://img.shields.io/badge/SQL-DuckDB-orange.svg)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-green.svg)
![A/B Testing](https://img.shields.io/badge/A%2FB%20Testing-Experiment-purple.svg)
![LLM Layer](https://img.shields.io/badge/LLM%20Layer-Seller%20Actions-pink.svg)
![Product Analytics](https://img.shields.io/badge/Product%20Analytics-SMB%20Growth-blueviolet.svg)

> **TL;DR:** Built an end-to-end AI-assisted SMB lead generation and recommendation analytics platform on **96K+ Olist e-commerce orders**. The project combines SQL business analysis, synthetic funnel construction, intent classification, lead scoring, recommendation strategy, an LLM-style seller action layer, simulated A/B testing, and Tableau dashboards. In the simulated experiment, the intent-aware recommendation strategy delivered a **+44.9% lift in Revenue per User** and a **+31.4% lift in Purchase Rate** compared with a popularity-based baseline.

---

## Project Overview

This project explores how a marketplace platform can help small and medium-sized sellers identify high-intent users, recommend relevant products, decide what follow-up action to take, and evaluate whether the strategy improves conversion and revenue.

The project is not only a recommendation model. It is designed as an AI-assisted lead generation workflow that connects:

1. marketplace performance analysis;
2. synthetic user funnel construction;
3. intent classification and lead scoring;
4. recommendation strategy design;
5. LLM-style seller action recommendations;
6. simulated A/B test evaluation;
7. Tableau dashboards for stakeholder communication.

The project is designed for data analytics, product analytics, growth analytics, recommendation strategy, and AI product roles.

---

## Product Problem Framing

SMB sellers on marketplace platforms often face a practical growth problem: they may have traffic, orders, reviews, and product visitors, but they do not always know which users are worth following up with or what action should be taken next.

The product problem is:

> How can a marketplace platform turn fragmented user, order, review, delivery, and engagement signals into high-intent lead prioritisation, relevant recommendations, and actionable seller follow-up decisions?

This framing shifts the project from “building a recommendation model” to designing a lead-to-action workflow for seller growth.

The workflow answers five business questions:

1. **Marketplace diagnosis:** How is the marketplace performing across users, categories, sellers, review quality, and delivery reliability?
2. **Lead generation:** Which users show stronger purchase intent and should be prioritised as leads?
3. **Recommendation strategy:** Can recommendations be improved by combining user intent, product quality, seller reliability, and category preference?
4. **Seller action support:** How can lead scores and intent labels be translated into seller-facing next-best actions?
5. **Experiment evaluation:** Does the intent-aware strategy create measurable uplift in conversion and revenue?

---

## User Persona and User Journey

### Primary User: SMB Seller

The primary user is a small or medium-sized seller who wants to convert marketplace traffic into leads, inquiries, and purchases.

Main pain points:

- does not know which users are worth following up with;
- lacks time and analytics resources to interpret customer behaviour;
- needs simple next-best-action guidance instead of raw model scores;
- wants to improve conversion from product visitors, inquiries, or livestream-style traffic.

### Internal User: Marketplace Product / Growth Team

The internal product or growth team uses the workflow to monitor funnel performance, compare recommendation strategies, evaluate A/B test uplift, and identify seller growth opportunities.

### End User: Buyer

The buyer receives more relevant product recommendations and seller follow-up actions based on their intent, concerns, and purchase readiness.

### User Journey

`Buyer interaction → Signal capture → Intent classification → Lead scoring → Recommendation strategy → Seller action recommendation → A/B test evaluation`

This journey connects user behaviour, AI-driven interpretation, seller action, and business outcome measurement.

---

## Alignment with SMB Lead Generation Scenario

This project aligns with a marketplace SMB lead generation scenario where sellers need help converting traffic into leads, inquiries, and purchases.

| Scenario Requirement | Project Implementation |
|---|---|
| Lead generation | Built synthetic funnel, intent classification, lead scoring, and high-intent user prioritisation |
| Recommendation strategy | Compared popularity-based, category-preference, and intent-aware recommendation strategies |
| LLM application | Added an LLM-style seller action layer that translates intent and lead signals into natural-language seller recommendations |
| User intent mining | Classified users into intent categories such as ready-to-purchase, price-sensitive, delivery-concerned, and product-quality-concerned |
| A/B testing | Simulated control vs. treatment experiment and evaluated CTR, inquiry rate, purchase rate, revenue per user, and significance |
| Seller growth insight | Converted model outputs into seller actions such as discounts, delivery reassurance, social proof, and customer support |

---

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**, which contains order, customer, seller, product, payment, review, and delivery information from a marketplace environment.

Main source tables include:

- orders;
- order items;
- customers;
- sellers;
- products;
- product category translation;
- payments;
- reviews.

The raw dataset does not include impression-level or clickstream-level user behaviour. To support lead generation and A/B testing analysis, this project creates a synthetic funnel based on transaction, review, delivery, product, and user segment signals.

---

## Project Workflow

### 1. Data Understanding and Cleaning

The first notebook builds the analytical base table from raw Olist data.

Main tasks:

- load and inspect raw marketplace datasets;
- merge order, customer, seller, product, payment, review, and delivery fields;
- clean missing values and inconsistent records;
- create order-level features such as GMV, delivery delay, price band, and review sentiment;
- export a clean base table for downstream analysis.

Main output:

- `data/processed/clean_order_base.csv`

---

### 2. SQL Business Analysis

The second notebook uses DuckDB SQL to analyse marketplace performance.

Main analysis areas:

- overall GMV and order performance;
- monthly GMV trend;
- category performance;
- seller performance;
- payment behaviour;
- review quality;
- delivery delay impact.

Main outputs include:

- `overall_kpi_summary.csv`
- `monthly_gmv_trend.csv`
- `category_performance.csv`
- `top_sellers_by_gmv.csv`
- `payment_type_summary.csv`
- `delivery_delay_impact.csv`

This stage provides the business foundation before building lead scoring and recommendation logic.

---

### 3. Synthetic User Funnel Analysis

The third notebook creates a synthetic behavioural funnel to approximate user engagement signals.

Simulated funnel stages include:

- view;
- click;
- add to cart;
- inquiry;
- purchase.

The funnel is generated from available signals such as category, price band, review score, user value segment, delivery delay, traffic source, and device type.

Main output:

- `data/final/fact_user_events.csv`

This table supports funnel analysis, lead scoring, recommendation evaluation, and A/B test simulation.

---

### 4. Intent Classification Layer

The fourth notebook creates a lightweight intent classification layer.

Intent categories include:

- `ready_to_purchase`;
- `price_sensitive`;
- `delivery_concern`;
- `product_quality_concern`;
- `after_sales_issue`;
- `general_negative`;
- `neutral_or_unclear`.

The intent layer uses review text, review score, delivery delay, price band, funnel behaviour, and purchase signals to create explainable intent labels.

Main output:

- `data/final/fact_reviews_llm.csv`

This layer is designed as a transparent prototype of user intent mining. In a production system, it could be upgraded with real LLM or embedding-based intent understanding.

---

### 5. Lead Scoring Model

The fifth notebook builds a lead scoring framework.

It combines rule-based scoring with a machine learning model to estimate user purchase intent and lead quality.

Main features include:

- funnel events;
- user value segment;
- review score;
- sentiment;
- price band;
- delivery delay;
- traffic source;
- device type;
- intent category.

Main outputs include:

- `data/final/fact_lead_scores.csv`
- `lead_scoring_model_metrics.csv`
- `lead_scoring_feature_importance.csv`
- `lead_score_by_user_segment.csv`

The lead scoring layer helps identify which users should be prioritised for seller follow-up.

---

### 6. Recommendation Strategy

The sixth notebook designs and compares three recommendation strategies:

1. **Popularity-based recommendation**  
   Recommends products mainly based on historical popularity and performance.

2. **Category-preference recommendation**  
   Recommends products based on user category preference.

3. **Intent-aware recommendation**  
   Combines lead score, intent category, product quality, seller reliability, category preference, and product high-intent rate.

Main outputs include:

- `data/final/fact_recommendations.csv`
- `recommendation_strategy_summary.csv`
- `recommendation_user_level.csv`
- `recommendation_category_summary.csv`

This layer moves the project from lead identification to product and seller matching.

---

### 7. Simulated A/B Test Evaluation

The seventh notebook evaluates whether the intent-aware recommendation strategy improves business outcomes.

The simulated experiment compares:

- **Control group:** popularity-based recommendation;
- **Treatment group:** intent-aware recommendation.

Evaluation metrics include:

- click-through rate;
- inquiry rate;
- purchase rate;
- revenue per user;
- total revenue;
- statistical significance.

Main outputs include:

- `data/final/fact_recommendation_experiment.csv`
- `ab_test_summary.csv`
- `ab_test_uplift_summary.csv`
- `ab_test_significance.csv`

---

### 8. LLM-Style Seller Action Layer

The final enhancement layer translates lead scores, intent labels, recommendation candidates, and seller quality signals into seller-facing next-best actions.

The output includes:

- seller action type;
- seller action priority;
- seller-facing message;
- natural-language explanation.

Example actions include:

- `send_limited_time_offer`;
- `send_discount_or_bundle`;
- `highlight_delivery_reliability`;
- `show_social_proof`;
- `offer_customer_support`;
- `personalised_product_follow_up`;
- `nurture_with_general_content`.

This layer makes the system more actionable for SMB sellers because it explains what the seller should do next, not just which product should be recommended.

Main outputs:

- `outputs/tables/llm_seller_action_recommendations.csv`
- `outputs/tables/llm_seller_action_summary.csv`

---

## Key Results

### Marketplace Scale

The cleaned analytical dataset contains:

- **96K+ orders**
- **96K+ unique users**
- **3K+ sellers**
- **70+ product categories**
- **R$13M+ GMV**

These figures provide enough marketplace scale to build a realistic analytics and recommendation workflow.

---

### A/B Test Results

The simulated treatment strategy showed stronger performance than the popularity-based control strategy.

| Metric | Control | Treatment | Lift |
|---|---:|---:|---:|
| Click-through rate | Baseline | Higher | Positive |
| Inquiry rate | Baseline | Higher | Positive |
| Purchase rate | Baseline | Higher | **+31.4%** |
| Revenue per user | Baseline | Higher | **+44.9%** |

The treatment strategy improved both conversion and monetisation outcomes in the simulated experiment.

---

### LLM-Style Seller Action Output

The LLM-style seller action layer generated **15,000 seller-facing action recommendations** based on user intent, lead quality, recommendation candidates, and seller quality signals.

| Seller Action Type | Share |
|---|---:|
| `send_limited_time_offer` | **49.86%** |
| `highlight_delivery_reliability` | **19.94%** |
| `send_discount_or_bundle` | **18.72%** |
| `nurture_with_general_content` | **5.28%** |
| `show_social_proof` | **4.26%** |
| `personalised_product_follow_up` | **1.08%** |
| `offer_customer_support` | **0.86%** |

The high share of limited-time offers reflects that this layer is built on a pre-filtered recommendation candidate pool rather than the full user base. The output is designed to help sellers move from raw lead scores to practical follow-up actions.

---

### Intent-Action Validation

The seller action layer maps different intent categories to different seller actions.

| Intent Category | Main Seller Action |
|---|---|
| `ready_to_purchase` | `send_limited_time_offer` |
| `price_sensitive` | `send_discount_or_bundle` |
| `delivery_concern` | `highlight_delivery_reliability` |
| `product_quality_concern` | `show_social_proof` |
| `after_sales_issue` | `offer_customer_support` |
| `general_negative` | `nurture_with_general_content` |
| `neutral_or_unclear` | Split by lead score and purchase intent |

This validation shows that the layer does not simply push generic promotions. It converts different user intent signals into context-aware seller actions.

---

## Tableau Dashboards

Three Tableau dashboards were created to communicate the project outputs.

### Dashboard 1: Executive Overview

Purpose:

- show overall GMV and order performance;
- compare category and seller performance;
- summarise marketplace-level health.

### Dashboard 2: User Intent and Lead Quality

Purpose:

- analyse intent category distribution;
- compare lead score by user segment;
- understand high-intent user patterns.

### Dashboard 3: Recommendation A/B Test Performance

Purpose:

- compare control and treatment performance;
- show uplift in purchase rate and revenue per user;
- communicate experiment results to stakeholders.

Dashboard screenshots are stored under:

```text
dashboard/
```

---

## Product Roadmap / MVP Plan

| Stage | Focus | Main Outputs |
|---|---|---|
| MVP 0 | Analytics foundation | Clean order table, SQL KPI outputs, Tableau overview |
| MVP 1 | Lead generation engine | Synthetic funnel, intent categories, lead scores |
| MVP 2 | Recommendation strategy | Popularity-based, category-preference, and intent-aware recommendations |
| MVP 3 | LLM-style seller action assistant | Seller action type, priority, message, explanation |
| MVP 4 | Experimentation and stakeholder reporting | Simulated A/B test, uplift metrics, Tableau dashboards |
| Production extension | Real platform deployment | Real clickstream logs, real LLM scripts, CRM integration, online A/B testing, safety guardrails |

This roadmap shows how the project can evolve from an analytical prototype into a practical SMB seller growth product.

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
│   ├── 07_ab_test_evaluation.ipynb
│   └── 08_llm_intent_explanation.ipynb
│
├── src/
│   ├── data_pipeline.py             # Reusable data cleaning and synthetic funnel generation logic
│   ├── intent_engine.py             # Intent feature extraction and lead scoring support
│   ├── recommendation_strategy.py   # Popularity-based and intent-aware recommendation logic
│   └── utils.py                     # Shared logging and utility functions
│
├── outputs/
│   ├── tables/                      # SQL, funnel, intent, recommendation, A/B test, and seller action outputs
│   └── model_results/               # Lead scoring model metrics and feature importance
│
├── dashboard/
│   ├── tableau_screenshots/         # Tableau dashboard screenshots
│   └── tableau_links.md             # Tableau Public dashboard links
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

The `notebook/` folder documents the full analytical workflow, including data exploration, SQL analysis, funnel construction, LLM-style intent classification, lead scoring, recommendation strategy design, A/B test evaluation, and LLM-style seller action generation.

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

This project is a portfolio prototype, not a production recommendation system. A production version would require:

- **Real user behaviour logs:** impression, click, add-to-cart, inquiry, chat, livestream engagement, and non-purchase sessions;
- **Online experimentation:** live randomisation and guardrail metrics;
- **Real-time infrastructure:** batch and streaming pipelines for lead scoring and recommendation updates;
- **Recommendation diversity:** controls for product diversity, seller fairness, and long-term marketplace health;
- **LLM governance:** if real LLMs are used for buyer intent understanding or seller message generation, cost, privacy, consistency, hallucination control, content safety, and auditability would need to be managed;
- **Seller action guardrails:** generated seller actions should avoid aggressive promotion for negative or support-related users and should consider seller fairness, buyer experience, and brand consistency.

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
- LLM-style seller action recommendation layer
- A/B test design and statistical testing
- Tableau dashboard design
- Product problem framing for SMB lead generation
- User persona and user journey design
- Product roadmap and MVP planning
- Business reporting and analytical storytelling

---

## How to Read This Project

For a quick review:

1. Start with this README for the project overview and workflow.
2. Read `report/project_report.md` for the full methodology and business interpretation.
3. Review the notebooks in order from `01` to `08`.
4. Check the Tableau dashboards for stakeholder-facing insights.
5. Review `outputs/tables/llm_seller_action_recommendations.csv` to see how lead scores and intent labels are converted into seller actions.

---

## Author

**Raina Hong**  
Master of Computer Science, University of Sydney  
Focus: Data Analytics, AI Product Analytics, Recommendation Strategy, and Growth Analytics
