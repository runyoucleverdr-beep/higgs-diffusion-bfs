# Higgs Diffusion BFS Project

This project analyzes information diffusion on Twitter using the SNAP Higgs Twitter Dataset and Breadth-First Search (BFS).

## Main Question
How far can information spread in the retweet network, and which early users are structurally positioned to trigger broader cascades?

## Dataset
- retweet_network.edgelist.gz
- higgs-activity_time.txt.gz

## Method
- Build a directed retweet graph
- Reverse edges to represent information flow
- Select source users from early retweet activity
- Run BFS from each source
- Measure reach, depth, and shortest-hop distance

## Run
```bash
python scripts/run_data_check.py
python scripts/run_bfs_experiment.py