from __future__ import annotations
import random
import networkx as nx
import pandas as pd
from src.activity_parser import get_earliest_users_by_column


def select_earliest_users(activity_df: pd.DataFrame, top_k: int = 10) -> list:
    return get_earliest_active_users_by_column(activity_df, user_col="user_a", top_k=top_k)


def select_top_out_degree_users(graph: nx.DiGraph, top_k: int = 10) -> list[str]:
    ranked = sorted(graph.out_degree(), key=lambda x: x[1], reverse=True)
    return [node for node, _ in ranked[:top_k]]


def select_random_users(graph: nx.DiGraph, k: int = 10, seed: int = 42) -> list[str]:
    random.seed(seed)
    nodes = list(graph.nodes())
    if not nodes:
        return []
    if k >= len(nodes):
        return nodes
    return random.sample(nodes, k)

def select_earliest_original_sources(activity_df: pd.DataFrame, top_k: int = 10) -> list:
    return get_earliest_users_by_column(activity_df, user_col="user_b", top_k=top_k)