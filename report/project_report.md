# AI-Powered Lead Generation & Recommendation Analytics Report

## 1. Introduction

This project builds an end-to-end analytics workflow for AI-powered lead generation and recommendation analysis in an e-commerce marketplace setting.

The project uses the public Olist Brazilian e-commerce dataset. The raw dataset contains orders, customers, sellers, products, payments, reviews, and delivery information. On top of this transaction data, the project creates simulated user engagement events, customer intent labels, lead scores, recommendation strategies, and an A/B testing framework.

The purpose of the project is to show how a platform could move from basic transaction reporting to a more business-oriented analytics workflow: identifying high-intent customers, understanding lead quality, recommending products more intelligently, and evaluating recommendation performance.

This is a portfolio analytics project rather than a production system. Where the original data does not contain certain fields, such as clickstream events or real experiment outcomes, those parts are simulated using transparent business assumptions.

---

## 2. Business Problem

For an e-commerce marketplace, product recommendation is not only a technical ranking problem. It is also a business problem. The platform needs to understand which customers are likely to purchase, which products and sellers are reliable, and which recommendation strategy is most likely to improve engagement and revenue.

A simple popularity-based approach can recommend frequently purchased products, but it ignores several important signals:

- whether the customer is showing strong purchase intent;
- whether the product matches the customer's preferred category;
- whether the product has strong review performance;
- whether the seller delivers reliably;
- whether a customer is high value or low value;
- whether the recommendation strategy actually improves conversion outcomes.

This project focuses on three business questions:

1. How can high-intent customers be identified from transaction, review, delivery, and behavioural signals?
2. Which product categories, sellers, and user segments are most valuable?
3. Can an intent-aware recommendation strategy outperform a popularity-based baseline in a simulated experiment?

---

## 3. Data Sources

The project uses the Olist public e-commerce dataset. The raw data tables include:

| Raw Table | Description |
|---|---|
| `olist_customers_dataset.csv` | Customer IDs, unique customer IDs, customer city, and state |
| `olist_orders_dataset.csv` | Order status and order lifecycle timestamps |
| `olist_order_items_dataset.csv` | Product, seller, price, and freight information at order-item level |
| `olist_order_payments_dataset.csv` | Payment type, payment instalments, and payment value |
| `olist_order_reviews_dataset.csv` | Review scores and customer review text |
| `olist_products_dataset.csv` | Product category and product attributes |
| `olist_sellers_dataset.csv` | Seller location information |
| `product_category_name_translation.csv` | Product category translation from Portuguese to English |
| `olist_geolocation_dataset.csv` | Brazilian zip code, latitude, longitude, city, and state data |

The raw data was transformed into one cleaned order-level dataset and several final analytical tables.

The main final datasets are:

| Dataset | Purpose |
|---|---|
| `clean_order_base.csv` | Cleaned order-level analytical base table |
| `fact_user_events.csv` | Simulated user event table for funnel analysis |
| `fact_reviews_llm.csv` | Intent classification and rule-based lead scoring table |
| `fact_lead_scores.csv` | Model-based lead scoring output |
| `fact_recommendations.csv` | Recommendation candidates from different strategies |
| `fact_recommendation_experiment.csv` | Simulated A/B test outcomes |

---

## 4. Data Cleaning and Preparation

The first step was to create a clean order-level analytical table. This table was built by merging order records with customer, product, seller, payment, order item, review, and product category translation data.

The cleaning process included:

- filtering and preparing delivered order records;
- merging product category translations so that categories can be analysed in English;
- combining price and freight value to calculate GMV;
- calculating delivery delay using actual delivery date and estimated delivery date;
- creating a late delivery flag;
- extracting order date, order year, and order month;
- standardising product category values;
- creating price bands;
- preserving customer location, seller location, payment type, and review score for later analysis.

The final cleaned order base contains business-ready fields such as `gmv`, `delivery_delay_days`, `late_delivery_flag`, `price_band`, `category`, `payment_type`, `review_score`, `seller_state`, and `customer_state`.

A missing value check was also completed. The highest missing rates were in review comment fields, which is expected because many customers leave a score without writing a text review. The review comment title had an 88.34% missing rate and the review comment message had a 58.70% missing rate. These missing text values were handled carefully in the later intent classification step by using a placeholder rather than dropping the records.

---

## 5. SQL Business Analysis

DuckDB SQL was used to generate the main business analysis outputs. The SQL layer produced KPI tables for overall marketplace performance, monthly GMV trend, category performance, seller performance, customer value, review quality, payment method, and delivery delay impact.

