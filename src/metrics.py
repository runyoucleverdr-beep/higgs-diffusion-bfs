from __future__ import annotations
import pandas as pd


def results_to_dataframe(results: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(results)


def rank_sources_by_metric(df: pd.DataFrame, metric: str, ascending: bool = False) -> pd.DataFrame:
    if metric not in df.columns:
        raise KeyError(f"Metric '{metric}' not found in dataframe.")
    return df.sort_values(metric, ascending=ascending).reset_index(drop=True)

def summarize_by_source_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate BFS metrics by source type.
    """
    if df.empty:
        return pd.DataFrame()

    metric_cols = [
        "out_degree",
        "reachable_nodes",
        "reachable_ratio",
        "max_depth",
        "avg_distance",
        "median_distance",
        "in_largest_wcc",
    ]
    summary = (
        df.groupby("source_type")[metric_cols]
        .agg(["count", "mean", "median", "min", "max"])
        .round(4)
    )

    summary.columns = [
        "{0}_{1}".format(col, stat) for col, stat in summary.columns.to_flat_index()
    ]
    summary = summary.reset_index()

    return summary