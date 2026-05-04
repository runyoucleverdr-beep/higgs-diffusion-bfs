from __future__ import annotations
from collections import deque, defaultdict
import networkx as nx


def bfs_distances(graph: nx.DiGraph, source: str) -> dict[str, int]:
    if source not in graph:
        return {}

    distances = {source: 0}
    queue = deque([source])

    while queue:
        current = queue.popleft()
        current_dist = distances[current]

        for neighbor in graph.neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)

    return distances


def summarize_bfs(distances: dict[str, int], total_nodes: int) -> dict:
    if not distances:
        return {
            "reachable_nodes": 0,
            "reachable_ratio": 0.0,
            "max_depth": 0,
            "avg_distance": 0.0,
        }

    dist_values = sorted(distances.values())
    reachable_nodes = len(distances)

    if len(dist_values) % 2 == 1:
        median_distance = float(dist_values[len(dist_values) // 2])
    else:
        mid = len(dist_values) // 2
        median_distance = (dist_values[mid - 1] + dist_values[mid]) / 2.0

    return {
        "reachable_nodes": reachable_nodes,
        "reachable_ratio": reachable_nodes / total_nodes if total_nodes > 0 else 0.0,
        "max_depth": max(dist_values),
        "avg_distance": sum(dist_values) / len(dist_values),
        "median_distance": median_distance,
    }


def level_counts(distances: dict[str, int]) -> dict[int, int]:
    counts = defaultdict(int)
    for d in distances.values():
        counts[d] += 1
    return dict(sorted(counts.items()))