The overall KPI summary showed:

| Metric | Value |
|---|---:|
| Completed orders | 96,478 |
| Unique users | 93,358 |
| Unique products | 32,216 |
| Unique sellers | 2,970 |
| Total GMV | BRL 15.42M |
| Average order value | BRL 139.93 |
| Average review score | 4.09 |

The highest GMV product categories were:

| Category | Orders | Total GMV | Average Review Score |
|---|---:|---:|---:|
| health_beauty | 8,647 | BRL 1.41M | 4.20 |
| watches_gifts | 5,495 | BRL 1.26M | 4.08 |
| bed_bath_table | 9,272 | BRL 1.23M | 3.94 |
| sports_leisure | 7,530 | BRL 1.12M | 4.17 |
| computers_accessories | 6,530 | BRL 1.03M | 3.99 |

Payment analysis showed that credit card was the dominant payment type, with 73,941 orders and BRL 12.23M GMV. Boleto was the second-largest payment method, with 19,191 orders and BRL 2.77M GMV.

One of the most important findings was the impact of delivery delay on review quality:

| Delivery Group | Orders | Avg Delivery Delay Days | Avg Review Score | Negative Review Rate |
|---|---:|---:|---:|---:|
| Non-late delivery | 89,936 | -13.62 | 4.21 | 11.32% |
| Late delivery | 6,534 | 10.49 | 2.33 | 61.32% |

This result shows that delivery reliability is closely related to customer satisfaction. For recommendation design, this means seller delivery performance should be considered alongside product popularity.

---

## 6. User Funnel Simulation

The Olist dataset does not include real browsing, click, add-to-cart, inquiry, or non-purchase session data. To support lead-generation analysis, this project created a simulated user engagement funnel based on observed purchase records and reproducible business assumptions.

The simulated event types are:

1. `view`
2. `click`
3. `add_to_cart`
4. `inquiry`
5. `purchase`

The generated funnel summary was:

| Event Type | Unique Users | Conversion from View | Stage-to-Stage Conversion |
|---|---:|---:|---:|
| view | 93,358 | 100.00% | 100.00% |
| click | 65,258 | 69.90% | 69.90% |
| add_to_cart | 48,823 | 52.30% | 74.82% |
| inquiry | 35,024 | 37.52% | 71.74% |
| purchase | 93,358 | 100.00% | 266.55% |

The purchase stage looks different from a normal acquisition funnel because the simulation was built from confirmed purchase records. In other words, the purchase records already exist in the source data, while earlier events were simulated around them. For this reason, the funnel should be interpreted as a simulated engagement funnel around completed purchases, not as a true acquisition funnel containing both converted and non-converted visitors.

The funnel was also analysed by user segment and traffic source. High Value users had a higher click-through rate and inquiry rate than lower-value users. High Value users had a 75.16% click-through rate and a 42.07% inquiry rate, compared with 65.92% and 34.01% for Low Value users. This supports the idea that user value segment can be useful for lead prioritisation.

---

## 7. LLM-Inspired Intent Classification

The next step was to create a customer intent layer. This project uses a rule-based, LLM-inspired approach rather than calling an external large language model API.

The intent classification logic uses:

- review score;
- review text;
- delivery delay;
- late delivery flag;
- simulated user behaviour signals;
- user value segment;
- price band;
- GMV.

Each record was assigned:

- `sentiment`: positive, neutral, or negative;
- `intent_category`: business-readable intent segment;
- `purchase_intent`: low, medium, or high;
- `lead_score`: rule-based score from 0 to 100;
- `high_intent_flag`: binary high-intent label.

The intent category summary showed:

| Intent Category | Records | Unique Users | Avg Lead Score | High-Intent Rate | Total GMV |
|---|---:|---:|---:|---:|---:|
| ready_to_purchase | 51,869 | 44,842 | 99.93 | 100.00% | BRL 4.02M |
| price_sensitive | 20,822 | 19,145 | 92.48 | 92.59% | BRL 6.69M |
| delivery_concern | 21,995 | 19,155 | 80.48 | 79.90% | BRL 3.36M |
| product_quality_concern | 4,883 | 4,082 | 74.79 | 78.07% | BRL 667.26K |
| neutral_or_unclear | 5,883 | 4,860 | 85.69 | 69.98% | BRL 451.91K |
| general_negative | 6,117 | 4,212 | 50.81 | 59.47% | BRL 468.15K |

