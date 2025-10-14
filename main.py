from src.data_gen import generate_decks
import src.scoring  # import the whole scoring module
from src.viz import generate_heatmaps 

# main script to augment data, score, and visualize
def augment_data():
    # get user input for number of new decks
    try:
        n = int(input("How many new decks would you like to generate? "))
        if n <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # generate decks
    generate_decks(n)
    print("Deck generation completed.")

    # run scoring
    src.scoring.main()
    print("Scoring completed.")

    # generate heatmaps
    generate_heatmaps()
    print("Heatmaps created.")


if __name__ == "__main__":
    augment_data()