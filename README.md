**README: File Descriptions:**

scoring_bit.py: 
Looks at the deck chunks, saves progress to a .json file to keep track, and saves results to a csv file. Finds all possible combinations of player1 and player2 choices (without duplicates) and scores the combinations by looping through the deck(s), stopping when a "match" is found for a player and adding it to the "tricks" score, and counting the final number of cards for each player to add it to the "cards" score. Also accounts for draws and stores them in the csv.

data_generation.py : 
200 .bin files generated in decks_chunks with 10,000 random decks each. For each deck 52 bits (1 representing Red cards and 0 representing Black cards) are converted into 7 bytes.
Included in this script is code for generation and storage of decks and reading the files. (Note: files of 10,000 decks were used to break data into smaller replicable chunks and for consistency with method 2 which can fit fewer decks into one “github-supported” file.)

run_tests.py: 
Runs the card generation and read code 10 times to get metrics (memory, generation time, write time, read time).. Prints metrics out in a table including results from each run and the means and standard deviations. 

decks_chunks: 
Stores decks in binary deck files where each .bin file holds decks encoded in bit sequences to take up less memory/space.

progress_bit.json:
Keeps track of the progress as the user continues loading decks for organization and recreatability.

results_bit.csv:
Stores the results in a table with the columns p1_seq, p2_seq, p1_tricks, p2_tricks, draws_tricks, p1_cards, p2_cards, draws_cards, runs.

main.py:
Generates decks and runs scoring 3 (or N) times.  

extra_code:
Folder for extra code that is not relevant to the current final product, including the files for scoring using strings instead of bits, etc.