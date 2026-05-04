from src.config import load_config
from src.graph_builder import load_retweet_graph, summarize_graph
from src.activity_parser import load_activity_data

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    config = load_config()

    graph = load_retweet_graph(config["paths"]["retweet_network"])
    summary = summarize_graph(graph)
    print("Graph summary:", summary)

    activity_df = load_activity_data(config["paths"]["activity_file"])
    print("Activity shape:", activity_df.shape)
    print(activity_df.head())


if __name__ == "__main__":
    main()