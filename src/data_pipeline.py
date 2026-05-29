# src/data_pipeline.py

import pandas as pd
import numpy as np
from typing import Optional
from src.utils import logger


class DataPipeline:

    """
    Pipeline for cleaning Olist transaction data and generating synthetic funnel events.

    Notes
    -----
    The original Olist dataset lacks front-end clickstream logs. To demonstrate a
    TikTok LIVE-style lead generation funnel, this pipeline synthetically generates
    behavioral events (View -> Click -> Cart -> Inquiry -> Purchase) based on
    reproducible business logic. This transforms a static reporting dataset into a
    dynamic product analytics environment.
    """

    def __init__(self, raw_data_path: str = "data/raw/", random_state: int = 42):
        self.raw_data_path = raw_data_path
        self.random_state = random_state
        self.rng = np.random.default_rng(random_state)

    def clean_transactions(
        self,
        orders_df: pd.DataFrame,
        items_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Clean order and item data, then calculate basic transaction-level features.

        Parameters
        ----------
        orders_df : pd.DataFrame
            Raw orders table.
        items_df : pd.DataFrame
            Raw order items table.

        Returns
        -------
        pd.DataFrame
            Cleaned transaction-level table with GMV.
        """
        logger.info("Starting transaction cleaning process...")

        required_order_cols = {"order_id", "order_status", "customer_id"}
        required_item_cols = {"order_id", "product_id", "price", "freight_value"}

        missing_order_cols = required_order_cols - set(orders_df.columns)
        missing_item_cols = required_item_cols - set(items_df.columns)

        if missing_order_cols:
            raise ValueError(f"orders_df is missing required columns: {missing_order_cols}")

        if missing_item_cols:
            raise ValueError(f"items_df is missing required columns: {missing_item_cols}")

        merged_df = pd.merge(
            orders_df,
            items_df,
            on="order_id",
            how="inner"
        )

        merged_df["price"] = pd.to_numeric(merged_df["price"], errors="coerce")
        merged_df["freight_value"] = pd.to_numeric(
            merged_df["freight_value"],
            errors="coerce"
        )

        merged_df["gmv"] = merged_df["price"] + merged_df["freight_value"]

        clean_df = merged_df.dropna(
            subset=[
                "order_id",
                "order_status",
                "customer_id",
                "product_id",
                "price",
                "freight_value",
                "gmv"
            ]
        ).copy()

        logger.info(f"Cleaned transactions shape: {clean_df.shape}")
        return clean_df

    def generate_synthetic_funnel(
        self,
        clean_transactions_df: pd.DataFrame,
        non_purchase_multiplier: float = 0.30
    ) -> pd.DataFrame:
        """
        Generate synthetic behavioural funnel events.

        The method creates two types of sessions:

        1. Purchase sessions based on real orders:
           view -> click -> add_to_cart -> inquiry -> purchase

        2. Non-purchase sessions sampled from existing users and products:
           view/click/add_to_cart/inquiry without purchase

        This makes the simulated funnel more realistic than treating every user
        interaction as a purchase journey.

        Parameters
        ----------
        clean_transactions_df : pd.DataFrame
            Cleaned transaction-level table.
        non_purchase_multiplier : float
            Number of synthetic non-purchase sessions as a proportion of real
            transaction rows. For example, 0.30 means adding non-purchase sessions
            equal to 30% of the number of transaction rows.

        Returns
        -------
        pd.DataFrame
            Synthetic behavioural event log with user_id, product_id, and event_type.
        """
        logger.info("Generating synthetic behavioural funnel...")

        required_cols = {"customer_id", "product_id"}

        missing_cols = required_cols - set(clean_transactions_df.columns)
        if missing_cols:
            raise ValueError(
                f"clean_transactions_df is missing required columns: {missing_cols}"
            )

        events = []

        for _, row in clean_transactions_df.iterrows():
            user_id = row["customer_id"]
            product_id = row["product_id"]

            # Existing orders are treated as completed purchase sessions.
            events.append(
                {"user_id": user_id, "product_id": product_id, "event_type": "view"}
            )

            if self.rng.random() < 0.85:
                events.append(
                    {"user_id": user_id, "product_id": product_id, "event_type": "click"}
                )

            if self.rng.random() < 0.65:
                events.append(
                    {
                        "user_id": user_id,
                        "product_id": product_id,
                        "event_type": "add_to_cart"
                    }
                )

            if self.rng.random() < 0.30:
                events.append(
                    {
                        "user_id": user_id,
                        "product_id": product_id,
                        "event_type": "inquiry"
                    }
                )

            events.append(
                {"user_id": user_id, "product_id": product_id, "event_type": "purchase"}
            )

        # Add synthetic non-purchase sessions to avoid a fully purchase-biased funnel.
        n_non_purchase = int(len(clean_transactions_df) * non_purchase_multiplier)

        if n_non_purchase > 0 and not clean_transactions_df.empty:
            sampled_users = self.rng.choice(
                clean_transactions_df["customer_id"].dropna().unique(),
                size=n_non_purchase,
                replace=True
            )
            sampled_products = self.rng.choice(
                clean_transactions_df["product_id"].dropna().unique(),
                size=n_non_purchase,
                replace=True
            )

            for user_id, product_id in zip(sampled_users, sampled_products):
                events.append(
                    {"user_id": user_id, "product_id": product_id, "event_type": "view"}
                )

                if self.rng.random() < 0.50:
                    events.append(
                        {
                            "user_id": user_id,
                            "product_id": product_id,
                            "event_type": "click"
                        }
                    )

                if self.rng.random() < 0.20:
                    events.append(
                        {
                            "user_id": user_id,
                            "product_id": product_id,
                            "event_type": "add_to_cart"
                        }
                    )

                if self.rng.random() < 0.10:
                    events.append(
                        {
                            "user_id": user_id,
                            "product_id": product_id,
                            "event_type": "inquiry"
                        }
                    )

        funnel_df = pd.DataFrame(events)

        if not funnel_df.empty:
            funnel_df["event_id"] = range(1, len(funnel_df) + 1)

        logger.info(f"Synthetic funnel generated with shape: {funnel_df.shape}")
        return funnel_df


if __name__ == "__main__":
    pipeline = DataPipeline(raw_data_path="data/raw/", random_state=42)

    # Example usage:
    # orders_df = pd.read_csv("data/raw/olist_orders_dataset.csv")
    # items_df = pd.read_csv("data/raw/olist_order_items_dataset.csv")
    # clean_df = pipeline.clean_transactions(orders_df, items_df)
    # funnel_df = pipeline.generate_synthetic_funnel(clean_df)