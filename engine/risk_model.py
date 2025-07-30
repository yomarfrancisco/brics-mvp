"""
risk_model.py
Stub for XGBoost-based credit risk scoring.
"""
import pandas as pd

def calculate_pd(transaction_df: pd.DataFrame) -> pd.Series:
    """
    Calculate probability of default (PD) for each transaction using XGBoost (mocked for MVP).
    Args:
        transaction_df (pd.DataFrame): DataFrame of transaction-level data.
    Returns:
        pd.Series: Series of PD values.
    """
    # TODO: Replace with real XGBoost model
    return pd.Series([0.07] * len(transaction_df), index=transaction_df.index) 