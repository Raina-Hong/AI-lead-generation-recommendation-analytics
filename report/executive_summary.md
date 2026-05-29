# Executive Summary

## Project Objective

This project explores how an e-commerce platform can use transaction data, customer reviews, delivery performance, and simulated behavioural signals to support lead generation and recommendation decisions.

The goal was not to build a production recommendation engine, but to create a complete analytics workflow that shows how a business could identify high-intent customers, prioritise better leads, design more relevant recommendations, and evaluate the expected impact through an A/B testing framework.

The project uses the public Olist Brazilian e-commerce dataset and builds the analysis from raw data to final Tableau dashboards.

---

## Business Context

Marketplace platforms often need to help sellers reach the right customers. A simple popularity-based recommendation approach can work as a baseline, but it does not consider whether a user is likely to buy, whether the product fits the user's category preference, or whether the seller has strong review and delivery performance.

This project addresses that problem by creating an intent-aware recommendation workflow. The workflow combines customer behaviour, review sentiment, delivery reliability, user value segment, product quality, and seller quality into one analytical process.

The project is designed around three questions:

1. Which customers are more likely to become high-intent leads?
2. Which product categories and sellers create stronger commercial value?
3. Can an intent-aware recommendation strategy outperform a popularity-based baseline?

---

## Analytical Approach

The project was completed in seven stages.

First, the raw Olist datasets were cleaned and merged into an order-level analytical table. This table combines orders, customers, products, sellers, payments, reviews, delivery dates, and product category translations.

Second, SQL analysis was used to generate business KPI outputs, including GMV, average order value, category performance, seller performance, review quality, payment method analysis, and delivery delay impact.

Third, a simulated user funnel was created. The original Olist dataset does not include real clickstream data, so user events such as view, click, add-to-cart, inquiry, and purchase were generated using reproducible business assumptions. This gives the project a realistic lead-generation structure while keeping the data limitation clear.

Fourth, a rule-based, LLM-inspired intent classification layer was created. It uses review text, review score, delivery delay, behavioural signals, and customer value segment to assign sentiment, intent category, purchase intent level, and rule-based lead score.

Fifth, Logistic Regression and Random Forest models were trained to automate the lead scoring framework.

Sixth, three recommendation strategies were designed: popularity-based, category-preference-based, and intent-aware recommendation.

Finally, a simulated A/B test was used to compare the popularity-based control group with the intent-aware treatment group.

---

## Key Findings

The cleaned dataset contains 96,478 completed orders, 93,358 unique users, 32,216 products, and 2,970 sellers. Total GMV reached BRL 15.42M, with an average order value of BRL 139.93 and an average review score of 4.09.

The strongest GMV categories were health_beauty, watches_gifts, bed_bath_table, sports_leisure, and computers_accessories. Health_beauty alone generated BRL 1.41M in GMV, followed by watches_gifts at BRL 1.26M and bed_bath_table at BRL 1.23M.

Delivery reliability appeared to be one of the clearest drivers of customer satisfaction. Non-late deliveries had an average review score of 4.21 and a negative review rate of 11.32%. Late deliveries had an average review score of only 2.33, and the negative review rate increased to 61.32%. This suggests that recommendation quality should not be judged only by product popularity. Seller reliability and delivery performance also matter.

The intent classification layer identified ready_to_purchase and price_sensitive users as two important commercial segments. The ready_to_purchase group contained 51,869 records with a 100% high-intent rate. The price_sensitive group generated BRL 6.69M in GMV, which shows that price sensitivity does not necessarily mean low value. These users can still represent strong purchase potential when they show clear behavioural intent.

The simulated A/B test showed that the intent-aware recommendation strategy outperformed the popularity-based baseline across all main metrics:

| Metric | Control | Treatment | Uplift |
|---|---:|---:|---:|
| CTR | 19.42% | 22.76% | +17.2% |
| Inquiry Rate | 12.70% | 16.32% | +28.5% |
| Purchase Rate | 10.32% | 13.56% | +31.4% |
| Revenue per User | 9.10 | 13.18 | +44.9% |

The improvements in CTR, inquiry rate, purchase rate, and revenue per user were statistically significant under the simulated experiment design.

---

## Business Implications

The analysis suggests that a lead generation system should combine intent, product quality, and seller reliability rather than relying only on historical product popularity.

For sellers, this type of workflow could help identify which customers are worth prioritising for outreach, live-stream follow-up, product recommendations, or promotional offers.

For a marketplace platform, the project shows how customer intent signals and operational quality metrics can be translated into a practical recommendation framework. It also shows how an experiment can be structured to test whether a new recommendation logic is likely to improve engagement and commercial outcomes.

---

## Limitations

The original Olist dataset does not contain real clickstream logs, live-stream engagement records, or non-converted user sessions. For that reason, user events, lead scores, recommendation outcomes, and A/B test outcomes were generated using reproducible business assumptions.

The funnel should be understood as a simulated engagement funnel built around observed purchases. It should not be interpreted as a real acquisition funnel covering both converted and non-converted visitors.

The lead scoring model achieved near-perfect performance because the target label was generated from rule-based business logic. The model should therefore be interpreted as an automation layer for the scoring framework, not as evidence of real-world predictive accuracy.

The A/B test is also simulated. It demonstrates how experiment evaluation can be designed, but it does not represent a live production test.

---

## Recommended Next Steps

A stronger future version of this project could add simulated non-purchase sessions so that the funnel includes users who drop off before purchase. This would make the conversion flow more realistic.

The recommendation strategy could also be improved by adding diversity constraints. In the current output, the intent-aware strategy performs strongly on score and simulated conversion, but it recommends a limited number of unique products and sellers. A production-style system would need to balance relevance, seller fairness, product diversity, and customer experience.

If real clickstream data became available, the lead scoring model could be rebuilt as a true predictive model using historical non-converted and converted user sessions.
