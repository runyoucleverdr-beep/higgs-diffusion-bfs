# Modeling Information Diffusion on Twitter Using Breadth-First Search  
### A Case Study of the SNAP Higgs Twitter Dataset

**Author:** Yiwei Jin  
**Project Type:** Individual Project

---

## 1. Project Overview

This project looks at how scientific news spreads on Twitter, using public data collected around the Higgs boson discovery. In simple terms, it asks how a piece of information moves from one user to another through retweets.

To study this, the project turns Twitter retweet activity into a network map:
- each user is a point in the map
- each retweet creates a connection between users

The project then uses a step-by-step search method called Breadth-First Search (BFS). In this project, BFS is used to trace how information could spread outward from a starting user, one layer at a time.

The project focuses on three main questions:

1. **How far** can information spread in the retweet network?
2. **How deep** can a diffusion cascade extend in terms of hop count?
3. **Which early users** are structurally positioned to trigger broader cascades?

To better reflect the direction in which information is likely to move, the project reverses the original retweet links before analysis. This makes the network better match the idea of information flowing from an earlier source to later retweeters.

---

## 2. Research Question

The main question of this project is:

What makes a user more likely to spread information widely in a Twitter retweet network?

More specifically, the project compares three possibilities:

- users who appear early in the discussion,
- users chosen at random,
- users who are already well connected in the retweet network.

To test this, the project compares three groups of starting users:

- **earliest_original**: users who appear early and are treated as likely early sources of information
- **top_out_degree**: users with many outward connections in the analyzed network
- **random**: randomly selected users used as a baseline for comparison

By comparing these three groups, the project asks whether broad diffusion is mainly related to timing, chance, or network position.

---

## 3. Dataset

This project uses the **SNAP Higgs Twitter Dataset**, which was built around Twitter activity related to the Higgs boson discovery.

### Main files used
- `higgs-retweet_network.edgelist.gz`
- `higgs-activity_time.txt.gz`

### Data description
- The retweet network is modeled as a **directed graph**
- Each node represents a Twitter user
- Each edge represents a retweet relation
- The activity file provides:
  - `user_a`
  - `user_b`
  - `timestamp`
  - `interaction`

The current project uses:

- the **retweet network** for BFS traversal
- the **activity file** to identify candidate source users

### Important note on edge direction
To analyze **information diffusion**, this project reverses the original retweet edge direction. This is because the observed retweet action and the direction of information flow are not the same.


---

## 4. Method

This project uses a network-based approach to study how information can spread through Twitter retweets.

### Step 1: Build an information-flow network

The retweet data is converted into a network:

* each user is treated as a node
* each retweet relation is treated as a connection between users

Because the goal is to study how information moves from earlier users to later retweeters, the direction of the original retweet links is reversed before analysis.

### Step 2: Choose starting users

The project compares three different kinds of starting users:

* **earliest_original**: users who appeared early and are treated as likely early sources of information
* **top_out_degree**: users with many outward connections in the analyzed network
* **random**: randomly selected users used as a baseline

This makes it possible to compare whether broad diffusion is more closely related to **timing**, **network position**, or **chance**.

### Step 3: Trace how information could spread

The main algorithm used is **Breadth-First Search (BFS)**.

In simple terms, BFS starts from one user and then moves outward step by step:

* first to directly connected users
* then to users one step further away
* then to the next layer, and so on

This makes BFS a natural way to study layered information diffusion.

### Step 4: Measure diffusion outcomes

For each starting user, the project measures:

* **reachable nodes**: how many users can be reached
* **reachable ratio**: what share of the whole network can be reached
* **maximum depth**: how many layers the diffusion can extend
* **average distance**: the average number of steps needed to reach other users
* **median distance**: the middle value of those step counts

These measures help describe both the **size** and the **depth** of diffusion.

### Step 5: Add structural diagnostics

To better understand why some users spread information much more effectively than others, the project also examines:

* whether a user is located inside the largest connected part of the network
* whether the network is broadly connected or only weakly connected
* how strongly a user’s number of outward connections is associated with diffusion reach

This helps explain not only **what** happens, but also **why** it happens.


---

## 5. Current Findings and Interpretation

The current results suggest several clear patterns.

First, users chosen at random usually have little or no ability to spread information widely. Most of them can reach only themselves or a very small number of other users.

Second, users who appeared early in the discussion do not all behave the same way. Some of them are able to spread information very broadly, while others remain limited to small local parts of the network. This means that **being early is not enough by itself**.

Third, users who are already strongly connected in the network tend to be the most powerful spreaders overall. As a group, they usually reach more users and produce deeper diffusion chains than the other two groups.

Finally, the network is broadly connected if direction is ignored, but much less connected when direction is taken seriously. This suggests that information does not move freely in all directions. Instead, it tends to follow more one-way diffusion paths.

Taken together, the current results suggest that information diffusion in this Twitter network is shaped mainly by **where a user sits in the overall flow of information**, not just by whether that user appeared early.

In other words:

* random users are usually not important spreaders,
* early users can be either strong or weak,
* and highly connected users are the strongest candidates overall.

The results also suggest that simply counting how many direct outward connections a user has is helpful, but not always enough. Some users with many outward links spread information very widely, but others with fewer direct links can still perform strongly if they occupy a favorable position in the broader network.

Overall, the project shows that **directed network position matters more than simple timing**, and that information diffusion is better understood as a structured, layered process rather than a random one.

