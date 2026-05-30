# Data Dictionary

This document explains the main datasets and fields used in the AI-Powered Lead Generation & Recommendation Analytics project.

The project uses the public Olist Brazilian e-commerce dataset and extends it with engineered analytical tables for synthetic event generation, intent classification, lead scoring, recommendation strategy design, and synthetic A/B test evaluation.

---

## 1. Raw Data Tables

### `olist_customers_dataset.csv`

| Field | Description |
|---|---|
| `customer_id` | Order-level customer identifier |
| `customer_unique_id` | Unique customer identifier across orders |
| `customer_zip_code_prefix` | Customer zip code prefix |
| `customer_city` | Customer city |
| `customer_state` | Customer state |

### `olist_orders_dataset.csv`

| Field | Description |
|---|---|
| `order_id` | Unique order identifier |
| `customer_id` | Customer identifier linked to the order |
| `order_status` | Order status, such as delivered or cancelled |
| `order_purchase_timestamp` | Timestamp when the order was placed |
| `order_approved_at` | Timestamp when the order was approved |
| `order_delivered_carrier_date` | Timestamp when the order was delivered to the carrier |
| `order_delivered_customer_date` | Timestamp when the order was delivered to the customer |
| `order_estimated_delivery_date` | Estimated delivery date |

### `olist_order_items_dataset.csv`

| Field | Description |
|---|---|
| `order_id` | Order identifier |
| `order_item_id` | Item sequence within an order |
| `product_id` | Product identifier |
| `seller_id` | Seller identifier |
| `shipping_limit_date` | Shipping deadline |
| `price` | Product price |
| `freight_value` | Freight cost |

### `olist_order_payments_dataset.csv`

| Field | Description |
|---|---|
| `order_id` | Order identifier |
| `payment_sequential` | Payment sequence number for the order |
| `payment_type` | Payment method, such as credit card, boleto, voucher, or debit card |
| `payment_installments` | Number of payment instalments |
| `payment_value` | Payment amount |

### `olist_order_reviews_dataset.csv`

| Field | Description |
|---|---|
| `review_id` | Review identifier |
| `order_id` | Order identifier linked to the review |
| `review_score` | Customer review score from 1 to 5 |
| `review_comment_title` | Review title text |
| `review_comment_message` | Review message text |
| `review_creation_date` | Review creation date |
| `review_answer_timestamp` | Timestamp when the review was answered |

### `olist_products_dataset.csv`

| Field | Description |
|---|---|
| `product_id` | Product identifier |
| `product_category_name` | Product category in Portuguese |
| `product_name_lenght` | Length of product name in characters |
| `product_description_lenght` | Length of product description in characters |
| `product_photos_qty` | Number of product photos |
| `product_weight_g` | Product weight in grams |
| `product_length_cm` | Product length in centimetres |
| `product_height_cm` | Product height in centimetres |
| `product_width_cm` | Product width in centimetres |

### `olist_sellers_dataset.csv`

| Field | Description |
|---|---|
| `seller_id` | Seller identifier |
| `seller_zip_code_prefix` | Seller zip code prefix |
| `seller_city` | Seller city |
| `seller_state` | Seller state |

### `product_category_name_translation.csv`

| Field | Description |
|---|---|
| `product_category_name` | Product category in Portuguese |
| `product_category_name_english` | Product category translated into English |

### `olist_geolocation_dataset.csv`

| Field | Description |
|---|---|
| `geolocation_zip_code_prefix` | Zip code prefix |
| `geolocation_lat` | Latitude |
| `geolocation_lng` | Longitude |
| `geolocation_city` | City |
| `geolocation_state` | State |

---

## 2. Processed Data Table

### `data/processed/clean_order_base.csv`

This is the main cleaned order-level analytical table. It combines order, customer, product, seller, payment, review, and delivery information.

| Field | Description |
|---|---|
| `order_id` | Unique order identifier |
| `customer_id` | Order-level customer identifier |
| `user_id` | Unique user identifier, derived from `customer_unique_id` |
| `product_id` | Product identifier |
| `seller_id` | Seller identifier |
| `order_time` | Timestamp when the order was placed |
| `order_status` | Order status |
| `price` | Product price |
| `freight_value` | Freight cost |
| `payment_value` | Payment amount |
| `payment_type` | Payment method |
| `payment_installments` | Number of payment instalments |
| `category` | Product category in English |
| `product_name_length` | Length of product name |
| `product_description_length` | Length of product description |
| `product_photos_qty` | Number of product photos |
| `seller_city` | Seller city |
| `seller_state` | Seller state |
| `customer_city` | Customer city |
| `customer_state` | Customer state |
| `review_score` | Customer review score from 1 to 5 |
| `review_comment_title` | Review title text |
| `review_comment_message` | Review message text |
| `order_delivered_customer_date` | Actual customer delivery date |
| `order_estimated_delivery_date` | Estimated delivery date |
| `order_date` | Date part of order timestamp |
| `order_year` | Order year |
| `order_month` | Order month in `YYYY-MM` format |
| `gmv` | Gross merchandise value, calculated as product price plus freight value |
| `delivery_delay_days` | Actual delivery date minus estimated delivery date, measured in days |
| `late_delivery_flag` | 1 if delivery was later than the estimated date; otherwise 0 |
| `price_band` | Product price segment, such as Low, Medium, Premium, or Luxury |

