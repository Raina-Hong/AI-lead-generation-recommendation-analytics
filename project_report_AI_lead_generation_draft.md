# AI-Powered Lead Generation & Recommendation Analytics Report

## 1. Executive Summary

This project develops an end-to-end analytics workflow for an e-commerce lead generation and recommendation use case. The project uses the public Olist e-commerce dataset and extends it into a portfolio-style business analytics system covering data cleaning, SQL KPI analysis, user funnel simulation, intent classification, lead scoring, recommendation strategy design, A/B test simulation, and Tableau dashboard reporting.

The core business objective is to identify high-intent users and recommend higher-quality products or sellers more effectively than a simple popularity-based strategy. The final simulated A/B test suggests that an intent-aware recommendation strategy can outperform a popularity-based baseline across click-through rate, inquiry rate, purchase rate, and revenue per user.

Because the original dataset does not contain real clickstream logs, user intent labels, recommendation exposure records, or experiment outcomes, these components are generated using transparent and reproducible business assumptions. Therefore, the project should be interpreted as an analytics and decision-support demonstration, not as a production causal experiment.

## 2. Business Context and Problem Definition

For an e-commerce or social commerce platform, lead generation is the process of identifying users who are likely to take valuable actions such as clicking a product, asking a question, adding an item to cart, or making a purchase. Recommendation quality affects both user experience and commercial outcomes. A weak recommendation strategy may over-rely on historically popular products, while ignoring user intent, seller reliability, product satisfaction, and customer segment differences.

This project addresses the following questions:

1. What are the main business performance patterns across categories, sellers, payment methods, and delivery experience?
2. How can review text, review score, delivery performance, and behavioural signals be translated into lead intent and lead quality scores?
3. How can product, seller, and user-level signals be combined into a recommendation strategy?
4. In a simulated A/B test, does an intent-aware recommendation strategy perform better than a popularity-based baseline?

## 3. Data Sources

The project uses the Olist Brazilian E-Commerce Public Dataset. The raw data includes customers, orders, order items, payments, reviews, products, sellers, geolocation, and product category translation tables.

The cleaned order-level dataset contains key fields such as order ID, user ID, product ID, seller ID, product category, order time, price, freight value, payment value, payment type, review score, customer location, seller location, delivery delay, and GMV.

## 4. Data Cleaning and Feature Engineering

The first notebook profiles all raw datasets and generates missing value summaries. Product categories are translated from Portuguese to English. Payment records and review records are aggregated at order level before joining with orders, order items, products, sellers, and customers.

Key features created include:

- `gmv`: order-level gross merchandise value
- `order_year` and `order_month`: time-series analysis fields
- `delivery_delay_days`: actual delivery date minus estimated delivery date
- `late_delivery_flag`: whether the order was delivered later than expected
- `price_band`: product price segmentation based on quartiles

The cleaned delivered-order dataset contains 96,478 orders, 93,358 unique users, 32,216 unique products, 2,970 unique sellers, and approximately 15.42M total GMV. The average review score is 4.09.

## 5. SQL Business Analysis

DuckDB SQL is used to create business-facing KPI tables. The analysis covers overall KPI summary, monthly GMV trend, category performance, top sellers, customer value, payment method, review score by category, delivery delay impact, and category-seller matrix.

This step is important because it separates analytical logic from Python data manipulation and demonstrates how a business analyst would create reusable SQL outputs for dashboards and reporting.

Key outputs include:

- `overall_kpi_summary.csv`
- `monthly_gmv_trend.csv`
- `category_performance.csv`
- `top_sellers_by_gmv.csv`
- `payment_method_analysis.csv`
- `delivery_delay_impact.csv`
- `category_seller_matrix.csv`

## 6. User Funnel Analysis

The Olist dataset contains confirmed purchases but does not contain browsing or clickstream data. To support funnel and lead-generation analysis, the project creates a simulated event log from confirmed purchase records.

The simulated event stages are:

1. view
2. click
3. add_to_cart
4. inquiry
5. purchase

Each purchase journey starts with a view and ends with a purchase. Intermediate engagement events are generated using reproducible probability rules influenced by user value, product review score, seller quality, and delivery performance.

The generated funnel outputs are used to analyse engagement patterns by category, traffic source, user segment, and seller.

Important interpretation note: because the event log is simulated from purchase records, the funnel should be described as a simulated engagement funnel around observed purchases, rather than a real end-to-end acquisition funnel with both converted and non-converted users.

## 7. LLM-Inspired Intent Classification

The project creates an intent classification layer using review text, review score, delivery delay, price band, and simulated behaviour signals. The logic is described as LLM-inspired because it imitates the business role of text interpretation and user intent extraction, but it is implemented using transparent keyword dictionaries and deterministic rules.

The classification produces:

