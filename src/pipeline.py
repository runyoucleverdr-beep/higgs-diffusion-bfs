from __future__ import annotations
from src.graph_builder import load_retweet_graph, reverse_graph_for_information_flow, summarize_graph,summarize_weakly_connected_components,
from src.activity_parser import load_activity_data, get_retweet_activity
from src.source_selection import build_source_groups
from src.bfs_analysis import bfs_distances, summarize_bfs, level_counts
from src.metrics import results_to_dataframe, summarize_by_source_type


def run_pipeline(config: dict):
    graph = load_retweet_graph(config["paths"]["retweet_network"])

    if config["graph"]["reverse_for_information_flow"]:
        graph = reverse_graph_for_information_flow(graph)

    graph_summary = summarize_graph(graph)
    wcc_summary = summarize_weakly_connected_components(graph)
    graph_summary.update(wcc_summary)

    activity_df = load_activity_data(config["paths"]["activity_file"])
    retweet_df = get_retweet_activity(activity_df)

    source_groups = build_source_groups(retweet_df, graph, config)


    results = []
    level_details = {}

    for source_type, sources in source_groups.items():
        print("\n" + "=" * 70)
        print(f"Running BFS for source group: {source_type}")
        print("=" * 70)

        for source in sources:
            source_str = str(source)
            print(f"Source {source_str}: out_degree={graph.out_degree(source_str)}")

            distances = bfs_distances(graph, source_str)
            
            summary = summarize_bfs(distances, graph.number_of_nodes())
            summary["source"] = source_str
            results.append(summary)
            level_details["{0}::{1}".format(source_type, source_str)] = level_counts(distances)

    results_df = results_to_dataframe(results)

    if not results_df.empty:
        ordered_cols = [
            "source",
            "source_type",
            "out_degree",
            "reachable_nodes",
            "reachable_ratio",
            "max_depth",
            "avg_distance",
            "median_distance",
        ]
        results_df = results_df[ordered_cols]

    source_type_summary_df = summarize_by_source_type(results_df)

    return {
        "graph": graph,
        "graph_summary": graph_summary,
        "activity_df": activity_df,
        "retweet_df": retweet_df,
        "source_groups": source_groups,
        "results_df": results_df,
        "source_type_summary_df": source_type_summary_df,
        "level_details": level_details,
    }