---

## 3. Final Analytical Tables

### `data/final/fact_user_events.csv`

This table contains synthetic user interaction events used for full-funnel analysis. The event pipeline reconstructs a realistic engagement journey from `view` to `click`, `add_to_cart`, `inquiry`, and `purchase` using reproducible business rules.

| Field | Description |
|---|---|
| `user_id` | Unique user identifier |
| `session_id` | Synthetic session identifier |
| `event_time` | Synthetic event timestamp |
| `event_type` | Synthetic event type: view, click, add_to_cart, inquiry, or purchase |
| `order_id` | Related order identifier |
| `product_id` | Related product identifier |
| `seller_id` | Related seller identifier |
| `category` | Product category |
| `device_type` | Synthetic device type, such as Web, iOS, or Android |
| `traffic_source` | Synthetic traffic source, such as For You Feed, Live Stream, Search, Shop Tab, or Creator Profile |
| `price` | Product price |
| `gmv` | GMV attached to the event. Non-purchase events may have zero GMV |
| `review_score` | Review score linked to the order |
| `user_value_segment` | User value segment based on purchase value |
| `event_date` | Date part of the event timestamp |

### `data/final/fact_reviews_llm.csv`

This table contains rule-based, LLM-inspired customer intent classification and lead scoring outputs. It combines review text, fulfilment signals, user engagement depth, and transaction value into structured lead-quality features.

| Field | Description |
|---|---|
| `order_id` | Order identifier |
| `user_id` | Unique user identifier |
| `product_id` | Product identifier |
| `seller_id` | Seller identifier |
| `category` | Product category |
| `order_time` | Order timestamp |
| `price` | Product price |
| `price_band` | Product price segment |
| `gmv` | Gross merchandise value |
| `review_score` | Customer review score |
| `review_text` | Review text used for intent classification. Missing text is handled with a placeholder |
| `delivery_delay_days` | Delivery delay in days |
| `late_delivery_flag` | Late delivery indicator |
| `traffic_source` | Synthetic traffic source |
| `device_type` | Synthetic device type |
| `user_value_segment` | User value segment |
| `total_events` | Number of synthetic events linked to the order or user journey |
| `viewed` | 1 if the user had a synthetic view event; otherwise 0 |
| `clicked` | 1 if the user had a synthetic click event; otherwise 0 |
| `added_to_cart` | 1 if the user had a synthetic add-to-cart event; otherwise 0 |
| `inquired` | 1 if the user had a synthetic inquiry event; otherwise 0 |
| `purchased` | 1 if the user had a purchase event; otherwise 0 |
| `sentiment` | Rule-based sentiment label: positive, neutral, or negative |
| `intent_category` | Rule-based customer intent category |
| `purchase_intent` | Purchase intent level: low, medium, or high |
| `lead_score` | Rule-based lead score from 0 to 100 |
| `high_intent_flag` | 1 if the record is classified as high-intent; otherwise 0 |

### `data/final/fact_lead_scores.csv`

This table extends `fact_reviews_llm.csv` with model-based lead scoring outputs.

| Field | Description |
|---|---|
| `model_high_intent_probability` | Model-estimated probability that the record belongs to the high-intent class |
| `model_lead_score` | Model probability converted into a score from 0 to 100 |
| `model_high_intent_prediction` | Binary model prediction for high-intent lead |

All other fields are inherited from `fact_reviews_llm.csv`.

### `data/final/fact_recommendations.csv`

This table contains recommendation candidates generated by three strategies: popularity-based, category-preference-based, and intent-aware recommendation.

| Field | Description |
|---|---|
| `user_id` | Unique user identifier |
| `user_value_segment` | User value segment |
| `preferred_category` | User's preferred product category based on historical records |
| `strategy` | Recommendation strategy name |
| `recommended_product_id` | Recommended product identifier |
| `recommended_seller_id` | Recommended seller identifier |
| `recommended_category` | Category of the recommended product |
| `recommendation_score` | Score used to rank recommendation candidates |
| `product_avg_price` | Average price of the recommended product |
| `product_avg_review_score` | Average review score of the recommended product |
| `product_high_intent_rate` | Historical high-intent rate for the product |
| `seller_avg_review_score` | Average review score for the recommended seller |
| `seller_late_delivery_rate` | Late delivery rate for the recommended seller |
| `user_avg_model_lead_score` | Average model lead score for the user |
| `user_high_intent_rate` | Historical high-intent rate for the user |
| `experiment_group` | Group assignment used for synthetic experiment design |
| `recommendation_date` | Recommendation date |

