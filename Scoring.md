Scoring_bit.md file:

Our scoring logic works by reading the decks that have been generated and stored in compressed bits in .bin files found in the decks_chunks folder. Player 1 and player 2 choices of sequences are chosen, and then a 3 bit window slides across the deck, checking for a sequence that matches either of those chosen by the players. If a match is found, this counts as a trick for this player and the scoring continues through the decks. At the end of this process, all the tricks for each combination of sequences for each player should have been found, and the cards for each combination are counted at the end of the game. Draws are also recorded and saved in the same .csv file.

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