Two points are worth highlighting. First, the ready_to_purchase segment is the clearest high-intent group. Second, the price_sensitive segment generated the largest GMV among the intent categories. This is important because price-sensitive customers are not necessarily low-quality leads. They may still have strong purchase intent if they show clear behavioural signals.

---

## 8. Lead Scoring Model

After creating the rule-based lead score and high-intent flag, two classification models were trained to automate the lead scoring framework:

- Logistic Regression
- Random Forest

The models used features such as review score, sentiment, purchase intent, intent category, behavioural events, user value segment, delivery delay, traffic source, and device type.

The model metrics were:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9997 | 1.0000 | 0.9996 | 0.9998 | 1.0000 |
| Random Forest | 0.9987 | 1.0000 | 0.9985 | 0.9992 | 1.0000 |

These numbers are intentionally interpreted with caution. The target variable was created using rule-based business logic, and the model features include variables that are closely related to that rule-based target. Because of this, the model is not evidence of real-world predictive performance.

The better interpretation is that the model successfully automates and reproduces the lead scoring framework. In a real business environment, a true predictive model would require both converted and non-converted users, real behavioural logs, and labels based on future conversion outcomes.

The most important model features included:

| Feature | Importance |
|---|---:|
| purchase_intent_high | 0.2585 |
| purchase_intent_low | 0.1389 |
| review_score | 0.1042 |
| sentiment_positive | 0.0928 |
| added_to_cart | 0.0786 |
| total_events | 0.0604 |
| purchase_intent_medium | 0.0502 |
| intent_category_ready_to_purchase | 0.0497 |
| inquired | 0.0441 |
| sentiment_negative | 0.0337 |

The feature ranking is consistent with the project logic: purchase intent, review quality, sentiment, and engagement depth are the most important signals for identifying high-intent leads.

---

## 9. Recommendation Strategy Design

The project then used the lead scoring output to design recommendation strategies.

Three strategies were created:

### 9.1 Popularity-Based Recommendation

This strategy recommends products based mainly on historical popularity. It is simple and easy to explain, but it can over-concentrate recommendations around a small number of products.

### 9.2 Category-Preference Recommendation

This strategy uses the user's preferred category and recommends products from that category. It is more personalised than pure popularity ranking, but it still does not fully consider user intent or seller reliability.

### 9.3 Intent-Aware Recommendation

This strategy combines multiple signals:

- user model lead score;
- user high-intent rate;
- preferred product category;
- product high-intent rate;
- product review score;
- seller review score;
- seller late delivery rate.

The recommendation strategy summary showed:

| Strategy | Recommendations | Unique Products | Unique Sellers | Avg Recommendation Score | Product Diversity Rate |
|---|---:|---:|---:|---:|---:|
| intent_aware | 5,000 | 10 | 8 | 0.9871 | 0.20% |
| popularity_based | 5,000 | 2 | 2 | 0.8567 | 0.04% |
| category_preference | 5,000 | 105 | 83 | 0.4821 | 2.10% |

The intent-aware strategy achieved the highest average recommendation score. However, it also recommended only 10 unique products and 8 unique sellers in the sampled output. This is a useful finding because it shows a common trade-off in recommendation systems: improving relevance can reduce diversity if no diversity constraint is added.

A stronger future version should balance relevance, product diversity, seller exposure, and customer experience.

---

## 10. Simulated A/B Test Evaluation

A simulated A/B test was created to compare the popularity-based recommendation strategy with the intent-aware recommendation strategy.

The experiment design was:

| Group | Strategy | Sample Size |
|---|---|---:|
| Control | Popularity-based recommendation | 5,000 users |
| Treatment | Intent-aware recommendation | 5,000 users |

The simulated outcomes were:

| Metric | Control | Treatment | Absolute Difference | Uplift |
|---|---:|---:|---:|---:|
| CTR | 19.42% | 22.76% | +3.34 pp | +17.2% |
| Inquiry Rate | 12.70% | 16.32% | +3.62 pp | +28.5% |
| Purchase Rate | 10.32% | 13.56% | +3.24 pp | +31.4% |
| Revenue per User | 9.10 | 13.18 | +4.08 | +44.9% |
| Total Revenue | 45,485.40 | 65,898.25 | +20,412.85 | +44.9% |

Statistical tests were also applied:

