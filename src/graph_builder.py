from __future__ import annotations

import networkx as nx
from src.io_utils import iter_lines


def load_retweet_graph(path: str) -> nx.DiGraph:
    """
    Load the Higgs retweet network as a directed graph.
    The current project uses an unweighted graph for BFS analysis.
    If a third column exists, it is ignored for now.
    """
    
    graph = nx.DiGraph()

    for line in iter_lines(path):
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        src, dst = parts[0], parts[1]
        graph.add_edge(src, dst)

    return graph


def reverse_graph_for_information_flow(graph: nx.DiGraph) -> nx.DiGraph:
    """
    Reverse edge direction so that edges better represent information flow.
    """
    return graph.reverse(copy=True)


def summarize_graph(graph: nx.DiGraph) -> dict:
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    
    return {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "avg_out_degree": (
            graph.number_of_edges() / graph.number_of_nodes()
            if graph.number_of_nodes() > 0 else 0
        ),
    }

def summarize_weakly_connected_components(graph: nx.DiGraph) -> dict:
    """
    Summarize weakly connected components in the directed graph.
    """
    if graph.number_of_nodes() == 0:
        return {
            "num_weakly_connected_components": 0,
            "largest_wcc_size": 0,
            "largest_wcc_ratio": 0.0,
        }
    component_sizes = sorted(
        [len(component) for component in nx.weakly_connected_components(graph)],
        reverse=True,
    )

    largest_wcc_size = component_sizes[0] if component_sizes else 0

    return {
        "num_weakly_connected_components": len(component_sizes),
        "largest_wcc_size": largest_wcc_size,
        "largest_wcc_ratio": largest_wcc_size / graph.number_of_nodes(),
    }
