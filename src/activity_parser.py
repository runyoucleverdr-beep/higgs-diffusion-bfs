from __future__ import annotations
import pandas as pd
from src.io_utils import iter_lines

def load_activity_data(path: str) -> pd.DataFrame:
    rows = []

    for line in iter_lines(path):
        if not line:
            continue
        parts = line.split()
        if len(parts) < 4:
            continue

        user_a, user_b, timestamp, interaction = parts[0], parts[1], parts[2], parts[3]
        rows.append(
            {
                "user_a": user_a,
                "user_b": user_b,
                "timestamp": int(timestamp),
                "interaction": interaction,
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        raise ValueError("Activity file was loaded, but no valid rows were parsed.")
    return df


def get_retweet_activity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only retweet rows.
    """
    if "interaction" not in df.columns:
        raise KeyError("Expected column 'interaction' not found in activity dataframe.")

    
    return df[df["interaction"].str.lower() == "rt"].copy()


def get_earliest_users_by_column(df: pd.DataFrame, user_col: str, top_k: int = 10) -> list:
    if df.empty:
        return []

    if user_col not in df.columns:
        raise KeyError(f"Expected column '{user_col}' not found.")

    
    
    first_seen = (
        df.groupby(user_col, as_index=False)["timestamp"]
        .min()
        .sort_values("timestamp", ascending=True)
    )
    return first_seen[user_col].head(top_k).tolist()