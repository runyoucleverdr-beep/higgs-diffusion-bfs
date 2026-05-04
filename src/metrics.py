from __future__ import annotations
import pandas as pd


def results_to_dataframe(results: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(results)


def rank_sources_by_metric(df: pd.DataFrame, metric: str, ascending: bool = False) -> pd.DataFrame:
    return df.sort_values(metric, ascending=ascending).reset_index(drop=True)