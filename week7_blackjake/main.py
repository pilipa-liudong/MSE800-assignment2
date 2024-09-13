import random
import os

# Create a deck of cards with values
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # 11 represents Ace

def deal_card():
    """Deals a random card from the deck."""
    return random.choice(deck)

def calculate_score(cards):
    """Calculates the score for a given hand of cards."""
    score = sum(cards)
    # If there's an Ace and the score is over 21, count Ace as 1 instead of 11
    if score > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)
        score = sum(cards)
    return score

def check_blackjack(cards):
    """Check if a hand is a Blackjack."""
    return sum(cards) == 21 and len(cards) == 2

def clear_console():
    """Clears the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def play_blackjack():
    """Plays a game of Blackjack."""
    while True:
        # Deal initial cards to user and computer
        user_cards = [deal_card(), deal_card()]
        computer_cards = [deal_card(), deal_card()]

        game_over = False

        # Show the computer's first card
        print(f"Computer's first card: {computer_cards[0]}")

        # Check for blackjack
        if check_blackjack(computer_cards):
            print(f"Computer has Blackjack! Computer's hand: {computer_cards}")
            game_over = True
        elif check_blackjack(user_cards):
            print(f"You have Blackjack! Your hand: {user_cards}")
            if not check_blackjack(computer_cards):
                game_over = True

        # User's turn
        while not game_over:
            user_score = calculate_score(user_cards)
            print(f"Your hand: {user_cards} | Current score: {user_score}")
            if user_score > 21:
                print("You went over 21! You lose.")
                game_over = True
                break

            user_choice = input("Type 'y' to get another card, or 'n' to pass: ").lower()
            if user_choice == 'y':
                user_cards.append(deal_card())
            else:
                break

        # Computer's turn
        while calculate_score(computer_cards) < 17 and not game_over:
            computer_cards.append(deal_card())

        # Final comparison of scores
        if not game_over:
            user_score = calculate_score(user_cards)
            computer_score = calculate_score(computer_cards)

            print(f"Your final hand: {user_cards} | Final score: {user_score}")
            print(f"Computer's final hand: {computer_cards} | Final score: {computer_score}")

            if computer_score > 21:
                print("Computer went over 21. You win!")
            elif user_score > 21:
                print("You went over 21! You lose.")
            elif user_score > computer_score:
                print("You win!")
            elif user_score < computer_score:
                print("You lose.")
            else:
                print("It's a draw!")

        # Ask if the player wants to play again
        play_again = input("Do you want to play again? Type 'y' to continue, or 'n' to exit: ").lower()
        if play_again == 'y':
            clear_console()
        else:
            break

if __name__ == "__main__":
    play_blackjack()
