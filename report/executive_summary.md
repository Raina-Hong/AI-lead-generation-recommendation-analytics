# Executive Summary: AI-Powered Recommendation & Lead Analytics

## The Bottom Line

This project shows that moving beyond popularity-based recommendation can create measurable commercial upside. By engineering an intent-aware recommendation strategy on top of **96,478 e-commerce orders**, the experiment framework achieved a **+44.9% incremental lift in revenue per user** and a **+31.4% increase in purchase rate** compared with a popularity-based baseline.

In simple terms: better intent signals led to better recommendations, and better recommendations drove stronger full-funnel outcomes.

---

## Core Business Problem and Solution

### The Problem

Marketplace platforms often rely on popularity-based recommendation because it is easy to implement and explain. However, popularity alone misses several important signals:

- whether the customer is showing strong purchase intent;
- whether the product category matches the customer's likely needs;
- whether the seller can fulfil the order reliably;
- whether operational issues, such as delivery delay, may damage conversion and satisfaction.

This creates a common growth problem: high-potential customers may receive generic recommendations, while products with strong intent fit may be underused.

### The Solution

I designed an end-to-end lead and recommendation analytics workflow using the public Olist Brazilian e-commerce dataset. The workflow converts static transaction records into a more decision-ready commercial system by combining customer intent, behavioural depth, review sentiment, product quality, seller reliability, and recommendation testing.

The final output is not just a dashboard. It is a business logic framework that shows how a marketplace could identify high-intent leads, prioritise better recommendation candidates, and evaluate incremental lift against a simple baseline.

---

## Technical Pillars

### 1. Synthetic Event Generation

The original dataset contains completed transaction records, but not frontend behavioural events. To bridge that gap, I built a synthetic event pipeline that reconstructs a full-funnel journey around marketplace activity, including view, click, add-to-cart, inquiry, and purchase stages.

This step makes the project more than static order reporting. It creates the behavioural layer needed for lead scoring, funnel analysis, and recommendation evaluation.

### 2. Rule-Based Intent Engine

I engineered a transparent intent classification layer using review text, review score, delivery delay, behavioural signals, and customer value segment. The goal was to turn raw customer and order data into business-readable intent categories such as ready to purchase, price sensitive, delivery concern, and product quality concern.

This approach keeps the logic explainable. Business stakeholders can see why a user is treated as a high-intent lead instead of relying on a black-box score.

### 3. Lead Scoring and Rule Automation

The lead scoring layer translates intent, engagement, customer value, and experience quality into prioritisation signals. A proxy machine learning model was then used to automate and validate the scoring logic, helping confirm which features were most aligned with high-intent lead identification.

The purpose here was practical: make the lead framework repeatable, structured, and ready to evolve into a real-time scoring service when live behavioural data becomes available.

### 4. Intent-Aware Recommendation Evaluation

I compared a popularity-based baseline with an intent-aware recommendation strategy. The treatment strategy combined user intent, product quality, seller performance, and lead quality signals to rank recommendation candidates.

The experiment showed that relevance based on intent can outperform popularity alone, especially at deeper funnel stages where purchase and revenue matter most.

---

## Key Commercial Results

### A/B Test Results: Intent-Aware vs. Popularity Baseline

The intent-aware strategy generated statistically significant full-funnel growth across engagement, inquiry, purchase, and revenue metrics.

| Metric | Control: Popularity-Based | Treatment: Intent-Aware | Incremental Lift | Significance |
|---|---:|---:|---:|:---:|
| **CTR** | 19.42% | 22.76% | **+17.2%** | ✅ p < 0.05 |
| **Inquiry Rate** | 12.70% | 16.32% | **+28.5%** | ✅ p < 0.05 |
| **Purchase Rate** | 10.32% | 13.56% | **+31.4%** | ✅ p < 0.05 |
| **Revenue per User** | 9.10 | 13.18 | **+44.9%** | ✅ p < 0.05 |

The strongest improvement appeared in revenue per user, not only click-through rate. That is important because it suggests the strategy improves commercial quality, not just surface-level engagement.

---

## Key Commercial Insights

### 1. Delivery reliability is a conversion and satisfaction bottleneck

Late delivery had a clear negative relationship with customer satisfaction. Non-late deliveries had an average review score of **4.21** and a negative review rate of **11.32%**. Late deliveries had an average review score of only **2.33**, while the negative review rate increased to **61.32%**.

**Business implication:** seller reliability should be part of recommendation ranking. Promoting products from sellers with weak fulfilment performance may increase short-term clicks, but it can hurt customer trust and post-purchase satisfaction.

### 2. Price-sensitive users are not low-value users

The price-sensitive segment generated **BRL 6.69M GMV**, making it one of the most commercially important intent groups. This shows that price sensitivity should not automatically lead to deprioritisation.

**Business implication:** price-sensitive users should be handled with targeted pricing actions, such as shipping incentives, bundles, limited-time offers, or value-based messaging. The goal is not to discount blindly, but to activate users who already show strong intent.

### 3. High-GMV categories are natural testing grounds

The strongest GMV categories included **Health Beauty**, **Watches Gifts**, **Bed Bath Table**, **Sports Leisure**, and **Computers Accessories**. Health Beauty alone generated around **BRL 1.41M GMV**.

**Business implication:** recommendation experiments should start in categories with both strong demand and enough transaction volume. This increases the chance that small improvements in conversion translate into meaningful commercial impact.

### 4. Recommendation performance needs diversity guardrails

The intent-aware strategy improved conversion and revenue metrics, but product diversity still needs to be managed. A strong production system should balance relevance with catalog exposure, seller fairness, and long-term customer experience.

**Business implication:** the next version should include diversity-aware re-ranking so that incremental lift does not come at the cost of overly narrow product exposure or internal traffic cannibalization.

---

## Path to Production

To turn this analytical framework into a live recommendation and lead scoring engine, the next engineering steps would be:

1. **Integrate real-time clickstream events**  
   Add live product views, clicks, add-to-cart events, session duration, search terms, and non-converted sessions.

2. **Deploy an intent scoring API**  
   Package the intent and lead scoring logic into a real-time service that can return lead quality scores during user sessions.

3. **Replace rule-based text logic with LLM-assisted review understanding**  
   Use a large language model to extract more nuanced signals from review text, such as urgency, dissatisfaction reason, product concern, and purchase motivation.

4. **Add diversity-aware re-ranking guardrails**  
   Balance relevance with catalog exposure, seller fairness, and category diversity to reduce concentration risk and traffic cannibalization.

5. **Run a production A/B test**  
   Validate the framework with live users, real conversion labels, and guardrail metrics such as refund rate, delivery satisfaction, repeat purchase rate, and seller exposure distribution.

---

## Final Takeaway

This project demonstrates how transaction data can be transformed into a practical lead generation and recommendation analytics framework. The strongest result is clear: an intent-aware strategy produced stronger full-funnel performance than a popularity-based baseline, with **+44.9% revenue per user uplift** and **+31.4% purchase rate uplift**.

The business message is simple: recommendation systems should not only ask what is popular. They should ask who is ready to buy, what they care about, and whether the platform can fulfil the promise after the click.
