# src/utils.py
import duckdb
import pandas as pd
import logging
from typing import Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Utility class for managing DuckDB database connections."""
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = duckdb.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

def execute_query(query: str, db_path: str = ":memory:") -> pd.DataFrame:
    """Execute an SQL query and return a pandas DataFrame."""
    try:
        with DatabaseConnection(db_path) as conn:
            return conn.execute(query).df()
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise

def load_data(file_path: str) -> pd.DataFrame:
    """Generic function to load CSV data."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded data from {file_path} with shape {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise