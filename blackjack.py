import random
import time

## Card Display Functions ##

def get_card_art(card):
    """
    Convert a card to ASCII art representation
    """
    if card == 'A':
        rank = 'A'
    elif card in ['J', 'Q', 'K']:
        rank = card
    else:
        rank = str(card)
    
    # Pad single digits with space for alignment
    if len(rank) == 1:
        rank = rank + ' '
    
    card_art = [
        f"┌─────────┐",
        f"│ {rank}      │",
        f"│         │",
        f"│         │",
        f"│         │",
        f"│      {rank} │",
        f"└─────────┘"
    ]
    return card_art

def get_hidden_card_art():
    """
    Return ASCII art for a hidden card
    """
    return [
        "┌─────────┐",
        "│ █ █ █ █ │",
        "│ █ █ █ █ │",
        "│ █ █ █ █ │",
        "│ █ █ █ █ │",
        "│ █ █ █ █ │",
        "└─────────┘"
    ]

def display_hand(hand, title="Hand", hide_second=False):
    """
    Display a hand of cards as ASCII art
    """
    print(f"\n{title}:")
    
    if not hand:
        print("No cards")
        return
    
    # Get card art for each card
    cards_art = []
    for i, card in enumerate(hand):
        if hide_second and i == 1:
            cards_art.append(get_hidden_card_art())
        else:
            cards_art.append(get_card_art(card))
    
    # Display cards side by side
    for row in range(7):  # Each card has 7 rows
        line = ""
        for card_art in cards_art:
            line += card_art[row] + " "
        print(line)
    
    # Show hand value if not hiding cards
    if not hide_second:
        value = optimal_hand(hand)
        print(f"Value: {value}")

def display_dealer_hand(dealer_hand, hide_second=True):
    """
    Display dealer's hand, optionally hiding the second card
    """
    display_hand(dealer_hand, "Dealer Hand", hide_second)

def display_player_hand(hand):
    """
    Display player's hand
    """
    display_hand(hand, "Your Hand")

## Starting Hand ##

face_values = {
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11
}

def create_deck(num_decks=1):
    single_deck = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']*4
    return single_deck*num_decks

def draw_card(deck):
    if len(deck) == 0:
        raise ValueError("Deck is Empty!")
    card = random.choice(deck)
    deck.remove(card)
    return card

def check_reshuffle(deck, min_cards=8, num_decks=1,running_count=0):
    if len(deck) < min_cards:
        print("Too few cards. Reshuffling deck.")
        return create_deck(num_decks), 0
    return deck, running_count


def optimal_hand(hand):
    value = 0
    high_ace_count = 0

    for card in hand:
        if isinstance(card,int):
            value += card
        elif card == 'A':
            value += 11
            high_ace_count += 1
        else: 
            value += face_values[card]
    
    while value > 21 and high_ace_count:
        value -= 10
        high_ace_count -= 1
    return(value)


def is_soft_17(hand):
    """
    Check if a hand is a soft 17 (equals 17 with an Ace counted as 11)
    """
    value = 0
    high_ace_count = 0

    for card in hand:
        if isinstance(card, int):
            value += card
        elif card == 'A':
            value += 11
            high_ace_count += 1
        else: 
            value += face_values[card]
    
    # If the hand equals 17 and has at least one Ace counted as 11, it's soft
    if value == 17 and high_ace_count > 0:
        return True
    
    return False


## Betting ##

def betting(balance, running_count):
    while True:
        try:
            wager = int(input(f"You have {balance} chips. How much would you like to bet? Please enter an integer value. The count is {running_count}."))

            if wager <= 0:
                print("You can't bet on the dealer in blackjack! Please bet a positive amount.")
            elif wager > balance:
                print("Stop trying to bet money you don't have!")
            else:
                print(f"You have successfully bet {wager} chips. Dealing now.")
                return wager
        except ValueError:
            print("Please bet a valid integer. No slicing chips here.")

## The Dealer ##

def dealer(deck,dealer_value,dealer_hand,running_count):

    while True:

        # Hit on any hand below 17 OR on a soft 17
        while dealer_value < 17 or (dealer_value == 17 and is_soft_17(dealer_hand)):
            deck, running_count = check_reshuffle(deck,running_count=running_count)
            card = draw_card(deck)
            dealer_hand.append(card)
            dealer_value = optimal_hand(dealer_hand)

            running_count += count(card)

            display_dealer_hand(dealer_hand, hide_second=False)
            time.sleep(1)

            
            if dealer_value > 21:
                print("Dealer busts!")
                break

        return dealer_hand, dealer_value, deck, running_count

