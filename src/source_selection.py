from __future__ import annotations
import random
import networkx as nx
import pandas as pd


def select_earliest_users(activity_df: pd.DataFrame, top_k: int = 10) -> list[str]:
    first_seen = (
        activity_df.groupby("user_a", as_index=False)["timestamp"]
        .min()
        .sort_values("timestamp", ascending=True)
    )
    return first_seen["user_a"].head(top_k).tolist()


def select_top_out_degree_users(graph: nx.DiGraph, top_k: int = 10) -> list[str]:
    ranked = sorted(graph.out_degree(), key=lambda x: x[1], reverse=True)
    return [node for node, _ in ranked[:top_k]]


def select_random_users(graph: nx.DiGraph, k: int = 10, seed: int = 42) -> list[str]:
    random.seed(seed)
    nodes = list(graph.nodes())
    if k >= len(nodes):
        return nodes
    return random.sample(nodes, k)
