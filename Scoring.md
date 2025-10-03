Scoring_bit.md file:

This script processes pre-generated decks stored in .bin files in the decks_chunks folder. A 3-bit sliding window moves across each 52-bit deck, and whenever the window matches a player’s chosen sequence, that player earns a trick and collects cards prior to the sequence (but after the last found sequence). The process continues until the deck is exhausted (less than 3 bits left), and all tricks and cards are counted for both players. If the players finish with the same number of tricks or cards, a draw is recorded respectively. Results for every possible matchup between different 3-bit sequences are aggregated and saved to results_2.csv, while progress is tracked in progress_2.json so the script can resume where it left off. Along with saving player tricks, cards, and draws, the script also reports runtime and peak memory usage for each file processed. Running scoring_bit.py once process decks from 1 file (10,000 decks). 

We arrived at this method because it seemed to be the most effective in terms of balancing time and memory efficiency. Originally, we tried scoring by using strings rather than bits, but decided to try bits in case it proved to be better, which it was. We tested this by adding time and memory measurments to both of these codes and comparing the results for scoring one deck, and then for scoring 3 deck files of 10,000 decks. In the end, the difference was pretty minimal, with the string method winning slightly on runtime and the bits method winning more significantly on memory usage. Since we will be running this code on a large scale of 2 million decks eventually, we decided it would be better to go with the bits method for scoring since memory will be more important to prioritize on that scale. 

Here is the comparison between the methods:

Bits:
One deck: 
* Runtime: 0.43 seconds | Peak memory: 0.57 MB
  
Three deck files: 
* Runtime: 1.26 seconds | Peak memory: 0.57 MB
* Runtime: 1.26 seconds | Peak memory: 0.56 MB
* Runtime: 1.31 seconds | Peak memory: 0.56 MB

Strings:
One deck: 
* Runtime: 0.30 seconds | Peak memory: 1.23 MB
  
Three deck files: 
* Runtime: 0.95 seconds | Peak memory: 1.23 MB
* Runtime: 0.96 seconds | Peak memory: 1.22 MB
* Runtime: 1.07 seconds | Peak memory: 1.22 MB