| Metric | Test Type | Test Statistic | P-Value | Significant at 0.05 |
|---|---|---:|---:|---|
| CTR | Two-proportion z-test | 4.0937 | 0.000042 | Yes |
| Inquiry Rate | Two-proportion z-test | 5.1391 | 0.000000 | Yes |
| Purchase Rate | Two-proportion z-test | 4.9960 | 0.000001 | Yes |
| Revenue per User | Welch's t-test | 5.8613 | 0.000000 | Yes |

Under the simulated design, the treatment group outperformed the control group across engagement, conversion, and revenue metrics.

These results should be read as an experiment design demonstration. They show how to compare recommendation strategies and test statistical significance, but they are not live production results.

---

## 11. Tableau Dashboard Design

Three Tableau dashboards were created for stakeholder communication.

### Dashboard 1: Executive Overview

This dashboard provides a business overview of marketplace performance. It includes total GMV, orders, users, products, sellers, category performance, seller performance, and commercial trends.

### Dashboard 2: User Intent & Lead Quality

This dashboard focuses on intent classification and lead quality. It shows intent category distribution, lead score patterns, user value segments, high-intent lead rates, and category-level lead quality.

### Dashboard 3: Recommendation A/B Test Performance

This dashboard compares the control and treatment groups in the simulated A/B test. It shows CTR, inquiry rate, purchase rate, revenue per user, total revenue, uplift, and statistical test outputs.

Dashboard links are available in `dashboard/tableau_links.md`.

---

## 12. Key Findings

The project produced five main findings.

First, the marketplace has strong category concentration. A small number of categories, including health_beauty, watches_gifts, bed_bath_table, sports_leisure, and computers_accessories, contribute a large share of GMV.

Second, delivery delay has a major impact on customer satisfaction. Late deliveries had a much lower review score and a much higher negative review rate than non-late deliveries.

Third, user intent segmentation provides more business context than review score alone. For example, price_sensitive users generated BRL 6.69M in GMV and had a high-intent rate of 92.59%.

Fourth, lead scoring can help translate behaviour, sentiment, delivery, and value signals into a prioritisation framework for customer targeting.

Fifth, the simulated A/B test suggests that intent-aware recommendations can outperform popularity-based recommendations when the recommendation logic considers lead quality, product quality, seller reliability, and user preference.

---

## 13. Limitations

This project has several important limitations.

The original Olist dataset does not include real clickstream data. Events such as view, click, add-to-cart, and inquiry were simulated. The funnel should therefore be interpreted as a simulated engagement funnel rather than a real acquisition funnel.

The source data is based on completed transactions. It does not include a full population of non-converted users. This limits the ability to build a true conversion prediction model.

The intent classification is rule-based and LLM-inspired. It does not use a real LLM API. This was done intentionally to keep the project reproducible and explainable.

The lead scoring model has target leakage because the target label was created from business rules and the model features are closely related to those rules. The model should be interpreted as an automation layer, not a production predictive model.

The A/B test is simulated. The results demonstrate experiment design and evaluation logic, but they do not represent a live platform experiment.

The recommendation strategy does not yet include diversity, fairness, or inventory constraints. The intent-aware strategy produced strong simulated performance but low product and seller diversity.

---

## 14. Future Improvements

A future version of the project could add simulated non-purchase sessions. This would allow the funnel to include users who drop off at view, click, add-to-cart, or inquiry stages before purchase.

If real clickstream data were available, the lead scoring model could be rebuilt as a true predictive model using historical user sessions and future conversion labels.

The recommendation strategy could be improved by adding diversity constraints, category coverage rules, seller exposure controls, and cold-start handling for new products and sellers.

The intent classification layer could also be upgraded by using an actual language model to classify review text and compare model-generated intent labels against the current rule-based labels.

Finally, the A/B testing section could be expanded with power analysis, minimum detectable effect calculation, and experiment duration planning.

---

## 15. Conclusion

This project demonstrates a complete analytics workflow for lead generation and recommendation strategy evaluation. It starts from raw e-commerce data, builds clean analytical tables, uses SQL to understand business performance, simulates a user engagement funnel, classifies customer intent, builds a lead scoring framework, designs recommendation strategies, and evaluates the recommendation strategy through a simulated A/B test.

The main business conclusion is that recommendation decisions should not rely only on product popularity. Customer intent, delivery reliability, product quality, seller quality, and user value segment can all provide useful signals for targeting high-intent users.

The project is strongest as a portfolio case study for data analytics, product analytics, and growth analytics roles. It shows not only technical skills in Python, SQL, modelling, and Tableau, but also the ability to connect data work to business decisions.
