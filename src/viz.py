# imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# paths - base project directory - was having directory issues
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_FILE = os.path.join(BASE_DIR, "data", "results.csv")
OUT_DIR = os.path.join(BASE_DIR, "data")

# sequences order
SEQUENCES = ["000", "001", "010", "011", "100", "101", "110", "111"]

# map 0 -> B and 1 -> R
SEQ_TO_BR = {"0": "B", "1": "R"}
# convert sequence string to B/R
def seq_to_br(seq):
    return "".join(SEQ_TO_BR[c] for c in seq)

# generate heatmaps from results.csv
def generate_heatmaps():
    if not os.path.exists(RESULTS_FILE):
        print("No results.csv found. Run scoring first.")
        return

    # read CSV
    df = pd.read_csv(RESULTS_FILE, dtype={"p1_seq": str, "p2_seq": str})
    # ensure 3-char strings - was not computing values with leading zeros
    df["p1_seq"] = df["p1_seq"].str.zfill(3)
    df["p2_seq"] = df["p2_seq"].str.zfill(3)

    # compute probabilities
    df["p1_win_tricks"] = df["p1_tricks"] / (df["p1_tricks"] + df["p2_tricks"] + df["draws_tricks"])
    df["draw_tricks_prob"] = df["draws_tricks"] / (df["p1_tricks"] + df["p2_tricks"] + df["draws_tricks"])
    df["p1_win_cards"] = df["p1_cards"] / (df["p1_cards"] + df["p2_cards"] + df["draws_cards"])
    df["draw_cards_prob"] = df["draws_cards"] / (df["p1_cards"] + df["p2_cards"] + df["draws_cards"])

    # total decks simulated, print updates
    n_decks = int(df["runs"].sum())
    print(f"Generating heatmaps from {n_decks:,} simulated decks...")

    # pivot data for heatmaps
    win_tricks = df.pivot_table(index="p2_seq", columns="p1_seq", values="p1_win_tricks", aggfunc="mean")
    draw_tricks = df.pivot_table(index="p2_seq", columns="p1_seq", values="draw_tricks_prob", aggfunc="mean")
    win_cards = df.pivot_table(index="p2_seq", columns="p1_seq", values="p1_win_cards", aggfunc="mean")
    draw_cards = df.pivot_table(index="p2_seq", columns="p1_seq", values="draw_cards_prob", aggfunc="mean")

    # reindex all sequences
    win_tricks = win_tricks.reindex(index=SEQUENCES, columns=SEQUENCES)
    draw_tricks = draw_tricks.reindex(index=SEQUENCES, columns=SEQUENCES)
    win_cards = win_cards.reindex(index=SEQUENCES, columns=SEQUENCES)
    draw_cards = draw_cards.reindex(index=SEQUENCES, columns=SEQUENCES)

    # make labels and ensure blank diagonal
    def make_labels(win_df, draw_df):
        labels = pd.DataFrame("", index=win_df.index, columns=win_df.columns, dtype=str)
        for r in win_df.index:
            for c in win_df.columns:
                w = win_df.loc[r, c]
                d = draw_df.loc[r, c]
                if pd.isna(w) or pd.isna(d) or r == c:
                    labels.loc[r, c] = ""
                else:
                    labels.loc[r, c] = f"{int(round(w*100))} ({int(round(d*100))})"
        return labels

    # create labels
    labels_tricks = make_labels(win_tricks, draw_tricks)
    labels_cards = make_labels(win_cards, draw_cards)

    def plot_heatmap(data, labels, title, filename):
        # mask for diagonal blanks
        mask_diag = np.zeros_like(data, dtype=bool)
        for i, seq in enumerate(SEQUENCES):
            mask_diag[i, i] = True

        plt.figure(figsize=(8, 6))

        # use dynamic min/max for darker colors based on dataset
        vmax = np.nanmax(data.values)
        vmin = np.nanmin(data.values)

        # main heatmap without diagonal
        ax = sns.heatmap(
            data,
            annot=labels,
            fmt="",
            cmap="Blues",
            linewidths=0.5,
            linecolor="gray",
            vmin=vmin,
            vmax=vmax,
            mask=mask_diag,
            cbar=False
        )

        # gray diagonal
        sns.heatmap(
            data,
            mask=~mask_diag,
            cmap=sns.color_palette(["lightgray"]),
            linewidths=0.5,
            linecolor="gray",
            cbar=False,
            ax=ax
        )

        # flip both axes so top-right = BBB - was flipped before
        ax.invert_yaxis()
        ax.invert_xaxis()

        # axis labels B/R - was 0/1 before
        ax.set_xticklabels([seq_to_br(c) for c in data.columns])
        ax.set_yticklabels([seq_to_br(r) for r in data.index])

        # format heatmap
        ax.set_title(title, fontsize=14, pad=15)
        ax.set_xlabel("My Choice (P1)", fontsize=12)
        ax.set_ylabel("Opponent Choice (P2)", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', rotation=0)

        # highlight best per row (skip diagonal)
        for y, seq in enumerate(SEQUENCES):
            row_vals = data.loc[seq]
            if row_vals.isna().all():
                continue
            # find max value in row
            max_val = row_vals.max()
            # highlight all max probs
            for x_idx, x_seq in enumerate(SEQUENCES):
                if pd.notna(row_vals[x_seq]) and row_vals[x_seq] == max_val and seq != x_seq:
                    ax.add_patch(plt.Rectangle((x_idx, y), 1, 1, fill=False, edgecolor="black", lw=2))

        # plot and save
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, filename), format="svg")
        plt.close()
        print(f"Saved {filename}")

    # title and filename
    plot_heatmap(win_tricks, labels_tricks, f"My Chance of Win(Draw) by Tricks \n N= ({n_decks:,} decks)", "ByTricks.svg")
    plot_heatmap(win_cards, labels_cards, f"My Chance of Win(Draw) by Cards \n N= ({n_decks:,} decks)", "ByCards.svg")

if __name__ == "__main__":
    generate_heatmaps()