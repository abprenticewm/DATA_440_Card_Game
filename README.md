## Introduction

In this project, two players each choose a sequence of coin flips composed of **three outcomes** (`B` for "black" or tails, and `R` for "red" or heads). A simulated deck of coin flips is generated a number of times indicated by the user, and each game variant determines which player performs better according to different scoring rules.

---

## Game Variants

### 1. Penney’s Game
In the original **Penney’s Game**, a fair coin is flipped repeatedly until one player’s sequence appears. The first sequence to occur wins.  
Despite the apparent symmetry, some sequences have a **statistical advantage** depending on the opponent’s choice. This creates a fascinating nontransitive cycle of dominance among sequences.

---

### 2. The Humble–Nishiyama Variant
The **Humble–Nishiyama Game** changes the rules by flipping through a full deck of coin outcomes rather than stopping early.  
Each player earns one point (“**trick**”) every time their sequence appears in the deck. The player with more tricks at the end wins.  

While this variation still displays nontransitive behavior, the **probability distributions differ subtly** from the original Penney’s Game. Sequences that were strong in the first version may not be as dominant here.

---

### 3. The New Card-Scoring Variant
This project introduces a **third variant**, where the game is scored by **total cards won** rather than the number of tricks.  
Each time a sequence appears, the player claims **all cards** that form that sequence. The player who collects the most cards in total wins.

This small rule change produces a **significant strategic shift**. Simulations suggest that the optimal countersequence for Player 2 differs from the one predicted by Penney’s Game or the Humble–Nishiyama Game. The change in scoring subtly alters which patterns are most rewarding, illustrating how different evaluation metrics can transform the underlying strategy landscape.

---

## Project Structure

- `decks.py` — Generates and shuffles large numbers of simulated decks.
- `run_tests.py` — Runs all sequence matchups and records results.
- `data/results.csv` — Aggregated simulation output, including counts of wins, draws, tricks, and cards for each matchup.
- `viz.py` — Creates labeled **heatmap visualizations** showing Player 1’s probability of winning and the draw rate across all possible sequence pairings.
- `ByTricks.svg` / `ByCards.svg` — Final exported visualizations for each scoring method.

---

## Quick Start Guide

**Requirements:**
- Python 3.8+
- Libraries:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`

This project can be run on **Windows PowerShell**. This project is managed using **UV**. If you have not installed UV or are having issues related to UV, refer to their [documentation](https://docs.astral.sh/uv/guides/install-python/).  
Once UV is installed, download the repository and then follow the steps below.  

1. **Navigate to the directory:**  
   ```powershell
   cd "path of directory"
2. **Install UV dependencies**
  ```uv sync 
3. **You can then run the program**
  ```uv run main.py

The main program will prompt you to enter the amount of decks you would like to be generated, scored, and visualized. The results csv and the heatmaps will be automatically updated and can be found in the data folder in the repository. 