viz.py file:

The viz.py file reads the scoring results from results.csv and generates two heatmap visualizations that show the win and draw probabilities for every matchup of sequences (p1 and p2 choices) in Penney's game. It generates a heatmap for both scoring by tricks and by cards, and the visualization is created to look as similar to the example heatmap as possible. 

First, viz.py loads and cleans the data, making sure everything is in the correct format for a visualization. It then calculates the probabilites of each sequence from the results csv. Each heatmap uses B and R instead of 0 and 1, and has a diagonal of grey empty cells like the example heatmap. 

At the end, two SVG visualizations are saved to the data folder: ByTricks.svg and ByCards.svg.