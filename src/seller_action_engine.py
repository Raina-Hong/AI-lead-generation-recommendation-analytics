"""
Seller Action Engine

This module converts customer intent signals, lead scores, recommendation outputs,
and seller/product quality indicators into seller-facing next-best-action recommendations.

The current implementation uses transparent rule-based and LLM-inspired logic.
It does not call a live LLM API. In a production environment, this layer could be
extended with an LLM service for personalised message generation and explanation.
"""

import pandas as pd
import numpy as np


def safe_get(row, col, default=None):
    """
    Safely read a value from a pandas row.

    Parameters
    ----------
    row : pandas.Series
        A row from a dataframe.
    col : str
        Column name to read.
    default : any
        Default value returned when the column is missing or empty.

    Returns
    -------
    any
        Row value or default value.
    """
    if col in row.index and pd.notna(row[col]):
        return row[col]
    return default


def normalise_text(x):
    """
    Convert text into a lowercase string for rule matching.
    """
    if pd.isna(x):
        return ""
    return str(x).strip().lower()


def assign_seller_action(row):
    """
    Generate a seller-facing next-best-action recommendation.

    The rule order matters:
    1. handle support or negative intent first;
    2. handle delivery, price, and quality concerns;
    3. handle ready-to-purchase users;
    4. handle medium-intent users with personalised follow-up.

    This avoids giving aggressive offers to users with negative or low-intent signals.
    """

    intent = normalise_text(safe_get(row, "intent_category", ""))
    purchase_intent = normalise_text(safe_get(row, "purchase_intent", ""))

    lead_score = float(safe_get(row, "lead_score", 0))
    model_lead_score = float(safe_get(row, "model_lead_score", lead_score))
    user_avg_model_lead_score = float(
        safe_get(row, "user_avg_model_lead_score", model_lead_score)
    )

    late_delivery_flag = int(safe_get(row, "late_delivery_flag", 0))
    seller_late_rate = safe_get(row, "seller_late_delivery_rate", np.nan)
    seller_review_score = safe_get(row, "seller_avg_review_score", np.nan)
    product_review_score = safe_get(row, "product_avg_review_score", np.nan)

    effective_score = max(lead_score, model_lead_score, user_avg_model_lead_score)

    action_type = "nurture_with_general_content"
    priority = "Medium"
    message = "Send a light product reminder and highlight the main product benefits."
    explanation = (
        "The user does not show a highly specific intent signal. "
        "A softer nurturing message is more suitable than an aggressive sales push."
    )

    if any(word in intent for word in ["support", "after", "return", "refund", "service"]) or intent == "after_sales_issue":
        action_type = "offer_customer_support"
        priority = "Medium"
        message = "Provide customer support, return guidance, warranty information, or service follow-up."
        explanation = (
            "The user may need service reassurance. "
            "A support-oriented follow-up is more appropriate than a hard selling message."
        )

    elif intent == "general_negative":
        action_type = "nurture_with_general_content"
        priority = "Medium"
        message = "Send a soft trust-building message and avoid aggressive promotion."
        explanation = (
            "The user shows a negative or unclear signal. "
            "The seller should rebuild trust before sending conversion-oriented offers."
        )

    elif any(word in intent for word in ["delivery", "logistics", "shipping"]) or late_delivery_flag == 1:
        action_type = "highlight_delivery_reliability"
        priority = "High" if effective_score >= 70 else "Medium"
        message = "Highlight estimated delivery time, return policy, and reliable fulfilment information."
        explanation = (
            "The user may be concerned about delivery or fulfilment. "
            "The seller should reduce delivery anxiety before pushing for purchase."
        )

    elif any(word in intent for word in ["price", "discount", "cost", "value"]) or intent == "price_sensitive":
        action_type = "send_discount_or_bundle"
        priority = "High" if effective_score >= 70 else "Medium"
        message = "Offer a small discount, free shipping, or a bundle deal to reduce price hesitation."
        explanation = (
            "The user appears to be price-sensitive. "
            "A value-focused offer is more useful than a generic product message."
        )

    elif any(word in intent for word in ["quality", "review", "trust", "defect"]) or intent == "product_quality_concern":
        action_type = "show_social_proof"
        priority = "Medium"
        message = "Show customer reviews, product details, usage examples, and after-sales support."
        explanation = (
            "The user may need more confidence in product quality. "
            "Reviews and product evidence can help build trust."
        )

    elif intent == "ready_to_purchase" or purchase_intent == "high":
        action_type = "send_limited_time_offer"
        priority = "High" if effective_score >= 70 else "Medium"
        message = "Send a limited-time offer with a clear call-to-action and a fast checkout link."
        explanation = (
            "The user shows strong purchase intent. "
            "The seller should prioritise direct conversion with a clear offer."
        )

    elif intent == "comparison_shopping":
        action_type = "show_social_proof"
        priority = "Medium"
        message = "Highlight product advantages, customer reviews, and seller credibility."
        explanation = (
            "The user may be comparing alternatives. "
            "The seller should focus on differentiation and trust-building."
        )

    elif effective_score >= 65:
        action_type = "personalised_product_follow_up"
        priority = "Medium"
        message = "Recommend a relevant product based on the user's preferred category and recent engagement."
        explanation = (
            "The user has a reasonable lead score, but the intent is not very specific. "
            "A personalised follow-up can help move the user closer to purchase."
        )

    warnings = []

    if pd.notna(seller_late_rate) and seller_late_rate > 0.20:
        warnings.append(
            "Seller late delivery risk is relatively high, so fulfilment reliability should be monitored."
        )

    if pd.notna(seller_review_score) and seller_review_score < 3.5:
        warnings.append(
            "Seller average review score is below the ideal level, so exposure should be used carefully."
        )

    if pd.notna(product_review_score) and product_review_score < 3.5:
        warnings.append(
            "The recommended product has a relatively low review score, so social proof may be needed."
        )

    if warnings:
        explanation = explanation + " " + " ".join(warnings)

    return pd.Series(
        {
            "seller_action_type": action_type,
            "seller_action_priority": priority,
            "seller_action_message": message,
            "llm_style_explanation": explanation,
        }
    )


def generate_seller_actions(df):
    """
    Apply seller action logic to a recommendation or lead dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing recommendation, intent, lead score, seller, and product signals.

    Returns
    -------
    pandas.DataFrame
        Original dataframe with seller action columns appended.
    """
    action_cols = df.apply(assign_seller_action, axis=1)
    return pd.concat([df.reset_index(drop=True), action_cols.reset_index(drop=True)], axis=1)


def summarise_seller_actions(df):
    """
    Summarise seller actions by intent category, action type, and priority.
    """
    required_cols = [
        "intent_category",
        "seller_action_type",
        "seller_action_priority",
        "lead_score",
        "recommendation_score",
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns for summary: {missing_cols}")

    summary = (
        df.groupby(
            ["intent_category", "seller_action_type", "seller_action_priority"],
            dropna=False,
        )
        .agg(
            action_count=("seller_action_type", "size"),
            avg_lead_score=("lead_score", "mean"),
            avg_recommendation_score=("recommendation_score", "mean"),
        )
        .reset_index()
        .sort_values("action_count", ascending=False)
    )

    return summary