## Player Actions ##
def post_hand_play(hand, value, deck, dealer_hand, dealer_value,balance,bet,running_count):

    while True:
        if hand[0] == hand[1]:
            action = input(f"Hit, Stand, Double, or Split? The count is {running_count}.").lower()
        else:
            action = input(f"Hit, Stand, or Double? The count is {running_count}.").lower()

        ## Hitting ##

        if action =="hit":
            deck, running_count =check_reshuffle(deck,running_count=running_count)
            card = draw_card(deck)
            hand.append(card)
            running_count += count(card)
            print(f"You drew a {card}.")
            time.sleep(1)

            value = optimal_hand(hand)
            display_player_hand(hand)
            time.sleep(1)


            if value > 21:
                print("Bust! You lose!")
                time.sleep(1)
                display_dealer_hand(dealer_hand, hide_second=False)
                time.sleep(1)
                print("Balance:", balance)
                break
        
        ## Standing ##
        
        elif action =="stand":
            print("Final Hand:")
            display_player_hand(hand)
            time.sleep(1)
            print("You Chose to Stand.")

            time.sleep(1)

            display_dealer_hand(dealer_hand, hide_second=False)
            time.sleep(1)

            dealer_hand, dealer_value, deck, running_count = dealer(deck, dealer_value, dealer_hand, running_count)

            print("Dealer Value:", dealer_value)

            if dealer_value > value and dealer_value <= 21:
                print("Dealer Wins! You Lose!")
                time.sleep(1)
                print("Balance:", balance)
                break
            elif dealer_value == value:
                balance += bet
                print("Tie! It's a Push!")
                time.sleep(1)
                print("Balance:", balance)
                break
            else:
                balance += bet*2
                print("You Win!")
                time.sleep(1)
                print("Balance:", balance)
                break
        
        ## Doubling ##

        elif action == "double":
            if balance < bet:
                print("You don't have enough money to double.")
                continue
            balance -= bet  
            bet *= 2        


            deck, running_count =check_reshuffle(deck, running_count=running_count)
            card = draw_card(deck)
            hand.append(card)
            running_count += count(card)
            print(f"You drew a {card}.")
            time.sleep(1)

            value = optimal_hand(hand)
            display_player_hand(hand)
            time.sleep(1)


            if value > 21:
                print("Bust! You lose!")
                time.sleep(1)
                display_dealer_hand(dealer_hand, hide_second=False)
                time.sleep(1)
                print("Balance:", balance)
                break

            else:
                print("You doubled. No more cards!")

                print("Final Hand:")
                display_player_hand(hand)
                time.sleep(1)

                display_dealer_hand(dealer_hand, hide_second=False)
                time.sleep(1)

                dealer_hand, dealer_value, deck, running_count = dealer(deck, dealer_value, dealer_hand, running_count)

                if dealer_value > value and dealer_value <= 21:
                    print("Dealer Wins! You Lose!")
                    time.sleep(1)
                    print("Balance:", balance)
                    break
                elif dealer_value == value:
                    balance += bet
                    print("Tie! It's a Push!")
                    time.sleep(1)
                    print("Balance:", balance)
                    break
                else:
                    balance += bet*2
                    print("You Win!")
                    time.sleep(1)
                    print("Balance:", balance)
                    break
        
        ## Splitting ##
        elif action == "split":
            if bet > balance:
                print("Not enough money to split.")
                continue
            else:
                balance -= bet
                split_hands = [
                    [hand[0], draw_card(deck)],
                    [hand[1], draw_card(deck)]
                ]

                split_results =[]

                for h in split_hands:
                    for card in h[1:]:
                        running_count += count(card)
                    print(f"\nPlaying split hand:")
                    display_player_hand(h)
                    final_hand, final_value, final_bet, running_count = split_hand_play(h, optimal_hand(h), deck, balance, bet, running_count)
                    split_results.append((final_hand,final_value,final_bet))
                
                time.sleep(1)

                display_dealer_hand(dealer_hand, hide_second=False)
                time.sleep(1)

                dealer_hand, dealer_value, deck, running_count = dealer(deck, dealer_value, dealer_hand, running_count)

                print("Dealer Value:", dealer_value)

                for final_hand, final_value, final_bet in split_results:
                     print(f"\nSplit Hand Result:")
                     display_player_hand(final_hand)
                     if final_value > 21:
                        print("You busted this hand.")
                     elif dealer_value > 21 or final_value > dealer_value:
                        balance += final_bet * 2
                        print("You win this hand!")
                     elif dealer_value == final_value:
                        balance += final_bet
                        print("Push on this hand.")
                     else:
                        print("Dealer wins this hand.")
                     time.sleep(1)

                print("Balance:", balance)
                break
                    

        else: 
            print("Invalid. Please hit or stand.")
    return deck, balance, bet, running_count


