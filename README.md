# Modeling Information Diffusion on Twitter Using Breadth-First Search  
### A Case Study of the SNAP Higgs Twitter Dataset

**Author:** Yiwei Jin  
**Project Type:** Individual Project

---

## 1. Project Overview

This project studies how scientific news spreads through a large social network using the **SNAP Higgs Twitter Dataset**. The main goal is to model the Twitter retweet network as a directed graph and apply **Breadth-First Search (BFS)** to analyze information diffusion.

The project focuses on three main questions:

1. **How far** can information spread in the retweet network?
2. **How deep** can a diffusion cascade extend in terms of hop count?
3. **Which early users** are structurally positioned to trigger broader cascades?

The current implementation uses the **retweet layer** of the Higgs dataset and reverses the edge direction to better represent **information flow** from source users to later retweeters.

---

## 2. Research Question

This project asks whether diffusion potential in a large Twitter retweet network is mainly determined by:

- simple early appearance,
- random structural location,
- or stronger directed structural position.

To test this, the project compares BFS diffusion outcomes across three different source-selection strategies:

- **earliest_original**
- **top_out_degree**
- **random**


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

### Core algorithm
The main algorithm used in this project is **Breadth-First Search (BFS)**.

### Why BFS
BFS is appropriate because it explores the graph level by level, which naturally matches the layered structure of information diffusion.

### Metrics currently computed
For each selected source user, the project computes:

- `reachable_nodes`
- `reachable_excluding_self`
- `reachable_ratio`
- `max_depth`
- `avg_distance`
- `median_distance`
- `out_degree`
- `in_largest_wcc`
- `in_largest_scc`

### Structural diagnostics
The project also measures global graph structure using:

- weakly connected components (WCC)
- strongly connected components (SCC)

This helps distinguish broad weak connectivity from true directed structural core membership.

---

## 5. Current Findings

The current experiment supports several conclusions:

1. **Random users usually have little or no diffusion ability.**
2. **Earliest original sources are heterogeneous**: some spread broadly, while others remain trapped in very small local structures.
3. **Top out-degree users are generally the strongest spreaders**, but not every high-degree node has the same reach.
4. The graph is **broadly connected in the weak sense but extremely sparse in the strong sense**, indicating a highly directional diffusion structure.

Overall, the project suggests that **directed structural position matters more than simple early appearance**.

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

````

## 16. AI usage
I took screenshots of the output to let AI help me write down and list all the output figures and tables in this markdown document. I also described the repo structure to let AI help me draw the tree structure in this markdown document.  
