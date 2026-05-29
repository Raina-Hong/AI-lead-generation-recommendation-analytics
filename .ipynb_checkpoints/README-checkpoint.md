# AI-Powered Lead Generation & Recommendation Analytics

## Project Overview

This project builds an end-to-end analytics workflow for an e-commerce lead generation and recommendation use case. Using the public Olist e-commerce dataset, the project combines data cleaning, SQL-based business analysis, simulated user funnel modelling, LLM-inspired intent classification, lead scoring, recommendation strategy design, A/B test simulation, and Tableau dashboard reporting.

The goal is to demonstrate how an analytics team could identify high-intent users, evaluate seller and product quality, generate recommendation candidates, and measure the business impact of an intent-aware recommendation strategy.

> Note: The original Olist dataset does not contain real clickstream, lead intent labels, recommendation exposure logs, or experiment outcomes. These components are generated using reproducible business rules and simulation logic for portfolio demonstration purposes.

## Business Problem

E-commerce platforms need to understand which users are most likely to convert and which products or sellers should be recommended to them. A simple popularity-based recommendation strategy may generate high exposure, but it can ignore user intent, seller quality, product satisfaction, and lead value.

This project answers three business questions:

1. Which categories, sellers, and customer segments generate the strongest commercial performance?
2. Can user behaviour and review signals be converted into interpretable lead intent and lead quality scores?
3. Does an intent-aware recommendation strategy outperform a popularity-based strategy in a simulated A/B test?

## Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset, including orders, order items, payments, reviews, products, sellers, customers, geolocation, and product category translation tables.

Main generated analytical tables include:

- `clean_order_base.csv`: cleaned order-level analytical dataset
- `fact_user_events.csv`: simulated user event log
- `fact_reviews_llm.csv`: LLM-inspired intent classification table
- `fact_lead_scores.csv`: model-based lead scoring output
- `fact_recommendations.csv`: recommendation strategy output
- `fact_recommendation_experiment.csv`: simulated A/B test exposure and outcome table

## Methodology

### 1. Data Understanding and Cleaning

Raw Olist tables are profiled, missing values are reviewed, Portuguese category names are translated into English, and order, payment, product, seller, customer, and review tables are merged into a clean order-level dataset.

Key engineered features include:

- order month and year
- gross merchandise value (GMV)
- delivery delay days
- late delivery flag
- product price band

### 2. SQL Business Analysis

DuckDB SQL is used to calculate core business KPIs and performance breakdowns, including:

- total orders, users, sellers, products, and GMV
- monthly GMV trend
- category performance
- top sellers by GMV
- payment method analysis
- delivery delay impact
- category-seller performance matrix

### 3. User Funnel Analysis

Because the original dataset does not contain clickstream events, a reproducible simulated event log is created from confirmed purchase records. Events include:

- view
- click
- add_to_cart
- inquiry
- purchase

The funnel is used to analyse user engagement patterns by category, traffic source, user segment, and seller.

### 4. LLM-Inspired Intent Classification

Review text, review score, delivery delay, price band, and behavioural signals are used to classify user intent. The logic is inspired by LLM-style text interpretation but implemented through transparent keyword and rule-based classification.

Generated labels include:

- sentiment
- intent category
- purchase intent level
- rule-based lead score
- high-intent lead flag

### 5. Lead Scoring Model

A predictive lead scoring model is built using Logistic Regression and Random Forest. The model predicts whether a record belongs to the high-intent lead group.

The model output is converted into a model-based lead score from 0 to 100.

Important modelling note: the high-intent label is generated from rule-based logic, so model performance should be interpreted as validation of the scoring framework rather than proof of real-world predictive accuracy.

### 6. Recommendation Strategy

Three recommendation strategies are designed and compared:

1. Popularity-based recommendation
2. Category-preference recommendation
3. Intent-aware recommendation

The intent-aware strategy combines product popularity, product review quality, product high-intent rate, model lead score, seller review quality, seller high-intent rate, and seller late-delivery penalty.

### 7. A/B Test Evaluation

A simulated A/B test compares:

- control group: popularity-based recommendation
- treatment group: intent-aware recommendation

Evaluation metrics include:

- click-through rate (CTR)
- inquiry rate
- purchase rate
- revenue per user
- total revenue
- statistical significance tests

## Key Results

- Cleaned order-level dataset contains 96,478 delivered orders and 93,358 unique users.
- Total GMV in the cleaned delivered-order dataset is approximately 15.42M.
- Average review score is 4.09.
- Simulated A/B test results show the intent-aware strategy outperformed the popularity-based strategy:
  - CTR uplift: 17.20%
  - inquiry rate uplift: 28.50%
  - purchase rate uplift: 31.40%
  - revenue per user uplift: 44.88%
- Statistical tests indicate significant differences between control and treatment groups in the simulated experiment.

## Tableau Dashboards

Three Tableau dashboards were created:

1. Executive Overview Dashboard
2. User Intent & Lead Quality Dashboard
3. Recommendation A/B Test Performance Dashboard

Dashboard links are stored in `dashboard/tableau_links.md`.

## Project Structure

```text
AI-lead-generation-recommendation-analytics/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
├── dashboard/
│   ├── tableau_links.md
│   └── tableau_screenshots/
├── notebook/
│   ├── 01_data_understanding_and_cleaning.ipynb
│   ├── 02_sql_business_analysis.ipynb
│   ├── 03_user_funnel_analysis.ipynb
│   ├── 04_llm_intent_classification.ipynb
│   ├── 05_lead_scoring_model.ipynb
│   ├── 06_recommendation_strategy.ipynb
│   └── 07_ab_test_evaluation.ipynb
├── outputs/
│   ├── tables/
│   └── model_results/
├── report/
├── sql/
├── requirements.txt
└── README.md
```

## Tools Used

- Python
- Pandas
- NumPy
- DuckDB SQL
- Scikit-learn
- SciPy
- Tableau
- Jupyter Notebook
- Git/GitHub

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the notebooks in order from the `notebook/` folder:

1. `01_data_understanding_and_cleaning.ipynb`
2. `02_sql_business_analysis.ipynb`
3. `03_user_funnel_analysis.ipynb`
4. `04_llm_intent_classification.ipynb`
5. `05_lead_scoring_model.ipynb`
6. `06_recommendation_strategy.ipynb`
7. `07_ab_test_evaluation.ipynb`

## Limitations

This is a portfolio analytics project based on public historical data. The original dataset does not include real user browsing sessions, ad exposure records, live recommendation logs, or real A/B experiment outcomes. Therefore, simulated funnel events, intent labels, lead scores, recommendations, and A/B outcomes should be interpreted as a structured analytical demonstration rather than production causal evidence.

## Portfolio Value

This project demonstrates practical skills in:

- end-to-end data analytics workflow design
- SQL business KPI analysis
- user funnel and conversion analytics
- rule-based NLP-style intent classification
- lead scoring model development
- recommendation strategy design
- A/B test simulation and statistical evaluation
- Tableau dashboard storytelling
