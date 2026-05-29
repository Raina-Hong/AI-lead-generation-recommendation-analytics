# src/intent_engine.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.exceptions import NotFittedError
from src.utils import logger


class IntentEngine:
    """
    Engine for extracting user intent features and training a lead scoring model.

    This module supports the lead generation part of the project:
    behavioural events + customer/order features -> lead score.
    """

    def __init__(self, model_path: str = None, random_state: int = 42):
        self.random_state = random_state

        if model_path:
            self.model = joblib.load(model_path)
            self.is_fitted = True
        else:
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=random_state,
                class_weight="balanced"
            )
            self.is_fitted = False

        # Keep feature names aligned with synthetic funnel event types.
        self.features = [
            "review_score",
            "delivery_delay_days",
            "view_count",
            "click_count",
            "add_to_cart_count",
            "inquiry_count"
        ]

        self.trained_features = None

    def extract_intent_features(
        self,
        user_data: pd.DataFrame,
        behavior_logs: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Extract intent features by combining user-level data and behavioural logs.

        Parameters
        ----------
        user_data : pd.DataFrame
            User-level feature table. Must contain user_id.
        behavior_logs : pd.DataFrame
            Synthetic or real behavioural event logs. Must contain user_id and event_type.

        Returns
        -------
        pd.DataFrame
            User-level intent feature table.

        Notes
        -----
        V2 Roadmap for TikTok LIVE / SMB use case:
        - Replace static review-score proxy with real-time comment sentiment or embedding signals.
        - Add live room watch duration, comment velocity, product click depth, and seller response speed.
        - Serve lead scores through an API for near real-time ranking.
        """

        logger.info("Extracting intent features from user behaviour and reviews...")

        if "user_id" not in user_data.columns:
            raise ValueError("user_data must contain a 'user_id' column.")

        required_log_cols = {"user_id", "event_type"}
        missing_log_cols = required_log_cols - set(behavior_logs.columns)

        if missing_log_cols:
            raise ValueError(
                f"behavior_logs is missing required columns: {missing_log_cols}"
            )

        behavior_agg = (
            behavior_logs
            .groupby("user_id")["event_type"]
            .value_counts()
            .unstack(fill_value=0)
        )

        behavior_agg.columns = [
            f"{event_type}_count" for event_type in behavior_agg.columns
        ]

        features_df = pd.merge(
            user_data,
            behavior_agg,
            on="user_id",
            how="left"
        )

        # Ensure all expected event-count columns exist even if some events are absent.
        expected_count_cols = [
            "view_count",
            "click_count",
            "add_to_cart_count",
            "inquiry_count",
            "purchase_count"
        ]

        for col in expected_count_cols:
            if col not in features_df.columns:
                features_df[col] = 0

        count_cols = [col for col in features_df.columns if col.endswith("_count")]
        features_df[count_cols] = features_df[count_cols].fillna(0)

        # Fill numeric columns only, avoiding accidental string replacement.
        numeric_cols = features_df.select_dtypes(include=["number"]).columns
        features_df[numeric_cols] = features_df[numeric_cols].fillna(0)

        return features_df

    def train_lead_scoring_model(
        self,
        features_df: pd.DataFrame,
        target_col: str = "is_high_intent"
    ) -> RandomForestClassifier:
        """
        Train a proxy model for lead scoring automation.

        Parameters
        ----------
        features_df : pd.DataFrame
            User-level feature table with target label.
        target_col : str
            Target column indicating whether the user is high-intent.

        Returns
        -------
        RandomForestClassifier
            Trained lead scoring model.
        """
        
        """
        Extract intent features by combining user-level data and behavioural logs.

        # TODO (V2 Roadmap - TikTok LIVE Integration):
        # 1. LLM Integration: Replace static 'review_score' with real-time text embeddings
        #    (e.g., using Qwen/Llama-3 APIs) generated from live chat/inquiries.
        # 2. Real-time Features: Integrate streaming metrics like 'chat_velocity' and
        #    'live_room_watch_duration' from Kafka/Flink pipelines.
        # 3. Multimodal Intent: Combine text sentiment with behavioral depth (e.g.,
        #    time spent hovering over the 'Cart' button).
        """
        logger.info("Training proxy model for lead scoring...")

        if target_col not in features_df.columns:
            raise ValueError(f"Target column '{target_col}' not found in features_df.")

        available_features = [
            feature for feature in self.features if feature in features_df.columns
        ]

        if not available_features:
            raise ValueError(
                "No required lead scoring features found in features_df. "
                f"Expected one or more of: {self.features}"
            )

        X = features_df[available_features].copy()
        y = features_df[target_col].copy()

        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        if y.nunique() < 2:
            raise ValueError(
                f"Target column '{target_col}' must contain at least two classes."
            )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=self.random_state,
            stratify=y
        )

        self.model.fit(X_train, y_train)
        self.is_fitted = True
        self.trained_features = available_features

        feature_importance = pd.DataFrame({
            "feature": available_features,
            "importance": self.model.feature_importances_
        }).sort_values("importance", ascending=False)

        logger.info(
            "Feature importance: "
            f"{feature_importance.to_dict(orient='records')}"
        )

        return self.model

    def predict_lead_score(self, new_user_features: pd.DataFrame) -> pd.Series:
        """
        Predict lead score as the probability of being high-intent.

        Parameters
        ----------
        new_user_features : pd.DataFrame
            New user feature table.

        Returns
        -------
        pd.Series
            Lead score between 0 and 1.
        """
        """
        Predict lead scores for new users based on extracted features.

        # Note for Production (TikTok LIVE):
        # This function is designed to be wrapped into a real-time Online Inference API.
        # It expects pre-calculated features (e.g., from a Redis Feature Store) to provide
        # millisecond-level latency for in-stream recommendation updates.
        """
        
        if not self.is_fitted:
            raise NotFittedError(
                "The lead scoring model has not been fitted yet. "
                "Call train_lead_scoring_model() first or load a fitted model."
            )

        if not self.trained_features:
            raise ValueError("No trained feature list found for prediction.")

        missing_features = [
            feature for feature in self.trained_features
            if feature not in new_user_features.columns
        ]

        if missing_features:
            raise ValueError(
                f"new_user_features is missing required columns: {missing_features}"
            )

        X_new = new_user_features[self.trained_features].copy()
        X_new = X_new.apply(pd.to_numeric, errors="coerce").fillna(0)

        probabilities = self.model.predict_proba(X_new)[:, 1]

        return pd.Series(
            probabilities,
            index=new_user_features.index,
            name="lead_score"
        )

    def save_model(self, model_path: str) -> None:
        """
        Save the trained lead scoring model.
        """
        if not self.is_fitted:
            raise NotFittedError("Cannot save an unfitted model.")

        joblib.dump(self.model, model_path)
        logger.info(f"Lead scoring model saved to {model_path}")


if __name__ == "__main__":
    engine = IntentEngine(random_state=42)

    # Example usage:
    # features_df = engine.extract_intent_features(user_df, behavior_logs_df)
    # model = engine.train_lead_scoring_model(features_df)
    # scores = engine.predict_lead_score(features_df)