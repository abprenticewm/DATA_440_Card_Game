**README: File Descriptions:**

scoring.py: 
Looks at the deck chunks, saves progress to a .json file to keep track, and saves results to a csv file. Finds all possible combinations of player1 and player2 choices (without duplicates) and scores the combinations by looping through the deck(s), stopping when a "match" is found for a player and adding it to the "tricks" score, and counting the final number of cards for each player to add it to the "cards" score. Also accounts for draws and stores them in the csv.

data_generation.py : 
200 .bin files generated in decks_chunks with 10,000 random decks each. For each deck 52 bits (1 representing Red cards and 0 representing Black cards) are converted into 7 bytes.
Included in this script is code for generation and storage of decks and reading the files. (Note: files of 10,000 decks were used to break data into smaller replicable chunks and for consistency with method 2 which can fit fewer decks into one “github-supported” file.)

run_tests.py: 
Runs the card generation and read code 10 times to get metrics (memory, generation time, write time, read time).. Prints metrics out in a table including results from each run and the means and standard deviations. 

decks_chunks: 
stores decks 

main.py:
Generates decks and runs scoring 3 (or N) times.  