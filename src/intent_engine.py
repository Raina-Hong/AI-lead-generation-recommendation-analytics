# src/intent_engine.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from src.utils import logger

class IntentEngine:
    """Engine for extracting user intent and automating lead scoring."""
    
    def __init__(self, model_path: str = None):
        self.model = joblib.load(model_path) if model_path else RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = ['review_score', 'delivery_delay_days', 'view_count', 'click_count', 'cart_count'] # Example features

    def extract_intent_features(self, user_data: pd.DataFrame, behavior_logs: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features combining text sentiment (using review score as proxy here) 
        and behavioral depth.
        (Aligns with Notebook 04)
        
        # TODO (V2 Roadmap - TikTok LIVE Integration):
        # 1. Replace rule-based sentiment with real-time Embedding Vector Search (e.g., using Qwen/Llama-3).
        # 2. Integrate real-time chat velocity and live room watch duration from streaming pipelines.
        """
        logger.info("Extracting intent features from user behavior and reviews...")
        
        # Assuming we aggregate user behavior by user_id
        behavior_agg = behavior_logs.groupby('user_id')['event_type'].value_counts().unstack().fillna(0)
        behavior_agg.columns = [f"{col}_count" for col in behavior_agg.columns]
        
        # Merge with user historical data
        features_df = pd.merge(user_data, behavior_agg, on='user_id', how='left').fillna(0)
        
        # Assume LLM-parsed sentiment score or classification goes here
        # features_df['sentiment_score'] = ... 
        
        return features_df

    def train_lead_scoring_model(self, features_df: pd.DataFrame, target_col: str = 'is_high_intent'):
        """
        Train the proxy model for lead scoring automation.
        (Aligns with Notebook 05)
        """
        logger.info("Training proxy model for lead scoring...")
        
        # Ensure required features are present
        available_features = [f for f in self.features if f in features_df.columns]
        
        X = features_df[available_features]
        y = features_df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        # Output feature importance for business attribution
        importance = dict(zip(available_features, self.model.feature_importances_))
        logger.info(f"Feature importance: {importance}")
        
        return self.model

    def predict_lead_score(self, new_user_features: pd.DataFrame) -> pd.Series:
        """
        Output intent probability scores (0-1), which can be wrapped as a real-time API.
        """
        available_features = [f for f in self.features if f in new_user_features.columns]
        probabilities = self.model.predict_proba(new_user_features[available_features])[:, 1]
        return pd.Series(probabilities, index=new_user_features.index, name="lead_score")

if __name__ == "__main__":
    engine = IntentEngine()
    # Mock data flow
    # features = engine.extract_intent_features(user_df, log_df)
    # model = engine.train_lead_scoring_model(features)
    # scores = engine.predict_lead_score(new_users)