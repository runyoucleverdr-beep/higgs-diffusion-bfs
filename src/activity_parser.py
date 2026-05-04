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
    return df


def get_retweet_activity(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["interaction"].str.lower() == "rt"].copy()


def get_earliest_active_users(df: pd.DataFrame, top_k: int = 10) -> list[str]:
    first_seen = (
        df.groupby("user_a", as_index=False)["timestamp"]
        .min()
        .sort_values("timestamp", ascending=True)
    )
    return first_seen["user_a"].head(top_k).tolist()