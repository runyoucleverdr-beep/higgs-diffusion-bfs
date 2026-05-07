from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config, ensure_dir
from src.pipeline import run_pipeline
from src.visualize import(
    plot_top_sources_bar, 
    plot_bfs_levels, 
    plot_metric_boxplot_by_source_type,
    plot_mean_metric_by_source_type,
)

def main():
    config = load_config()

    ensure_dir(config["paths"]["output_tables"])
    ensure_dir(config["paths"]["output_figures"])

    outputs = run_pipeline(config)
    results_df = outputs["results_df"]
    source_type_summary_df = outputs["source_type_summary_df"]
    level_details = outputs["level_details"]
    graph_summary = outputs["graph_summary"]

    tables_dir = Path(config["paths"]["output_tables"])
    figures_dir = Path(config["paths"]["output_figures"])

    results_df.to_csv(tables_dir / "bfs_source_summary.csv", index=False)
    source_type_summary_df.to_csv(tables_dir / "bfs_source_type_summary.csv", index=False)

    # Sorted result tables
    if not results_df.empty:
        results_df.sort_values(
            ["reachable_nodes", "max_depth", "out_degree"],
            ascending=[False, False, False]
        ).to_csv(
            tables_dir / "bfs_source_summary_sorted_by_reach.csv",
            index=False
        )

        results_df.sort_values(
            ["max_depth", "reachable_nodes", "out_degree"],
            ascending=[False, False, False]
        ).to_csv(
            tables_dir / "bfs_source_summary_sorted_by_depth.csv",
            index=False
        )

    # Save graph summary as a simple text file
    with open(tables_dir / "graph_summary.txt", "w", encoding="utf-8") as f:
        for key, value in graph_summary.items():
            f.write(f"{key}: {value}\n")

    # Overall top-source plots
    plot_top_sources_bar(
        results_df,
        metric="reachable_nodes",
        output_path=str(figures_dir / "top_sources_reach.png"),
        top_k=config["plot"]["top_k_sources"],
    )

    plot_top_sources_bar(
        results_df,
        metric="max_depth",
        output_path=str(figures_dir / "top_sources_depth.png"),
        top_k=config["plot"]["top_k_sources"],
    )

    # Group comparison plots
    plot_metric_boxplot_by_source_type(
        results_df,
        metric="reachable_nodes",
        output_path=str(figures_dir / "reachable_nodes_by_source_type_boxplot.png"),
    )

    plot_metric_boxplot_by_source_type(
        results_df,
        metric="max_depth",
        output_path=str(figures_dir / "max_depth_by_source_type_boxplot.png"),
    )

    plot_mean_metric_by_source_type(
        results_df,
        metric="reachable_nodes",
        output_path=str(figures_dir / "mean_reachable_nodes_by_source_type.png"),
    )

    plot_mean_metric_by_source_type(
        results_df,
        metric="max_depth",
        output_path=str(figures_dir / "mean_max_depth_by_source_type.png"),
    )

    # Representative BFS-level plot: source with largest reachable_nodes
    if not results_df.empty:
        representative_row = results_df.sort_values("reachable_nodes", ascending=False).iloc[0]
        source_key = "{0}::{1}".format(representative_row["source_type"], representative_row["source"])

        plot_bfs_levels(
            level_details[source_key],
            output_path=str(figures_dir / "representative_bfs_levels.png"),
            source=source_key,
        )

    print("\nExperiment completed.")

    print("\nGraph summary:")
    for key, value in graph_summary.items():
        print(f"  {key}: {value}")

    print("\nPer-source results:")
    print(results_df)

    print("\nPer-source-type summary:")
    print(source_type_summary_df)

    print("\nTop sources by reachable_nodes:")
    if not results_df.empty:
        print(
            results_df.sort_values("reachable_nodes", ascending=False)[
                [
                    "source",
                    "source_type",
                    "out_degree",
                    "in_largest_wcc",
                    "reachable_nodes",
                    "max_depth",
                    "avg_distance",
                ]
            ].head(10)
        )
        
    print("\nTop sources by max_depth:")
    if not results_df.empty:
        print(
            results_df.sort_values("max_depth", ascending=False)[
                [
                    "source",
                    "source_type",
                    "out_degree",
                    "in_largest_wcc",
                    "reachable_nodes",
                    "max_depth",
                    "avg_distance",
                ]
            ].head(10)
        )

    print(results_df.sort_values("reachable_nodes", ascending=False)[
    ["source", "source_type", "out_degree", "reachable_nodes", "max_depth"]].head(10))

if __name__ == "__main__":
    main()