- sentiment: positive, neutral, or negative
- intent category: delivery concern, product quality concern, price sensitive, after-sales issue, ready to purchase, comparison shopping, or neutral/unclear
- purchase intent: high, medium, or low
- rule-based lead score from 0 to 100
- high-intent lead flag

This stage turns raw review and behaviour signals into structured features that can support lead scoring and recommendation logic.

## 8. Lead Scoring Model

The lead scoring model predicts whether a record is a high-intent lead. Logistic Regression is used as an interpretable baseline, while Random Forest is used as a more flexible model. The final model generates a model-based high-intent probability and converts it into a 0–100 lead score.

The model achieves very high evaluation metrics, with both Logistic Regression and Random Forest producing near-perfect ROC-AUC. This result should be interpreted carefully. The target label is generated from rule-based lead scoring logic, and several model features are strongly related to that label. Therefore, the model validates and reproduces the designed scoring framework rather than proving real-world predictive power.

For a production version, the target should ideally come from real future outcomes such as actual conversion, repeat purchase, inquiry-to-purchase conversion, or campaign response.

## 9. Recommendation Strategy Design

The recommendation notebook designs three strategies:

1. Popularity-based recommendation: recommends products with strong historical order and GMV performance.
2. Category-preference recommendation: recommends products from the user's preferred category.
3. Intent-aware recommendation: combines product performance, lead intent, seller quality, and delivery reliability.

The intent-aware recommendation score uses signals such as product orders, product GMV, product review score, product high-intent rate, product average model lead score, seller review score, seller high-intent rate, and seller late-delivery penalty.

The strategy comparison shows that the popularity-based method is highly concentrated, while the category-preference method improves product and seller diversity. The intent-aware strategy prioritises high-quality and high-intent products but may still require additional diversity controls in a production setting.

## 10. Simulated A/B Test Evaluation

The final notebook simulates an A/B test comparing:

- control group: popularity-based recommendation
- treatment group: intent-aware recommendation

The experiment evaluates CTR, inquiry rate, purchase rate, total revenue, and revenue per user. Statistical tests are used to compare control and treatment outcomes.

The simulated A/B test results are:

| Metric | Control | Treatment | Uplift |
|---|---:|---:|---:|
| CTR | 0.1942 | 0.2276 | 17.20% |
| Inquiry rate | 0.1270 | 0.1632 | 28.50% |
| Purchase rate | 0.1032 | 0.1356 | 31.40% |
| Revenue per user | 9.0971 | 13.1796 | 44.88% |
| Total revenue | 45,485.40 | 65,898.25 | 44.88% |

The significance tests indicate that the simulated treatment-control differences are statistically significant at the 5% level.

## 11. Tableau Dashboard Design

Three Tableau dashboards were created to communicate the project outputs.

### Dashboard 1: Executive Overview

This dashboard summarises business-level performance, including GMV, orders, review score, category performance, seller performance, and monthly trend.

### Dashboard 2: User Intent & Lead Quality

This dashboard focuses on intent classification and lead quality. It shows sentiment distribution, purchase intent, lead score by category, and lead quality by user segment.

### Dashboard 3: Recommendation A/B Test Performance

This dashboard compares control and treatment groups in the simulated recommendation experiment. It presents CTR, inquiry rate, purchase rate, revenue per user, uplift, and segment-level differences.

## 12. Limitations

This project has several important limitations:

1. The original dataset does not contain real clickstream events, so funnel events are simulated.
2. The intent labels and high-intent lead flag are generated using rule-based logic, not human-labelled training data.
3. The lead scoring model uses features that are strongly related to the generated target, so the high model performance should not be interpreted as production predictive accuracy.
4. The recommendation exposure and A/B test outcomes are simulated, not collected from a live experiment.
5. Recommendation diversity is limited in the current strategy design, especially for popularity-based and intent-aware strategies.

## 13. Recommendations for Improvement

Future improvements could include:

- simulate non-purchase sessions to create a more realistic acquisition funnel
- use real future purchase or repeat purchase as the lead scoring target
- remove target-leakage features from the predictive model
- add recommendation diversity constraints
- evaluate precision@k, recall@k, MAP, or NDCG for recommendation ranking
- separate training and scoring periods to avoid temporal leakage
- add model calibration and threshold analysis
- create a monitoring dashboard for lead score drift and recommendation performance

## 14. Conclusion

This project demonstrates a complete analytics workflow for lead generation and recommendation strategy evaluation. It shows how raw e-commerce data can be transformed into business KPIs, lead intent signals, scoring models, recommendation outputs, and experiment evaluation dashboards.

The strongest portfolio value of this project is not that it proves a production recommendation system, but that it demonstrates business problem framing, data modelling, SQL analytics, feature engineering, machine learning workflow design, A/B test thinking, and dashboard storytelling in one coherent project.
