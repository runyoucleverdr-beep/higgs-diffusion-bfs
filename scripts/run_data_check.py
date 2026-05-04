from src.config import load_config
from src.graph_builder import load_retweet_graph, summarize_graph
from src.activity_parser import load_activity_data


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