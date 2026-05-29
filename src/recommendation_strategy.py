# src/recommendation_strategy.py
import pandas as pd
from typing import List, Dict
from src.utils import logger

class RecommendationSystem:
    """System providing multiple recommendation strategies."""
    
    def __init__(self, item_catalog: pd.DataFrame, interaction_history: pd.DataFrame):
        self.item_catalog = item_catalog
        self.interaction_history = interaction_history

    def generate_popularity_recs(self, user_id: str, top_k: int = 5) -> List[str]:
        """
        Baseline strategy: Popularity-based recommendations derived from historical sales.
        (Aligns with Control group)
        """
        # Calculate global best-selling items
        popular_items = self.interaction_history[
            self.interaction_history['event_type'] == 'purchase'
        ]['product_id'].value_counts().head(top_k).index.tolist()
        
        logger.debug(f"Generated popularity recs for user {user_id}")
        return popular_items

    def generate_intent_aware_recs(self, user_id: str, user_intent_score: float, top_k: int = 5) -> List[str]:
        """
        Treatment strategy: Intent-aware recommendations.
        Incorporates user lead scores, seller fulfillment quality, etc.
        """
        logger.debug(f"Generating intent-aware recs for user {user_id} with score {user_intent_score}")
        
        # 1. If user intent is high, recommend premium items with high CVR
        if user_intent_score > 0.8:
            # Filter out products from sellers with high late delivery rates
            candidates = self.item_catalog[self.item_catalog['seller_late_rate'] < 0.1]
            # Sort by product's historical conversion rate (CVR)
            recs = candidates.sort_values(by='historical_cvr', ascending=False).head(top_k)['product_id'].tolist()
        
        # 2. If user is price-sensitive (moderate intent)
        elif 0.5 <= user_intent_score <= 0.8:
            # Recommend cost-effective items or those with shipping subsidies
            candidates = self.item_catalog[self.item_catalog['price_band'] == 'Low']
            recs = candidates.sort_values(by='historical_sales', ascending=False).head(top_k)['product_id'].tolist()
            
        # 3. Fallback strategy
        else:
            recs = self.generate_popularity_recs(user_id, top_k)
            
        return recs

    def evaluate_ab_test(self, control_metrics: Dict, treatment_metrics: Dict):
        """
        Evaluate A/B test effects for different recommendation strategies.
        (Aligns with Notebook 07)
        """
        # This is a placeholder function; actual implementation should include 
        # statistical calculations (e.g., scipy.stats.ttest_ind).
        # Only printing here for demonstration, proving architectural thinking.
        logger.info("Evaluating A/B Test Results...")
        for metric in control_metrics.keys():
            c_val = control_metrics[metric]
            t_val = treatment_metrics[metric]
            uplift = (t_val - c_val) / c_val * 100 if c_val > 0 else 0
            logger.info(f"{metric}: Control={c_val}, Treatment={t_val}, Uplift={uplift:.2f}%")

if __name__ == "__main__":
    # Mock execution
    # cat_df = pd.DataFrame({'product_id': ['p1', 'p2'], 'seller_late_rate': [0.05, 0.2], 'historical_cvr': [0.1, 0.05]})
    # hist_df = pd.DataFrame({'user_id': ['u1'], 'product_id': ['p1'], 'event_type': ['purchase']})
    # rec_sys = RecommendationSystem(cat_df, hist_df)
    # print(rec_sys.generate_intent_aware_recs('u1', 0.9))