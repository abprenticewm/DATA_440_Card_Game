# imports
import csv
import json
import os
from pathlib import Path

# save files in data folder
DECKS_DIR = os.path.join("data", "decks_chunks")
RESULTS_FILE = os.path.join("data", "results.csv")
PROGRESS_FILE = os.path.join("data", "progress.json")

# establish deck size and bytes per deck
DECK_SIZE_BITS = 52
BYTES_PER_DECK = (DECK_SIZE_BITS + 7) // 8

# hard code possible options for players
SEQUENCES = [
    "000", "001", "010", "011",
    "100", "101", "110", "111",
]

# all pairings without duplicates
MATCHUPS = [(p1, p2) for i, p1 in enumerate(SEQUENCES) for j, p2 in enumerate(SEQUENCES) if i != j]


def load_progress():
    # load progress from json file if it exists
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"matchup_index": 0, "file_index": 0}

# save progress to json file
def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def load_results():
    results = {}
    # load results from csv file if it exists
    if Path(RESULTS_FILE).exists():
        with open(RESULTS_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["p1_seq"], row["p2_seq"])
                # matchup results stored in dictionary
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

# save results to csv file
def save_results(results):
    # column names
    fieldnames = [
        "p1_seq", "p2_seq",
        "p1_tricks", "p2_tricks", "draws_tricks",
        "p1_cards", "p2_cards", "draws_cards",
        "runs",
    ]
    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # write each matchup result
        for (p1_seq, p2_seq), vals in results.items():
            writer.writerow({
                "p1_seq": p1_seq,
                "p2_seq": p2_seq,
                **vals
            })


# read one deck file and return list of strings
def read_decks_from_file(filename):
    decks = []
    with open(filename, "rb") as f:
        # read each deck an add to list
        while (chunk := f.read(BYTES_PER_DECK)):
            deck_int = int.from_bytes(chunk, "big")
            deck_bits = format(deck_int, f"0{DECK_SIZE_BITS}b")
            decks.append(deck_bits)
    return decks


# play through a single deck and return winner
def play_deck(deck_bits, p1_seq, p2_seq):
    i = 0
    n = len(deck_bits)
    # initialize scores
    p1_tricks = p2_tricks = 0
    p1_cards = p2_cards = 0
    # loop through deck
    while i <= n - 3:
        window = deck_bits[i:i+3]
        # if match, score and remove cards
        if window == p1_seq:
            p1_tricks += 1
            p1_cards += (i + 3)  # cards up to and including sequence
            deck_bits = deck_bits[i+3:]  # remove used cards
            n = len(deck_bits)
            i = 0
            continue
        # elif match for player 2
        elif window == p2_seq:
            p2_tricks += 1
            p2_cards += (i + 3)
            deck_bits = deck_bits[i+3:]
            n = len(deck_bits)
            i = 0
            continue
        # else move window forward
        i += 1

    # account for draws
    draws_tricks = 0
    draws_cards = 0
    if p1_tricks == p2_tricks:
        draws_tricks = 1
    if p1_cards == p2_cards:
        draws_cards = 1

    return p1_tricks, p2_tricks, draws_tricks, p1_cards, p2_cards, draws_cards


def main():
    # Load progress
    progress = load_progress()
    matchup_index = progress["matchup_index"]
    file_index = progress["file_index"]

    # get deck file
    deck_file = os.path.join(DECKS_DIR, f"decks_seed{file_index+1:03d}.bin")
    if not Path(deck_file).exists():
        print(f"No more deck files to process at index {file_index}. Done!")
        return

    decks = read_decks_from_file(deck_file)
    print(f"Processing file: {deck_file} with {len(decks)} decks...")

    # load results
    results = load_results()

    # run scoring
    for deck_bits in decks:
        p1_seq, p2_seq = MATCHUPS[matchup_index]
        # play deck and get results
        p1_tricks, p2_tricks, draws_tricks, p1_cards, p2_cards, draws_cards = play_deck(deck_bits, p1_seq, p2_seq)
        # update results dictionary
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
        # update cumulative results
        results[key]["p1_tricks"] += p1_tricks
        results[key]["p2_tricks"] += p2_tricks
        results[key]["draws_tricks"] += draws_tricks
        results[key]["p1_cards"] += p1_cards
        results[key]["p2_cards"] += p2_cards
        results[key]["draws_cards"] += draws_cards
        results[key]["runs"] += 1

        # advance matchup
        matchup_index = (matchup_index + 1) % len(MATCHUPS)

    # save updated results
    save_results(results)

    # update progress
    progress["matchup_index"] = matchup_index
    progress["file_index"] = file_index + 1
    save_progress(progress)

    # print status to keep track
    print(f"Finished file {file_index+1}. Next run will use file index {file_index+1}.")


if __name__ == "__main__":
    main()