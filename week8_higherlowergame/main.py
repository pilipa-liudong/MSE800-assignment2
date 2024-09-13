import random

# Simulated keywords and their monthly search volumes (based on fictional data)
search_data = {
    "Facebook": 2500000000,
    "Instagram": 1400000000,
    "Python programming": 12000000,
    "JavaScript": 8000000,
    "Climate change": 1000000,
    "Artificial Intelligence": 2000000,
    "The Beatles": 5000000,
    "World Cup": 7000000,
    "Donald Trump": 9000000,
    "New Zealand": 1200000
}

def play_higher_lower():
    print("Welcome to the Higher or Lower: Search Volume Edition!")
    print("Rules: Guess whether the second keyword has a higher or lower search volume than the first one.")

    # Shuffle the search terms
    terms = list(search_data.keys())
    random.shuffle(terms)

    score = 0
    index = 0

    # Main game loop
    while index < len(terms) - 1:
        term1 = terms[index]
        term2 = terms[index + 1]
        print(f"\nKeyword 1: {term1}, Search volume: {search_data[term1]}")
        print(f"Keyword 2: {term2}, Search volume unknown")

        guess = input("Do you think Keyword 2 has a Higher (H) or Lower (L) search volume? (Enter H or L): ").upper()

        # Check for valid input
        if guess not in ['H', 'L']:
            print("Invalid input, please enter 'H' or 'L'.")
            continue

        # Compare search volumes
        if (guess == 'H' and search_data[term2] > search_data[term1]) or \
           (guess == 'L' and search_data[term2] < search_data[term1]):
            score += 1
            print(f"Correct! {term2} has a search volume of: {search_data[term2]}")
        else:
            print(f"Wrong! {term2} has a search volume of: {search_data[term2]}")
            print(f"Your final score is: {score}")
            break

        index += 1

    # If the player guesses through all terms
    if index == len(terms) - 1:
        print(f"You've guessed all the keywords! Final score: {score}")

# Start the game
if __name__ == "__main__":
    play_higher_lower()