---

## 6. Repository Structure

```text
higgs-diffusion-bfs/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ config/
│  └─ default.yaml
├─ data/
│  ├─ raw/
│  ├─ interim/
│  └─ processed/
├─ outputs/
│  ├─ figures/
│  ├─ tables/
│  └─ logs/
├─ notebooks/
│  ├─ 01_data_check.ipynb
│  ├─ 02_graph_eda.ipynb
│  └─ 03_bfs_results.ipynb
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ io_utils.py
│  ├─ graph_builder.py
│  ├─ activity_parser.py
│  ├─ source_selection.py
│  ├─ bfs_analysis.py
│  ├─ metrics.py
│  ├─ visualize.py
│  └─ pipeline.py
├─ scripts/
│  ├─ __init__.py
│  ├─ run_data_check.py
│  ├─ run_bfs_experiment.py
│  └─ run_full_pipeline.py
└─ tests/
   ├─ test_graph_builder.py
   ├─ test_bfs_analysis.py
   └─ test_source_selection.py
````

---

## 7. Environment Setup

### Recommended Python version

This project is best run with **Python 3.10**.

### Create environment with Conda

```bash
conda create -n higgs-bfs python=3.10 -y
conda activate higgs-bfs
pip install -r requirements.txt
```

---

## 8. Download the Dataset

The raw dataset files are **not included** in this repository.
Please download them manually and place them in:

```text
data/raw/
```

### Required files

```text
data/raw/higgs-retweet_network.edgelist.gz
data/raw/higgs-activity_time.txt.gz
```

### Example PowerShell download commands

```powershell
New-Item -ItemType Directory -Path .\data\raw -Force | Out-Null

Invoke-WebRequest `
  -Uri "https://snap.stanford.edu/data/higgs-retweet_network.edgelist.gz" `
  -OutFile ".\data\raw\higgs-retweet_network.edgelist.gz"

Invoke-WebRequest `
  -Uri "https://snap.stanford.edu/data/higgs-activity_time.txt.gz" `
  -OutFile ".\data\raw\higgs-activity_time.txt.gz"
```

---

## 9. Configuration

The main configuration file is:

```text
config/default.yaml
```

Example:

```yaml
paths:
  retweet_network: data/raw/higgs-retweet_network.edgelist.gz
  activity_file: data/raw/higgs-activity_time.txt.gz
  output_tables: outputs/tables
  output_figures: outputs/figures

experiment:
  num_earliest_sources: 10
  num_top_out_degree_users: 10
  num_random_users: 10
  random_seed: 42

graph:
  reverse_for_information_flow: true

plot:
  top_k_sources: 10
```

---

## 10. How to Run

### Step 1: Data check

This verifies that the retweet network and activity file can be loaded correctly.

```bash
python scripts/run_data_check.py
```

### Step 2: Run BFS experiment

This runs the current diffusion analysis pipeline.

```bash
python scripts/run_bfs_experiment.py
```

### Step 3: Full pipeline

Currently equivalent to the BFS experiment script.

```bash
python scripts/run_full_pipeline.py
```

---

## 11. Outputs

After running the BFS experiment, the following files are generated:

### Tables

* `outputs/tables/bfs_source_summary.csv`
* `outputs/tables/bfs_source_type_summary.csv`
* `outputs/tables/bfs_source_type_concise_summary.csv`
* `outputs/tables/top_10_sources_by_reach.csv`
* `outputs/tables/top_10_sources_by_depth.csv`
* `outputs/tables/degree_reach_correlations.csv`
* `outputs/tables/graph_summary.txt`
* `outputs/tables/analysis_notes.txt`

### Figures

* `outputs/figures/top_sources_reach.png`
* `outputs/figures/top_sources_depth.png`
* `outputs/figures/reachable_nodes_by_source_type_boxplot.png`
* `outputs/figures/max_depth_by_source_type_boxplot.png`
* `outputs/figures/mean_reachable_nodes_by_source_type.png`
* `outputs/figures/mean_max_depth_by_source_type.png`
* `outputs/figures/out_degree_vs_reachable_nodes.png`
* `outputs/figures/representative_bfs_levels.png`

---

## 12. Current Interpretation

The current results suggest that diffusion in the reversed retweet graph is not well explained by randomness or early timing alone.

* Random nodes are usually terminal.
* Early original sources can be either highly influential or structurally weak.
* Top out-degree nodes are the strongest candidates overall.
* Out-degree is useful globally, but it does not fully determine diffusion reach within already strong source groups.

This means that **global directed structural position** plays a central role in diffusion.

---


## 13. Project Status

### Completed

* dataset loading
* retweet graph construction
* reversed information-flow modeling
* BFS-based diffusion analysis
* three source-group comparison
* WCC / SCC diagnostics
* degree–reach correlation analysis
* automatic analysis notes export

### Next step

The next stage is to turn the current outputs into a formal written report and presentation.

---

## 14. Notes

* Raw data files are excluded from version control.
* Generated outputs are excluded from version control.
* The current BFS analysis is **unweighted**.
* The project currently prioritizes **interpretability and structural analysis** over model complexity.

---

## 15. Academic Use

This repository is intended for academic course-project use.
Please refer to the original SNAP dataset source for data usage conditions.

---

## 16. AI usage
I used AI to generate some high-tech style pictures to make it look nicer. 

---