"""
main.py

Entry point for the AI-Powered Lead Generation & Recommendation Analytics project.

This script provides a lightweight overview of how the modular Python components
under the src/ folder are organised.

The full end-to-end analytical workflow is documented in the notebook/ folder,
where raw data loading, data cleaning, SQL analysis, funnel construction,
lead scoring, recommendation evaluation, and Tableau-ready outputs are generated.

Modules:
- DataPipeline: transaction cleaning and synthetic behavioural funnel generation
- IntentEngine: intent feature extraction and lead scoring model
- RecommendationSystem: popularity-based and intent-aware recommendation strategies
"""

import logging

from src.data_pipeline import DataPipeline
from src.intent_engine import IntentEngine
from src.recommendation_strategy import RecommendationSystem


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline_overview() -> None:
    """
    Show how the core project modules are structured.

    This function intentionally does not reload all raw datasets because the
    complete reproducible workflow is maintained in the notebook/ folder.
    It acts as a clean entry point for understanding the project architecture.
    """

    logger.info("=== AI-Powered Lead Generation & Recommendation Analytics ===")

    logger.info("Initialising data pipeline module...")
    data_pipeline = DataPipeline(
        raw_data_path="data/raw/",
        random_state=42
    )

    logger.info("Initialising intent engine module...")
    intent_engine = IntentEngine(
        random_state=42
    )

    logger.info("RecommendationSystem requires item_catalog and interaction_history.")
    logger.info("These inputs are generated through the notebook workflow.")

    logger.info("Core modules loaded successfully:")
    logger.info(f"- DataPipeline: {data_pipeline.__class__.__name__}")
    logger.info(f"- IntentEngine: {intent_engine.__class__.__name__}")
    logger.info("- RecommendationSystem: available after loading item catalog and interaction history")

    logger.info("For the full workflow, run notebooks 01 to 07 in the notebook/ folder.")
    logger.info("=== Pipeline overview completed ===")


if __name__ == "__main__":
    run_pipeline_overview()