### `data/final/fact_recommendation_experiment.csv`

This table contains synthetic A/B test outcomes for the recommendation experiment.

| Field | Description |
|---|---|
| `click_probability` | Synthetic probability that the user clicks the recommendation |
| `inquiry_probability` | Synthetic probability that the user makes an inquiry |
| `purchase_probability` | Synthetic probability that the user purchases |
| `clicked` | Synthetic click outcome: 1 if clicked, otherwise 0 |
| `inquired` | Synthetic inquiry outcome: 1 if inquired, otherwise 0 |
| `purchased` | Synthetic purchase outcome: 1 if purchased, otherwise 0 |
| `revenue` | Synthetic revenue from the recommendation outcome |

All recommendation fields from `fact_recommendations.csv` are also included.

---

## 4. Main Output Tables

### Business KPI Outputs

| Output Table | Description |
|---|---|
| `overall_kpi_summary.csv` | Overall orders, users, products, sellers, GMV, average order value, and average review score |
| `monthly_gmv_trend.csv` | Monthly GMV, order count, user count, and average order value |
| `category_performance.csv` | Category-level order volume, users, sellers, GMV, average order value, and review score |
| `top_sellers_by_gmv.csv` | Top sellers ranked by GMV |
| `category_seller_matrix.csv` | Category and seller-level performance matrix |
| `payment_method_analysis.csv` | Payment method performance by orders, GMV, instalments, and review score |
| `customer_value_analysis.csv` | Customer-level value summary |
| `category_review_score.csv` | Category-level review quality summary |
| `delivery_delay_impact.csv` | Delivery delay impact on review score and negative review rate |

### Funnel Outputs

| Output Table | Description |
|---|---|
| `funnel_summary.csv` | Overall synthetic event funnel by stage |
| `daily_funnel_trend.csv` | Daily synthetic event funnel trend |
| `category_funnel_performance.csv` | Funnel performance by product category |
| `user_segment_funnel.csv` | Funnel performance by user value segment |
| `traffic_source_funnel.csv` | Funnel performance by synthetic engagement source |

### Intent and Lead Scoring Outputs

| Output Table | Description |
|---|---|
| `intent_distribution.csv` | Sentiment and purchase intent distribution |
| `intent_category_summary.csv` | Intent category-level lead score, high-intent rate, and GMV |
| `lead_score_by_category.csv` | Lead score performance by product category |
| `lead_score_by_user_segment.csv` | Lead score performance by user value segment |
| `seller_lead_quality.csv` | Seller-level lead quality and funnel performance |

### Recommendation Outputs

| Output Table | Description |
|---|---|
| `recommendation_strategy_summary.csv` | Comparison of recommendation strategies by score, diversity, product quality, and seller quality |
| `recommendation_category_summary.csv` | Recommendation performance by strategy and category |
| `recommendation_user_level.csv` | User-level recommendation summary |

### A/B Test Outputs

| Output Table | Description |
|---|---|
| `ab_test_summary.csv` | Synthetic A/B test summary by experiment group |
| `ab_test_uplift_summary.csv` | Uplift comparison between control and treatment groups |
| `ab_test_significance.csv` | Statistical test results for CTR, inquiry rate, purchase rate, and revenue per user |
| `ab_test_category_summary.csv` | A/B test results by recommended category |
| `ab_test_segment_summary.csv` | A/B test results by user value segment |

### Model Result Outputs

| Output Table | Description |
|---|---|
| `lead_scoring_model_metrics.csv` | Classification metrics for Logistic Regression and Random Forest |
| `lead_scoring_feature_importance.csv` | Feature importance from the lead scoring model |
| `lead_score_model_summary_by_segment.csv` | Model-based lead score summary by user value segment |


> **Note on LLM-inspired fields:**  
> The current version uses transparent rule-based and LLM-inspired logic to simulate how customer intent and seller next-best-action recommendations could be structured in a production LLM workflow. It does not call a live LLM API. In a production environment, this layer could be replaced or enhanced with an LLM service for intent extraction, reason generation, and seller message personalisation.
### LLM-Inspired Seller Action Outputs

#### `outputs/tables/llm_seller_action_recommendations.csv`

This table converts recommendation outputs, lead scoring results, customer intent signals, and seller-level context into seller-facing next-best-action recommendations.

