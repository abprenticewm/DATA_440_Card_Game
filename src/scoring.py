# imports
import random
import json
import os
import csv
import time
import tracemalloc
from pathlib import Path

# base project directory - was having directory issues
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# folder with deck files
DECKS_DIR = os.path.join(BASE_DIR, "data", "decks_chunks")
# where results are saved
RESULTS_FILE = os.path.join(BASE_DIR, "data", "results.csv")
# where progress is tracked
PROGRESS_FILE = os.path.join(BASE_DIR, "data", "progress.json")
DECK_SIZE_BITS = 52
BYTES_PER_DECK = (DECK_SIZE_BITS + 7) // 8

# sequences and matchups
SEQUENCES = ["000", "001", "010", "011", "100", "101", "110", "111"]
MATCHUPS = [(p1, p2) for p1 in SEQUENCES for p2 in SEQUENCES]  # include all combos

# progress tracking
def load_progress():
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"file_index": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

# results
def load_results():
    results = {}
    if Path(RESULTS_FILE).exists():
        with open(RESULTS_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["p1_seq"], row["p2_seq"])
                results[key] = {
                    "p1_tricks": int(row["p1_tricks"]),
                    "p2_tricks": int(row["p2_tricks"]),
                    "draws_tricks": int(row["draws_tricks"]),
                    "p1_cards": int(row["p1_cards"]),
                    "p2_cards": int(row["p2_cards"]),
                    "draws_cards": int(row["draws_cards"]),
                    "runs": int(row["runs"]),
                }
    return results

# save results to csv
def save_results(results):
    fieldnames = [
        "p1_seq", "p2_seq",
        "p1_tricks", "p2_tricks", "draws_tricks",
        "p1_cards", "p2_cards", "draws_cards",
        "runs",
    ]
    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for (p1_seq, p2_seq), vals in results.items():
            writer.writerow({"p1_seq": p1_seq, "p2_seq": p2_seq, **vals})

# read decks
def read_decks_from_file(filename):
    decks = []
    with open(filename, "rb") as f:
        while (chunk := f.read(BYTES_PER_DECK)):
            decks.append(int.from_bytes(chunk, "big"))
    return decks

# play one deck
def play_deck(deck_int, p1_seq, p2_seq):
    i = 0
    n = DECK_SIZE_BITS
    p1_tricks = p2_tricks = 0
    p1_cards = p2_cards = 0

    p1_bits = int(p1_seq, 2)
    p2_bits = int(p2_seq, 2)

    # play through the deck
    while i <= n - 3:
        window = (deck_int >> (n - 3 - i)) & 0b111

        if window == p1_bits:
            p1_tricks += 1
            p1_cards += (i + 3)
            n -= (i + 3)
            deck_int &= (1 << n) - 1
            i = 0
            continue
        elif window == p2_bits:
            p2_tricks += 1
            p2_cards += (i + 3)
            n -= (i + 3)
            deck_int &= (1 << n) - 1
            i = 0
            continue

        i += 1

    # determine deck winners (1 per deck)
    if p1_tricks > p2_tricks:
        tricks_winner = "p1"
    elif p2_tricks > p1_tricks:
        tricks_winner = "p2"
    else:
        tricks_winner = "draw"

    if p1_cards > p2_cards:
        cards_winner = "p1"
    elif p2_cards > p1_cards:
        cards_winner = "p2"
    else:
        cards_winner = "draw"

    return tricks_winner, cards_winner

# main loop
def main():
    progress = load_progress()
    file_index = progress.get("file_index", 0)
    results = load_results()

    deck_files = sorted([f for f in os.listdir(DECKS_DIR) if f.startswith("decks_seed") and f.endswith(".bin")])
    total_files = len(deck_files)

    if file_index >= total_files:
        print("All deck files have been processed. Done!")
        return

    start_time = time.perf_counter()
    tracemalloc.start()

    for fi in range(file_index, total_files):
        decks_file = os.path.join(DECKS_DIR, deck_files[fi])
        decks = read_decks_from_file(decks_file)
        print(f"Processing file {fi+1}/{total_files}: {decks_file} ({len(decks)} decks)")

        for deck_int in decks:
            p1_seq, p2_seq = random.choice(MATCHUPS)
            key = (p1_seq, p2_seq)

            if key not in results:
                results[key] = {
                    "p1_tricks": 0,
                    "p2_tricks": 0,
                    "draws_tricks": 0,
                    "p1_cards": 0,
                    "p2_cards": 0,
                    "draws_cards": 0,
                    "runs": 0,
                }

            tricks_winner, cards_winner = play_deck(deck_int, p1_seq, p2_seq)

            # increment win counts
            if tricks_winner == "p1":
                results[key]["p1_tricks"] += 1
            elif tricks_winner == "p2":
                results[key]["p2_tricks"] += 1
            else:
                results[key]["draws_tricks"] += 1

            if cards_winner == "p1":
                results[key]["p1_cards"] += 1
            elif cards_winner == "p2":
                results[key]["p2_cards"] += 1
            else:
                results[key]["draws_cards"] += 1

            results[key]["runs"] += 1

        progress["file_index"] = fi + 1
        save_progress(progress)
        save_results(results)
        print(f"Finished file {fi+1}/{total_files}")

    elapsed = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"All files processed. Runtime: {elapsed:.2f}s | Peak memory: {peak / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()