## Split Hand Play

def split_hand_play(hand, value, deck,balance,bet,running_count):

    while True:
        action = input(f"Hit, Stand, or Double? The count is {running_count}.").lower()

        ## Hitting ##

        if action =="hit":
            deck, running_count =check_reshuffle(deck,running_count=running_count)
            card = draw_card(deck)
            hand.append(card)
            running_count += count(card)
            print(f"You drew a {card}.")
            time.sleep(1)

            value = optimal_hand(hand)
            display_player_hand(hand)
            time.sleep(1)


            if value > 21:
                print("Bust! You lose!")
                time.sleep(1)
                break

            ## Standing ##
        
        elif action =="stand":
            print("Final Hand:")
            display_player_hand(hand)
            time.sleep(1)
            print("Final Value:", value)
            time.sleep(1)
            print("You Chose to Stand.")
            break

        
        ## Doubling ##

        elif action == "double":
            if balance < bet:
                print("You don't have enough money to double.")
                continue
            balance -= bet  
            bet *= 2        


            deck, running_count =check_reshuffle(deck, running_count=running_count)
            card = draw_card(deck)
            hand.append(card)
            running_count += count(card)
            print(f"You drew a {card}.")
            time.sleep(1)

            value = optimal_hand(hand)
            display_player_hand(hand)
     
            if value > 21:
                print("Bust! You lose!")
                time.sleep(1)
                break

            else:
                print("You doubled. No more cards!")

                print("Final Hand:")
                display_player_hand(hand)
                time.sleep(1)

                print("Final Value:", value)
                time.sleep(1)
                break

    return hand, value, bet, running_count



## Counting Cards ##

def count(card):
    positives = [2,3,4,5,6]
    neutrals = [7,8,9]
    negatives = [10,'J','Q','K','A']

    if card in positives:
        return 1
    elif card in neutrals:
        return 0
    elif card in negatives:
        return -1
    else:
        return 0





## Start Play ##
balance = 1000
deck = create_deck()
running_count =0

while True:
    print("\n--- New Round ---\n")

    deck, running_count = check_reshuffle(deck,running_count=running_count)

    bet = betting(balance,running_count)
    balance -= bet

    hand = [draw_card(deck), draw_card(deck)]
    value = optimal_hand(hand)

    for card in hand:
        running_count += count(card)

    dealer_hand = [draw_card(deck), draw_card(deck)]
    dealer_value = optimal_hand(dealer_hand)

    for card in dealer_hand:
        running_count += count(card)

    shown_hand = [dealer_hand[0], '?']

    display_player_hand(hand)
    display_dealer_hand(dealer_hand, hide_second=True)

    if value == 21 and dealer_value != 21:
        balance += bet*2.5
        time.sleep(1)
        print("Blackjack! You win!")
        time.sleep(1)
        print("Balance:", balance)

    elif value != 21 and dealer_value == 21:
        time.sleep(1)
        display_dealer_hand(dealer_hand, hide_second=False)
        time.sleep(1)
        print("Dealer Blackjack! You lose!")
        time.sleep(1)
        print("Balance:", balance)

    else:
        deck, balance, bet, running_count = post_hand_play(hand, value, deck, dealer_hand, dealer_value,balance, bet, running_count)


    again = input("\n Play another hand? (y/n)").lower()
    if again != 'y':
        print("Thanks for playing!")
        break
    elif balance <= 0:
        print("You have no money. Go home!")
        break

    
    
    
   