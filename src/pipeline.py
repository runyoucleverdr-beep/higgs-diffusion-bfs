from __future__ import annotations
from src.graph_builder import(
    load_retweet_graph, 
    reverse_graph_for_information_flow, 
    summarize_graph,
    summarize_weakly_connected_components,
    get_largest_weakly_connected_component_nodes,
    summarize_strongly_connected_components,
    get_largest_strongly_connected_component_nodes,
    )
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
    scc_summary = summarize_strongly_connected_components(graph)

    graph_summary.update(wcc_summary)
    graph_summary.update(scc_summary)

    largest_wcc_nodes = get_largest_weakly_connected_component_nodes(graph)
    largest_scc_nodes = get_largest_strongly_connected_component_nodes(graph)

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
            out_degree = graph.out_degree(source_str) if source_str in graph else 0
            in_largest_wcc = source_str in largest_wcc_nodes
            in_largest_scc = source_str in largest_scc_nodes

            print(
                "Source {0}: source_type={1}, out_degree={2}, in_largest_wcc={3}".format(
                    source_str, source_type, out_degree, in_largest_wcc, in_largest_scc
                )
            )

            distances = bfs_distances(graph, source_str)
            
            summary = summarize_bfs(distances, graph.number_of_nodes())
            
            row = {
                "source": source_str,
                "source_type": source_type,
                "out_degree": out_degree,
                "in_largest_wcc": in_largest_wcc,
                "in_largest_scc": in_largest_scc,
                "reachable_nodes": summary.get("reachable_nodes", 0),
                "reachable_excluding_self": max(summary.get("reachable_nodes", 0) - 1, 0),
                "reachable_ratio": summary.get("reachable_ratio", 0.0),
                "max_depth": summary.get("max_depth", 0),
                "avg_distance": summary.get("avg_distance", 0.0),
                "median_distance": summary.get("median_distance", 0.0),
            }


            results.append(row)
            level_details["{0}::{1}".format(source_type, source_str)] = level_counts(distances)

    results_df = results_to_dataframe(results)

    if not results_df.empty:
        ordered_cols = [
            "source",
            "source_type",
            "out_degree",
            "in_largest_wcc",
            "in_largest_scc",
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
        "largest_wcc_nodes": largest_wcc_nodes,
        "largest_scc_nodes": largest_scc_nodes,
    }
