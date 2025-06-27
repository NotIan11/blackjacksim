import random
import time

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

        while dealer_value < 17:
            deck, running_count = check_reshuffle(deck,running_count=running_count)
            card = draw_card(deck)
            dealer_hand.append(card)
            dealer_value = optimal_hand(dealer_hand)

            running_count += count(card)

            print("Dealer Hand:", dealer_hand)
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
            print("Hand:", hand)
            time.sleep(1)

            print("Value:", value)

            if value > 21:
                print("Bust! You lose!")
                time.sleep(1)
                print("Dealer Hand:", dealer_hand)
                time.sleep(1)
                print("Balance:", balance)
                break
        
        ## Standing ##
        
        elif action =="stand":
            print("Final Hand:",hand)
            time.sleep(1)
            print("Final Value:", value)
            time.sleep(1)
            print("You Chose to Stand.")

            time.sleep(1)

            print("Dealer Hand:", dealer_hand)
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
            print("Hand:", hand)
            time.sleep(1)

            print("Value:", value)

            if value > 21:
                print("Bust! You lose!")
                time.sleep(1)
                print("Dealer Hand:", dealer_hand)
                time.sleep(1)
                print("Balance:", balance)
                break

            else:
                print("You doubled. No more cards!")

                print("Final Hand:",hand)
                time.sleep(1)

                print("Final Value:", value)
                time.sleep(1)

                print("Dealer Hand:", dealer_hand)
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
                for h in split_hands:
                    for card in h[1:]:
                        running_count += count(card)
                    print(f"\nPlaying split hand: {h}")
                    deck, balance, bet, running_count = post_hand_play(
                        h, optimal_hand(h), deck, dealer_hand[:], dealer_value, balance, bet, running_count
                    )
                break

        else: 
            print("Invalid. Please hit or stand.")
    return deck, balance, bet, running_count

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

    print("Starting Hand:", hand, "\n", "Starting Value:", value)
    print("Dealer Hand:", shown_hand)

    if value == 21 and dealer_value != 21:
        balance += bet*2.5
        time.sleep(1)
        print("Blackjack! You win!")
        time.sleep(1)
        print("Balance:", balance)

    elif value != 21 and dealer_value == 21:
        time.sleep(1)
        print("Dealer Hand:", dealer_hand)
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

    
    
    
   