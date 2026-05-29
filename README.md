# AI-Powered Lead Generation & Recommendation Analytics

This project is an end-to-end analytics case study for an e-commerce marketplace. It uses the Brazilian Olist public e-commerce dataset to explore how transaction data, customer reviews, delivery performance, and simulated user behaviour can be combined to support lead generation and recommendation decisions.

The project was built as a portfolio project for data analytics, product analytics, and growth analytics roles. It focuses on a practical business question: **how can a platform identify high-intent customers and recommend products more effectively than a simple popularity-based approach?**

The workflow covers data cleaning, SQL-based business analysis, simulated user funnel analysis, intent classification, lead scoring, recommendation strategy design, simulated A/B testing, and Tableau dashboard reporting.

---

## Business Problem

Small and medium-sized sellers on marketplace platforms often need help understanding which customers are more likely to purchase, which product categories create stronger commercial value, and whether a more personalised recommendation strategy can improve engagement.

This project turns that problem into three analytical questions:

1. Which customers show stronger purchase intent?
2. Which categories, sellers, and customer segments create the most business value?
3. Can an intent-aware recommendation strategy outperform a basic popularity-based recommendation baseline?

---

## Dataset

The project uses the public Olist Brazilian e-commerce dataset. The raw data includes orders, customers, sellers, products, order items, payments, reviews, geolocation information, and product category translations.

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

After cleaning and feature engineering, the project creates analytical datasets for business reporting, lead scoring, recommendation analysis, and Tableau dashboards.

---

## Project Workflow

### 1. Data Understanding and Cleaning

The raw Olist tables were merged into a cleaned order-level dataset. The cleaning process included handling missing values, standardising product categories, calculating GMV, creating delivery delay features, and preparing customer, product, seller, and review information for analysis.

### 2. SQL Business Analysis

DuckDB SQL was used to generate business KPI tables, including overall GMV, monthly GMV trends, category performance, seller performance, payment method analysis, review score patterns, and delivery delay impact.

### 3. Simulated User Funnel Analysis

Because the Olist dataset contains completed transactions but does not provide real clickstream logs, this project builds a simulated engagement funnel using reproducible business assumptions. The funnel includes:

- view
- click
- add_to_cart
- inquiry
- purchase

This part is used to demonstrate lead-generation analytics logic rather than to claim access to real platform behaviour logs.

### 4. LLM-Inspired Intent Classification

A rule-based, LLM-inspired intent classification layer was built using review text, review score, delivery delay, behavioural signals, purchase value, and user segment information. Customers were assigned sentiment labels, intent categories, purchase intent levels, and rule-based lead scores.

Intent categories include:

- ready_to_purchase
- price_sensitive
- delivery_concern
- product_quality_concern
- after_sales_issue
- general_negative
- comparison_shopping
- neutral_or_unclear

### 5. Lead Scoring Model

Logistic Regression and Random Forest models were used to automate the lead scoring framework. The model uses behavioural, sentiment, delivery, value segment, and intent features to classify high-intent leads.

The model performance is very high because the target label is generated from rule-based business logic. Therefore, the model should be interpreted as an automation layer for the lead scoring framework, not as proof of real-world predictive accuracy.

### 6. Recommendation Strategy Design

Three recommendation strategies were designed and compared:

1. **Popularity-based recommendation**: recommends products mainly based on historical popularity.
2. **Category-preference recommendation**: recommends products based on the user's preferred category.
3. **Intent-aware recommendation**: combines user lead score, product high-intent rate, product review quality, seller review quality, and delivery reliability.

### 7. Simulated A/B Test Evaluation

A simulated A/B test was created to compare:

- **Control group**: popularity-based recommendation
- **Treatment group**: intent-aware recommendation

The evaluation compares CTR, inquiry rate, purchase rate, revenue per user, total revenue, and statistical significance.

---

## Key Results

The cleaned dataset contains:

- **96,478** completed orders
- **93,358** unique users
- **32,216** unique products
- **2,970** sellers
- **BRL 15.42M** total GMV
- **BRL 139.93** average order value
- **4.09** average review score

Top GMV categories included:

- health_beauty: BRL 1.41M
- watches_gifts: BRL 1.26M
- bed_bath_table: BRL 1.23M
- sports_leisure: BRL 1.12M
- computers_accessories: BRL 1.03M

Delivery performance had a clear impact on customer satisfaction:

| Delivery Group | Orders | Avg Review Score | Negative Review Rate |
|---|---:|---:|---:|
| Non-late delivery | 89,936 | 4.21 | 11.32% |
| Late delivery | 6,534 | 2.33 | 61.32% |

The simulated A/B test showed that the intent-aware recommendation strategy performed better than the popularity-based baseline:

| Metric | Control | Treatment | Uplift |
|---|---:|---:|---:|
| CTR | 19.42% | 22.76% | +17.2% |
| Inquiry Rate | 12.70% | 16.32% | +28.5% |
| Purchase Rate | 10.32% | 13.56% | +31.4% |
| Revenue per User | 9.10 | 13.18 | +44.9% |

Two-proportion z-tests showed statistically significant improvements in CTR, inquiry rate, and purchase rate at the 5% level. A Welch's t-test also showed a significant improvement in revenue per user.

---

## Tableau Dashboards

Three Tableau dashboards were created to present the final results.

- [Dashboard 1: Executive Overview](https://public.tableau.com/views/AI-lead-generation-recommendation-analytics/Dashboard1ExecutiveOverviewDashboard?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Dashboard 2: User Intent & Lead Quality](https://public.tableau.com/views/AI-lead-generation-recommendation-analytics/UserIntentLeadQuality?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Dashboard 3: Recommendation A/B Test Performance](https://public.tableau.com/views/AI-lead-generation-recommendation-analytics/Dashboard3RecommendationABTestPerformance?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

Dashboard screenshots are stored in:

```text
/dashboard/tableau_screenshots/
```

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
├── README.md
└── requirements.txt
```

---

## How to Run

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Then run the notebooks in order:

```text
01_data_understanding_and_cleaning.ipynb
02_sql_business_analysis.ipynb
03_user_funnel_analysis.ipynb
04_llm_intent_classification.ipynb
05_lead_scoring_model.ipynb
06_recommendation_strategy.ipynb
07_ab_test_evaluation.ipynb
```

The notebooks generate cleaned data, final analytical tables, model results, and dashboard-ready CSV outputs.

---

## Documentation

- [Executive Summary](report/executive_summary.md)
- [Full Project Report](report/project_report.md)
- [Data Dictionary](report/data_dictionary.md)

---

## Limitations

This project uses public transaction data rather than real platform clickstream data. User events, intent labels, lead scores, recommendation outcomes, and A/B test results are generated using transparent and reproducible business assumptions.

The funnel should be interpreted as a simulated engagement funnel around observed purchases, not as a real acquisition funnel with both converted and non-converted users.

The lead scoring model has near-perfect performance because the high-intent target was created from rule-based logic. The model is therefore best understood as a way to automate the scoring framework, not as a production predictive model.

The A/B test is simulated. It demonstrates experiment design and evaluation logic, but it does not represent a live production experiment.

---

## Skills Demonstrated

- Python data cleaning and feature engineering
- SQL business analysis with DuckDB
- Funnel analysis
- Customer intent segmentation
- Lead scoring framework design
- Classification model development
- Recommendation strategy design
- A/B test simulation and statistical testing
- Tableau dashboard design
- Business reporting and analytical storytelling
