from __future__ import annotations
import random
import networkx as nx
import pandas as pd
from src.activity_parser import get_earliest_users_by_column


def select_earliest_original_sources(activity_df: pd.DataFrame, top_k: int = 10) -> list:
    """
    Select earliest original-source candidates using user_b from RT activity.
    """
    return get_earliest_users_by_column(activity_df, user_col="user_b", top_k=top_k)


def select_top_out_degree_users(graph: nx.DiGraph, top_k: int = 10) -> list[str]:
    ranked = sorted(graph.out_degree(), key=lambda x: x[1], reverse=True)
    return [node for node, _ in ranked[:top_k]]


def select_random_users(graph: nx.DiGraph, k: int = 10, seed: int = 42) -> list:
    random.seed(seed)
    nodes = list(graph.nodes())

    if not nodes:
        return []
    
    if k >= len(nodes):
        return [str(node) for node in nodes]
    
    return [str(node) for node in random.sample(nodes, k)]

def build_source_groups(activity_df: pd.DataFrame, graph: nx.DiGraph, config: dict) -> dict:
    """
    Build all source groups for comparison experiments.
    """
    experiment_cfg = config["experiment"]

    return {
        "earliest_original": select_earliest_original_sources(
            activity_df,
            top_k=experiment_cfg["num_earliest_sources"],
        ),
        "top_out_degree": select_top_out_degree_users(
            graph,
            top_k=experiment_cfg["num_top_out_degree_users"],
        ),
        "random": select_random_users(
            graph,
            k=experiment_cfg["num_random_users"],
            seed=experiment_cfg["random_seed"],
        ),
    }