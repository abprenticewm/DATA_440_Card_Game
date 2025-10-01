from src.data_generation import run_generation
import src.scoring
import os

N_RUNS = 3  # number of times to run scoring

def main():
    # generate decks once
    stats = run_generation()
    print(f"Generated {len(stats['files'])} deck files into data/decks_chunks.")

    # run scoring multiple times
    for i in range(N_RUNS):
        print(f"\n=== Scoring run {i+1}/{N_RUNS} ===")
        src.scoring.main()

if __name__ == "__main__":
    main()
