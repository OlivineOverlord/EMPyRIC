import pandas as pd

def load_csv(filepath: str) -> pd.DataFrame:
    """Loads geochemical data from a CSV file."""
    return pd.read_csv(filepath)

def save_csv(df: pd.DataFrame, filepath: str):
    """Saves DataFrame to CSV."""
    df.to_csv(filepath, index=False)