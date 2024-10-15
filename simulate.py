#!/usr/bin/env python3

import random
import sys
import statistics
import tabulate

class Deck():
    "Class to represent a standard 52 deck of playing cards"

    def __init__(self):
        self.cards = []
        self.reset()
        self.shuffle()

    def reset(self, exclude = []):
        """Re-initialise the deck with all cards"""
        self.cards = [(value, suit)  for suit in ("D", "C", "H", "S") for value in range(1, 14) if (value, suit) not in exclude]
        

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        """Take a card from the deck, removing it (so it can't be removed again)."""
        return self.cards.pop()


def game(num_cards):
    """
    Play a game of ride-the-bus.

    :param num_cards: How many cards the player needs to beat.
    """
    deck = Deck()
    
    # First, draw our home cards.
    home_cards = [[deck.draw()] for _ in range (0, num_cards)]

    rounds = 0
    shuffles = 1
    won = False
    # Play
    while not won:
        # Start again.
        rounds +=1
        for index in range(len(home_cards)):
            # First, if the deck is empty, refresh.
            if len(deck.cards) == 0:
                #print("Out of cards! Shuffling ... ", end = "")
                shuffles += 1
                # Keep the top most cards, discard everything else.
                home_cards = [[home_cards[index][-1]] for index in range (0, num_cards)]

                # Shuffle other cards into deck.
                deck.reset(exclude = [stack[0] for stack in home_cards])
                deck.shuffle()
                #print(" there are now {} cards in the deck".format(len(deck.cards)))

            home_stack = home_cards[index]
            # We need to beat the top-most card.
            card_to_beat = home_stack[-1]
            #print("Card {} of {}, trying to beat a {}... ".format(index +1, len(home_cards), card_to_beat[0]), end = "")

            # This is the card we're going to be given.
            next_card = deck.draw()

            # Without card-counting, we simply decide based on the card value.
            # If we need to beat a 6 or below, we'll guess high.
            # If we need to beat an 8 or above, we'll guess low.
            # For a 7, we'll guess randomly.
            #
            # We can also guess 'same', but this is never an optimal call.
            # Regardless of what we guess, if we get an ace, we're wrong.
            try:
                if next_card[0] == 1:
                    # Pulled an ace.
                    #print("but got an ace")
                    break

                elif card_to_beat[0] >= 8:
                    #print("guessing low...", end = "")
                    # We'll guess low.
                    if next_card[0] >= card_to_beat[0]:
                        # Wrong, go again.
                        #print(" but got a {}".format(next_card[0]))
                        break

                elif card_to_beat[0] <= 6:
                    #print(" guessing high ...", end = "")
                    # We'll guess high.
                    if next_card[0] <= card_to_beat[0]:
                        # Wrong, go again.
                        #print(" but got a {}".format(next_card[0]))
                        break

                else:
                    # A 7, guess randomly.
                    if random.getrandbits(1):
                        #print(" guessing low ...", end = "")
                        # We'll guess low.
                        if next_card[0] >= card_to_beat[0]:
                            # Wrong, go again.
                            #print(" but got a {}".format(next_card[0]))
                            break
                    else:
                        #print(" guessing high ...", end = "")
                        # We'll guess high.
                        if next_card[0] <= card_to_beat[0]:
                            # Wrong, go again.
                            #print(" but got a {}".format(next_card[0]))
                            break

                #print(" and got a {}!".format(next_card[0]))
                # Have we won?
                if index == len(home_cards) -1:
                    # Yes!
                    #print("Finally won after {} rounds!".format(rounds))
                    won = True

            finally:
                # Add card to stack.
                home_stack.append(next_card)

    return rounds, shuffles

        
def main():
    iters = 10000
    num_cards = int(sys.argv[1])
    results = [game(num_cards) for iter in range(iters)]

    rounds = [result[0] for result in results]
    shuffles = [result[1] for result in results]

    average = sum(rounds) / len(rounds)

    headers = ["Num cards", "average rounds", "stddev", "min", "max"]
    data = [num_cards, average, statistics.stdev(rounds), min(rounds), max(rounds)]

    odds = {rounds_taken: len([res for res in rounds if res <= rounds_taken]) / iters for rounds_taken in range(1,100)}
    headers += odds.keys()
    data += odds.values()
    #print(",".join([str(item) for item in headers]))
    print(",".join([str(item) for item in data]))
    #print(tabulate.tabulate([data], headers= headers))

#    print("For {} cards, average rounds =  {:.1f}  (±{:.1f}), min = {}, max = {}".format(num_cards, average, statistics.stdev(rounds), min(rounds), max(rounds)))
#    print(odds)
    
# If we've been invoked as a program, call main().    
if __name__ == '__main__':
    sys.exit(main())
    
