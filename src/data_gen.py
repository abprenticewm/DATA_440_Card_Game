# imports
import os
import random
from pathlib import Path

# params
OUT_DIR = "data/decks_chunks"       # directory where generated binary deck files are stored
CHUNK_SIZE = 10_000                 # number of decks per full chunk file
DECK_SIZE_BITS = 52                 # number of bits per deck
BYTES_PER_DECK = (DECK_SIZE_BITS + 7) // 8  # convert bits to required bytes per deck

# create one balanced deck and return as bytes
def generate_balanced_deck(rng: random.Random) -> bytes:
    bits = [0] * 26 + [1] * 26
    rng.shuffle(bits)
    # convert bits to bytes
    deck_int = 0
    for bit in bits:
        deck_int = (deck_int << 1) | bit
    # return as bytes
    return deck_int.to_bytes(BYTES_PER_DECK, byteorder="big")

# create one chunk file with num_decks decks
def generate_chunk(chunk_index: int, num_decks: int = CHUNK_SIZE, out_dir: str = OUT_DIR):
    # use chunk index as seed for reproducibility
    seed = chunk_index + 1
    rng = random.Random(seed)
    os.makedirs(out_dir, exist_ok=True)
    # read files
    filename = f"decks_seed{seed:03d}.bin"
    path = os.path.join(out_dir, filename)
    # skip if file already exists
    if os.path.exists(path):
        print(f"Skipping existing file: {filename}")
        return None
    # write decks to binary file
    with open(path, "wb") as f:
        for _ in range(num_decks):
            f.write(generate_balanced_deck(rng))

    print(f"Created file ({num_decks} decks): {filename}")
    return path


# count existing chunk files
def get_existing_chunks(out_dir: str = OUT_DIR) -> int:
    if not os.path.exists(out_dir):
        return 0
    return len([f for f in os.listdir(out_dir) if f.startswith("decks_seed") and f.endswith(".bin")])

# main function to generate requested number of decks
# creates full 10k chunks and a final smaller chunk if needed
def generate_decks(n_new: int, out_dir: str = OUT_DIR):
    os.makedirs(out_dir, exist_ok=True)
    existing = get_existing_chunks(out_dir)
    # find number of full chunks and remainder
    num_full_chunks = n_new // CHUNK_SIZE
    remainder = n_new % CHUNK_SIZE
    generated_files = []
    # create full chunks
    for i in range(num_full_chunks):
        path = generate_chunk(existing + i, CHUNK_SIZE, out_dir)
        if path:
            generated_files.append(path)
    # create final chunk if needed
    if remainder > 0:
        path = generate_chunk(existing + num_full_chunks, remainder, out_dir)
        if path:
            generated_files.append(path)

    print(f"Generated {n_new} decks across {len(generated_files)} file(s).")
    return generated_files

if __name__ == "__main__":
    import argparse
    # command line questions for user
    parser = argparse.ArgumentParser(description="Generate binary deck chunk files.")
    parser.add_argument("num_decks", type=int, help="Number of decks to generate")
    args = parser.parse_args()

    generate_decks(args.num_decks)