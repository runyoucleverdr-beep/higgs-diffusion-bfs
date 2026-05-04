from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config, ensure_dir
from src.pipeline import run_pipeline
from src.visualize import plot_top_sources_bar, plot_bfs_levels


def main():
    config = load_config()

    ensure_dir(config["paths"]["output_tables"])
    ensure_dir(config["paths"]["output_figures"])

    outputs = run_pipeline(config)
    results_df = outputs["results_df"]
    level_details = outputs["level_details"]

    table_path = Path(config["paths"]["output_tables"]) / "bfs_source_summary.csv"
    results_df.to_csv(table_path, index=False)

    plot_top_sources_bar(
        results_df,
        metric="reachable_nodes",
        output_path=str(Path(config["paths"]["output_figures"]) / "top_sources_reach.png"),
        top_k=config["plot"]["top_k_sources"],
    )

    plot_top_sources_bar(
        results_df,
        metric="max_depth",
        output_path=str(Path(config["paths"]["output_figures"]) / "top_sources_depth.png"),
        top_k=config["plot"]["top_k_sources"],
    )

    if not results_df.empty:
        representative_source = results_df.sort_values(
            "reachable_nodes", ascending=False
        ).iloc[0]["source"]

        plot_bfs_levels(
            level_details[representative_source],
            output_path=str(Path(config["paths"]["output_figures"]) / "representative_bfs_levels.png"),
            source=representative_source,
        )

    print("Experiment completed.")
    print(results_df)


if __name__ == "__main__":
    main()