# src/recommendation_strategy.py

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from src.utils import logger


class RecommendationSystem:
    """
    System providing baseline and intent-aware recommendation strategies.

    The recommendation logic is designed for offline analytics demonstration:
    - Control group: popularity-based ranking
    - Treatment group: intent-aware recommendation with seller quality and SMB exploration
    """

    def __init__(
        self,
        item_catalog: pd.DataFrame,
        interaction_history: pd.DataFrame,
        random_state: int = 42
    ):
        self.item_catalog = item_catalog.copy()
        self.interaction_history = interaction_history.copy()
        self.random_state = random_state
        self.rng = np.random.default_rng(random_state)

        self._validate_base_inputs()

    def _validate_base_inputs(self) -> None:
        """
        Validate the minimum columns required for recommendation generation.
        """
        if "product_id" not in self.item_catalog.columns:
            raise ValueError("item_catalog must contain a 'product_id' column.")

        required_history_cols = {"product_id", "event_type"}
        missing_history_cols = required_history_cols - set(self.interaction_history.columns)

        if missing_history_cols:
            raise ValueError(
                f"interaction_history is missing required columns: {missing_history_cols}"
            )

    def _has_columns(self, columns: List[str]) -> bool:
        """
        Check whether item_catalog contains all required columns.
        """
        return all(col in self.item_catalog.columns for col in columns)

    def generate_popularity_recs(
        self,
        user_id: str,
        top_k: int = 5
    ) -> List[str]:
        """
        Baseline strategy: recommend globally popular products based on purchase history.

        Parameters
        ----------
        user_id : str
            User identifier. Kept for interface consistency.
        top_k : int
            Number of products to recommend.

        Returns
        -------
        List[str]
            Recommended product IDs.
        """
        purchase_history = self.interaction_history[
            self.interaction_history["event_type"] == "purchase"
        ]

        if purchase_history.empty:
            logger.warning(
                "No purchase events found. Falling back to item catalog order."
            )
            return self.item_catalog["product_id"].head(top_k).tolist()

        popular_items = (
            purchase_history["product_id"]
            .value_counts()
            .head(top_k)
            .index
            .tolist()
        )

        # If fewer than top_k purchased products exist, fill from catalog.
        if len(popular_items) < top_k:
            fallback_items = (
                self.item_catalog[
                    ~self.item_catalog["product_id"].isin(popular_items)
                ]["product_id"]
                .head(top_k - len(popular_items))
                .tolist()
            )
            popular_items.extend(fallback_items)

        logger.debug(f"Generated popularity recommendations for user {user_id}")
        return popular_items

    def _sample_smb_exploration_recs(
        self,
        top_k: int
    ) -> Optional[List[str]]:
        """
        Sample high-quality low-exposure products for SMB exploration.

        Returns None if required columns are not available or no candidate exists.
        """
        required_cols = [
            "seller_sales_volume",
            "seller_review_score",
            "product_id"
        ]

        if not self._has_columns(required_cols):
            return None

        smb_candidates = self.item_catalog[
            (self.item_catalog["seller_sales_volume"] < 100)
            & (self.item_catalog["seller_review_score"] >= 4.5)
        ]

        if smb_candidates.empty:
            return None

        sample_size = min(top_k, len(smb_candidates))

        sampled_indices = self.rng.choice(
            smb_candidates.index,
            size=sample_size,
            replace=False
        )

        return smb_candidates.loc[sampled_indices, "product_id"].tolist()

    def generate_intent_aware_recs(
        self,
        user_id: str,
        user_intent_score: float,
        top_k: int = 5,
        exploration_rate: float = 0.10
    ) -> List[str]:
        """
        Treatment strategy: generate intent-aware recommendations.

        Logic
        -----
        1. With a small exploration probability, recommend high-quality low-exposure
           SMB products.
        2. For high-intent users, recommend high-CVR products from reliable sellers.
        3. For medium-intent users, recommend cost-effective products.
        4. For low-intent users, fall back to popularity-based recommendations.

        Parameters
        ----------
        user_id : str
            User identifier.
        user_intent_score : float
            Lead score between 0 and 1.
        top_k : int
            Number of products to recommend.
        exploration_rate : float
            Probability of applying SMB exploration.

        Returns
        -------
        List[str]
            Recommended product IDs.
        """
        logger.debug(
            f"Generating intent-aware recommendations for user {user_id} "
            f"with score {user_intent_score}"
        )

        if not 0 <= user_intent_score <= 1:
            raise ValueError("user_intent_score must be between 0 and 1.")

        # SMB exploration layer.
        if self.rng.random() < exploration_rate:
            smb_recs = self._sample_smb_exploration_recs(top_k=top_k)
            if smb_recs:
                logger.debug(f"SMB exploration recommendations used for {user_id}")
                return smb_recs

        recs = []

        # High-intent users: recommend high-CVR products from reliable sellers.
        if user_intent_score > 0.8:
            required_cols = [
                "seller_late_rate",
                "historical_cvr",
                "product_id"
            ]

            if self._has_columns(required_cols):
                candidates = self.item_catalog[
                    self.item_catalog["seller_late_rate"] < 0.10
                ]

                if not candidates.empty:
                    recs = (
                        candidates
                        .sort_values(by="historical_cvr", ascending=False)
                        .head(top_k)["product_id"]
                        .tolist()
                    )

            if not recs:
                logger.warning(
                    "High-intent recommendation candidates unavailable. "
                    "Falling back to popularity strategy."
                )
                recs = self.generate_popularity_recs(user_id, top_k)

        # Medium-intent users: recommend cost-effective products.
        elif 0.5 <= user_intent_score <= 0.8:
            required_cols = [
                "price_band",
                "historical_sales",
                "product_id"
            ]

            if self._has_columns(required_cols):
                candidates = self.item_catalog[
                    self.item_catalog["price_band"] == "Low"
                ]

                if not candidates.empty:
                    recs = (
                        candidates
                        .sort_values(by="historical_sales", ascending=False)
                        .head(top_k)["product_id"]
                        .tolist()
                    )

            if not recs:
                logger.warning(
                    "Medium-intent recommendation candidates unavailable. "
                    "Falling back to popularity strategy."
                )
                recs = self.generate_popularity_recs(user_id, top_k)

        # Low-intent users: use conservative popularity-based fallback.
        else:
            recs = self.generate_popularity_recs(user_id, top_k)

        return recs

    def evaluate_ab_test(
        self,
        control_metrics: Dict[str, float],
        treatment_metrics: Dict[str, float]
    ) -> pd.DataFrame:
        """
        Evaluate A/B test effects for recommendation strategies.

        Parameters
        ----------
        control_metrics : Dict[str, float]
            Metrics for the control group.
        treatment_metrics : Dict[str, float]
            Metrics for the treatment group.

        Returns
        -------
        pd.DataFrame
            Table containing metric, control, treatment, absolute delta, and uplift percentage.
        """
        logger.info("Evaluating A/B test results...")

        results = []

        common_metrics = set(control_metrics.keys()) & set(treatment_metrics.keys())

        if not common_metrics:
            raise ValueError(
                "control_metrics and treatment_metrics do not share any metric names."
            )

        for metric in sorted(common_metrics):
            control_value = control_metrics[metric]
            treatment_value = treatment_metrics[metric]

            absolute_delta = treatment_value - control_value
            uplift_pct = (
                absolute_delta / control_value * 100
                if control_value != 0
                else np.nan
            )

            results.append({
                "metric": metric,
                "control": control_value,
                "treatment": treatment_value,
                "absolute_delta": absolute_delta,
                "uplift_pct": uplift_pct
            })

            logger.info(
                f"{metric}: Control={control_value}, "
                f"Treatment={treatment_value}, "
                f"Uplift={uplift_pct:.2f}%"
            )

        results_df = pd.DataFrame(results)

        return results_df

    def check_guardrail_metrics(
        self,
        guardrail_metrics: Dict[str, Dict[str, float]]
    ) -> pd.DataFrame:
        """
        Evaluate guardrail metrics such as refund rate or seller exposure diversity.

        Expected input format
        ---------------------
        {
            "refund_rate": {"control": 0.021, "treatment": 0.022},
            "smb_exposure_diversity": {"control": 0.12, "treatment": 0.18}
        }

        Returns
        -------
        pd.DataFrame
            Guardrail metric comparison table.
        """
        logger.info("Checking recommendation guardrail metrics...")

        rows = []

        for metric, values in guardrail_metrics.items():
            if "control" not in values or "treatment" not in values:
                raise ValueError(
                    f"Guardrail metric '{metric}' must contain control and treatment values."
                )

            control_value = values["control"]
            treatment_value = values["treatment"]
            delta = treatment_value - control_value

            rows.append({
                "metric": metric,
                "control": control_value,
                "treatment": treatment_value,
                "absolute_delta": delta
            })

        return pd.DataFrame(rows)


if __name__ == "__main__":
    # Example usage:
    # item_catalog_df = pd.DataFrame({
    #     "product_id": ["p1", "p2", "p3"],
    #     "seller_late_rate": [0.05, 0.20, 0.03],
    #     "historical_cvr": [0.12, 0.05, 0.10],
    #     "price_band": ["High", "Low", "Low"],
    #     "historical_sales": [120, 300, 180],
    #     "seller_sales_volume": [80, 500, 60],
    #     "seller_review_score": [4.6, 4.2, 4.8]
    # })
    #
    # interaction_history_df = pd.DataFrame({
    #     "user_id": ["u1", "u2", "u3"],
    #     "product_id": ["p1", "p2", "p2"],
    #     "event_type": ["purchase", "purchase", "view"]
    # })
    #
    # rec_sys = RecommendationSystem(
    #     item_catalog=item_catalog_df,
    #     interaction_history=interaction_history_df
    # )
    #
    # print(rec_sys.generate_intent_aware_recs("u1", 0.9))
    # print(rec_sys.evaluate_ab_test(
    #     control_metrics={"purchase_rate": 0.12, "revenue_per_user": 18.5},
    #     treatment_metrics={"purchase_rate": 0.15, "revenue_per_user": 24.0}
    # ))