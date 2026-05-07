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

def concise_source_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compact source-type summary for quick interpretation.
    """
    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("source_type", as_index=False)
        .agg(
            num_sources=("source", "count"),
            mean_out_degree=("out_degree", "mean"),
            median_out_degree=("out_degree", "median"),
            mean_reachable_nodes=("reachable_nodes", "mean"),
            median_reachable_nodes=("reachable_nodes", "median"),
            mean_max_depth=("max_depth", "mean"),
            median_max_depth=("max_depth", "median"),
            pct_in_largest_wcc=("in_largest_wcc", "mean"),
            pct_in_largest_scc=("in_largest_scc", "mean"),
        )
        .round(4)
    )

    return summary


def top_sources_compact(
    df: pd.DataFrame,
    sort_by: str,
    top_k: int = 10
) -> pd.DataFrame:
    """
    Compact top-k source table for report use.
    """
    if df.empty:
        return pd.DataFrame()

    cols = [
        "source",
        "source_type",
        "out_degree",
        "in_largest_wcc",
        "in_largest_scc",
        "reachable_nodes",
        "max_depth",
        "avg_distance",
        "median_distance",
    ]

    return (
        df.sort_values(sort_by, ascending=False)[cols]
        .head(top_k)
        .reset_index(drop=True)
    )

def compute_degree_reach_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Pearson and Spearman correlations between out_degree and reachable_nodes,
    both overall and by source_type.
    """
    if df.empty:
        return pd.DataFrame()

    results = []

    def _safe_corr(sub_df: pd.DataFrame, method: str) -> float:
        if len(sub_df) < 2:
            return float("nan")
        if sub_df["out_degree"].nunique() <= 1 or sub_df["reachable_nodes"].nunique() <= 1:
            return float("nan")
        return sub_df["out_degree"].corr(sub_df["reachable_nodes"], method=method)

    overall = {
        "group": "overall",
        "n": len(df),
        "pearson_out_degree_vs_reach": _safe_corr(df, "pearson"),
        "spearman_out_degree_vs_reach": _safe_corr(df, "spearman"),
    }
    results.append(overall)

    for source_type, group_df in df.groupby("source_type"):
        results.append(
            {
                "group": source_type,
                "n": len(group_df),
                "pearson_out_degree_vs_reach": _safe_corr(group_df, "pearson"),
                "spearman_out_degree_vs_reach": _safe_corr(group_df, "spearman"),
            }
        )

    return pd.DataFrame(results).round(4)