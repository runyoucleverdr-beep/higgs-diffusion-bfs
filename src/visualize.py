from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd



def plot_top_sources_bar(
    df: pd.DataFrame,
    metric: str,
    output_path: str,
    top_k: int = 10
) -> None:
    top_df = df.sort_values(metric, ascending=False).head(top_k)

    plt.figure(figsize=(10, 6))
    plt.bar(top_df["source"], top_df[metric])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_k} Sources by {metric}")
    plt.xlabel("Source User")
    plt.ylabel(metric)
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_bfs_levels(level_count_dict: dict[int, int], output_path: str, source: str) -> None:
    levels = list(level_count_dict.keys())
    counts = list(level_count_dict.values())

    plt.figure(figsize=(8, 5))
    plt.plot(levels, counts, marker="o")
    plt.title(f"BFS Level Distribution for Source {source}")
    plt.xlabel("BFS Level")
    plt.ylabel("Number of Nodes")
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()