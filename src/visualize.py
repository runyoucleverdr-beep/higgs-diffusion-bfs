from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def _ensure_parent(output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def plot_top_sources_bar(
    df: pd.DataFrame,
    metric: str,
    output_path: str,
    top_k: int = 10
) -> None:
    if df.empty or metric not in df.columns:
        return
    
    top_df = df.sort_values(metric, ascending=False).head(top_k)
    top_df["label"] = top_df["source_type"] + ":" + top_df["source"].astype(str)

    plt.figure(figsize=(12, 6))
    plt.bar(top_df["label"], top_df[metric])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_k} Sources by {metric}")
    plt.xlabel("Source")
    plt.ylabel(metric)
    plt.tight_layout()

    _ensure_parent(output_path)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_bfs_levels(level_count_dict: dict[int, int], output_path: str, source: str) -> None:
    if not level_count_dict:
        return
    
    levels = list(level_count_dict.keys())
    counts = list(level_count_dict.values())

    plt.figure(figsize=(8, 5))
    plt.plot(levels, counts, marker="o")
    plt.title(f"BFS Level Distribution for Source {source}")
    plt.xlabel("BFS Level")
    plt.ylabel("Number of Nodes")
    plt.tight_layout()

    _ensure_parent(output_path)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

def plot_metric_boxplot_by_source_type(
    df: pd.DataFrame,
    metric: str,
    output_path: str
) -> None:
    if df.empty or metric not in df.columns:
        return

    grouped = []
    labels = []

    for source_type, group_df in df.groupby("source_type"):
        grouped.append(group_df[metric].tolist())
        labels.append(source_type)

    if not grouped:
        return

    plt.figure(figsize=(8, 5))
    plt.boxplot(grouped, labels=labels)
    plt.title(f"{metric} by Source Type")
    plt.xlabel("Source Type")
    plt.ylabel(metric)
    plt.tight_layout()

    _ensure_parent(output_path)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()  


def plot_mean_metric_by_source_type(
    df: pd.DataFrame,
    metric: str,
    output_path: str
) -> None:
    if df.empty or metric not in df.columns:
        return

    summary = (
        df.groupby("source_type", as_index=False)[metric]
        .mean()
        .sort_values(metric, ascending=False)
    )
    plt.figure(figsize=(8, 5))
    plt.bar(summary["source_type"], summary[metric])
    plt.title(f"Mean {metric} by Source Type")
    plt.xlabel("Source Type")
    plt.ylabel(f"Mean {metric}")
    plt.tight_layout()

    _ensure_parent(output_path)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()