from __future__ import annotations
from src.graph_builder import load_retweet_graph, reverse_graph_for_information_flow, summarize_graph
from src.activity_parser import load_activity_data, get_retweet_activity
from src.source_selection import select_earliest_users
from src.bfs_analysis import bfs_distances, summarize_bfs, level_counts
from src.metrics import results_to_dataframe
from src.source_selection import select_earliest_original_sources


def run_pipeline(config: dict):
    graph = load_retweet_graph(config["paths"]["retweet_network"])

    if config["graph"]["reverse_for_information_flow"]:
        graph = reverse_graph_for_information_flow(graph)

    graph_summary = summarize_graph(graph)

    activity_df = load_activity_data(config["paths"]["activity_file"])
    retweet_df = get_retweet_activity(activity_df)

    sources = select_earliest_original_sources(
        retweet_df,
        top_k=config["experiment"]["num_early_users"]
    )

    results = []
    level_details = {}

    for source in sources:
        source_str = str(source)
        print(f"Source {source_str}: out_degree={graph.out_degree(source_str)}")

        distances = bfs_distances(graph, source)
        summary = summarize_bfs(distances, graph.number_of_nodes())
        summary["source"] = source
        results.append(summary)
        level_details[source] = level_counts(distances)

    results_df = results_to_dataframe(results)

    return {
        "graph": graph,
        "graph_summary": graph_summary,
        "activity_df": activity_df,
        "retweet_df": retweet_df,
        "sources": sources,
        "results_df": results_df,
        "level_details": level_details,
    }
