from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config, ensure_dir
from src.pipeline import run_pipeline
from src.metrics import (
    concise_source_type_summary, 
    top_sources_compact,
    compute_degree_reach_correlations,
)

from src.visualize import(
    plot_top_sources_bar, 
    plot_bfs_levels, 
    plot_metric_boxplot_by_source_type,
    plot_mean_metric_by_source_type,
    plot_out_degree_vs_reach_scatter,
)

def format_df_for_console(df):
    if df.empty:
        return "[empty dataframe]"
    return df.to_string(index=False)

def write_analysis_notes(
    output_path: str,
    graph_summary: dict,
    concise_summary_df,
    correlation_df,
    top_reach_df,
    top_depth_df,
) -> None:
    lines = []

    lines.append("Higgs Diffusion BFS Project - Analysis Notes")
    lines.append("=" * 60)
    lines.append("")

    lines.append("1. Graph-level structure")
    lines.append("- num_nodes: {0}".format(graph_summary.get("num_nodes")))
    lines.append("- num_edges: {0}".format(graph_summary.get("num_edges")))
    lines.append("- avg_out_degree: {0}".format(graph_summary.get("avg_out_degree")))
    lines.append("- largest_wcc_ratio: {0}".format(graph_summary.get("largest_wcc_ratio")))
    lines.append("- largest_scc_ratio: {0}".format(graph_summary.get("largest_scc_ratio")))
    lines.append("")

    if (
        "largest_wcc_ratio" in graph_summary
        and "largest_scc_ratio" in graph_summary
    ):
        lines.append(
            "Interpretation: the reversed retweet graph is broadly connected in the weak sense "
            "but very sparse in the strong sense, suggesting a highly directional diffusion structure."
        )
        lines.append("")

    lines.append("2. Source-group comparison")
    if not concise_summary_df.empty:
        lines.append(concise_summary_df.to_string(index=False))
        lines.append("")

        try:
            strongest_group = concise_summary_df.sort_values(
                "mean_reachable_excluding_self", ascending=False
            ).iloc[0]["source_type"]
            lines.append(
                "The strongest source group by mean reachable_excluding_self is: {0}".format(
                    strongest_group
                )
            )
        except Exception:
            pass

        try:
            highest_scc_group = concise_summary_df.sort_values(
                "pct_in_largest_scc", ascending=False
            ).iloc[0]["source_type"]
            lines.append(
                "The source group with the highest presence in the largest SCC is: {0}".format(
                    highest_scc_group
                )
            )
        except Exception:
            pass

        lines.append("")

    lines.append("3. Degree vs reach correlation")
    if not correlation_df.empty:
        lines.append(correlation_df.to_string(index=False))
        lines.append("")

        try:
            overall_row = correlation_df[correlation_df["group"] == "overall"].iloc[0]
            lines.append(
                "Overall Spearman correlation between out_degree and reachable_nodes: {0}".format(
                    overall_row["spearman_out_degree_vs_reach"]
                )
            )
            lines.append(
                "Overall Pearson correlation between out_degree and reachable_nodes: {0}".format(
                    overall_row["pearson_out_degree_vs_reach"]
                )
            )
        except Exception:
            pass

        lines.append(
            "Interpretation: out-degree is a useful global signal of diffusion potential, "
            "but it does not fully determine reach within already strong source groups."
        )
        lines.append("")

    lines.append("4. Top sources by reachable_nodes")
    if not top_reach_df.empty:
        lines.append(top_reach_df.to_string(index=False))
        lines.append("")

    lines.append("5. Top sources by max_depth")
    if not top_depth_df.empty:
        lines.append(top_depth_df.to_string(index=False))
        lines.append("")

    lines.append("6. Short narrative summary")
    lines.append(
        "Random nodes generally have little or no diffusion ability. "
        "Earliest original sources are heterogeneous: some spread broadly, while others remain local. "
        "Top out-degree nodes are generally the strongest spreaders, but not every high-degree node has the same reach. "
        "This suggests that directed structural position matters more than simple early appearance."
    )
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    config = load_config()

    ensure_dir(config["paths"]["output_tables"])
    ensure_dir(config["paths"]["output_figures"])

    outputs = run_pipeline(config)
    results_df = outputs["results_df"]
    source_type_summary_df = outputs["source_type_summary_df"]
    level_details = outputs["level_details"]
    graph_summary = outputs["graph_summary"]

    concise_summary_df = concise_source_type_summary(results_df)
    top_reach_df = top_sources_compact(results_df, sort_by="reachable_nodes", top_k=10)
    top_depth_df = top_sources_compact(results_df, sort_by="max_depth", top_k=10)
    correlation_df = compute_degree_reach_correlations(results_df)

    tables_dir = Path(config["paths"]["output_tables"])
    figures_dir = Path(config["paths"]["output_figures"])

    results_df.to_csv(tables_dir / "bfs_source_summary.csv", index=False)
    source_type_summary_df.to_csv(tables_dir / "bfs_source_type_summary.csv", index=False)
    concise_summary_df.to_csv(tables_dir / "bfs_source_type_concise_summary.csv", index=False)
    top_reach_df.to_csv(tables_dir / "top_10_sources_by_reach.csv", index=False)
    top_depth_df.to_csv(tables_dir / "top_10_sources_by_depth.csv", index=False)
    correlation_df.to_csv(tables_dir / "degree_reach_correlations.csv", index=False)


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

    write_analysis_notes(
        output_path=str(tables_dir / "analysis_notes.txt"),
        graph_summary=graph_summary,
        concise_summary_df=concise_summary_df,
        correlation_df=correlation_df,
        top_reach_df=top_reach_df,
        top_depth_df=top_depth_df,
    )

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

    plot_out_degree_vs_reach_scatter(
        results_df,
        output_path=str(figures_dir / "out_degree_vs_reachable_nodes.png"),
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

    print("\nConcise source-type summary:")
    print(concise_summary_df)

    print("\nPer-source results:")
    print(results_df)

    print("\nDegree vs reach correlations:")
    print(correlation_df)

    print("\nPer-source-type summary:")
    print(source_type_summary_df)

    print("\nTop 10 sources by reachable_nodes:")
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

    print("\nTop 10 sources by max_depth:")
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

    
if __name__ == "__main__":
    main()