| Field | Description |
|---|---|
| `user_id` | User identifier used for lead and recommendation matching |
| `recommended_product_id` | Product recommended to the user |
| `recommended_seller_id` | Seller associated with the recommended product |
| `recommended_category` | Product category of the recommended item |
| `preferred_category` | User's preferred or historically inferred product category |
| `strategy` | Recommendation strategy used, such as popularity-based, category-preference, or intent-aware |
| `experiment_group` | A/B test group assigned to the recommendation |
| `recommendation_score` | Ranking score from the recommendation strategy |
| `product_avg_price` | Average price of the recommended product |
| `product_avg_review_score` | Average review score of the recommended product |
| `product_high_intent_rate` | Share of high-intent users associated with the product |
| `seller_avg_review_score` | Average review score of the recommended seller |
| `seller_late_delivery_rate` | Seller-level late delivery rate |
| `user_value_segment` | User value segment, such as High Value, Medium Value, or Low Value |
| `traffic_source` | Simulated or assigned traffic acquisition source |
| `device_type` | Simulated or assigned user device type |
| `intent_category` | Customer intent category used to guide seller action logic |
| `purchase_intent` | Purchase intent label, such as low, medium, or high |
| `lead_score` | User-level lead score from the rule-based scoring layer |
| `model_lead_score` | Model-derived lead score proxy |
| `model_high_intent_probability` | Estimated probability that the user is a high-intent lead |
| `high_intent_flag` | Binary flag indicating whether the user is classified as high intent |
| `seller_action_type` | Recommended seller action type |
| `seller_action_priority` | Priority level of the recommended seller action |
| `seller_action_message` | Seller-facing next-best-action message |
| `llm_style_explanation` | Human-readable explanation of why the seller action is recommended |
| `recommendation_date` | Date when the recommendation record was generated |

#### `outputs/tables/llm_seller_action_summary.csv`

This table summarises seller action recommendations by customer intent and action type.

| Field | Description |
|---|---|
| `intent_category` | Customer intent category |
| `seller_action_type` | Recommended seller action type |
| `seller_action_priority` | Priority level of the action |
| `action_count` | Number of recommendations assigned to this action group |
| `avg_lead_score` | Average lead score within the action group |
| `avg_recommendation_score` | Average recommendation score within the action group |

---
## 5. Key Derived Fields

| Field | Description |
|---|---|
| `gmv` | Gross merchandise value, calculated as product price plus freight value |
| `delivery_delay_days` | Difference between actual delivery date and estimated delivery date |
| `late_delivery_flag` | 1 if delivery was late; otherwise 0 |
| `price_band` | Price segment assigned based on product price |
| `user_value_segment` | User segment based on customer purchase value |
| `traffic_source` | Synthetic acquisition or engagement source |
| `device_type` | Synthetic user device type |
| `event_type` | Synthetic user journey event type |
| `sentiment` | Rule-based review sentiment label |
| `intent_category` | Rule-based, LLM-inspired customer intent segment |
| `purchase_intent` | Low, medium, or high purchase intent level |
| `lead_score` | Rule-based lead score from 0 to 100 |
| `high_intent_flag` | Binary high-intent label derived from business rules |
| `model_high_intent_probability` | Model-estimated probability of high-intent classification |
| `model_lead_score` | Model-generated lead score from 0 to 100 |
| `recommendation_score` | Ranking score for recommendation candidate selection |
| `experiment_group` | Control or treatment group in the synthetic AB test |
| `clicked` | Synthetic click outcome |
| `inquired` | Synthetic inquiry outcome |
| `purchased` | Synthetic purchase outcome |
| `revenue` | Synthetic revenue generated in the A/B test |

---

## 6. Notes on Synthetic Data Generation

To bridge the gap between static transaction records and full-funnel product analytics, several behavioural and experiment fields were generated using a business-driven synthetic data pipeline. This design allows the project to move beyond order-level reporting and support lead scoring, funnel analysis, recommendation evaluation, and dashboard storytelling.

Synthetic fields include:

- Event identifiers: `session_id`, `event_time`, `event_type`
- Acquisition and device attributes: `traffic_source`, `device_type`
- Funnel behaviour flags: `viewed`, `clicked`, `added_to_cart`, `inquired`, `purchased`
- Experiment outcome fields: `click_probability`, `inquiry_probability`, `purchase_probability`, `clicked`, `inquired`, `purchased`, `revenue`

The A/B test table contains synthetic experiment outcomes used to compare popularity-based and intent-aware recommendation strategies. Key outcome fields include `clicked`, `inquired`, `purchased`, and `revenue`.

Rather than treating the absence of real clickstream logs as a blocker, these fields were built on reproducible business logic and probabilistic generation rules. The synthetic data layer creates a realistic marketplace environment for demonstrating advanced product analytics workflows, including full-funnel conversion analysis, high-intent lead identification, recommendation strategy comparison, and experiment evaluation.

In a production environment, these synthetic fields would be replaced or calibrated with real platform event logs, live recommendation exposure records, and observed conversion outcomes.
