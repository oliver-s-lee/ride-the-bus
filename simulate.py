#!/usr/bin/env python3

import random
import sys
import statistics
import tabulate
import argparse
import logging

logger = logging.getLogger()

class Player():
    "Someone who plays the game. ABC."

    def __init__(self, ace_rule):
        """
        :param ace_rule: Are aces always wrong?
        """
        self.ace_rule = ace_rule

    def play(self, card_to_beat, *args, **kwargs):
        """
        Make the player play the game.

        The player will 'guess' whether to go "higher", "lower", or the "same" as the current card they need to beat.
        Some players need to know how many cards are left in the deck.
        """
        raise NotImplementedError("Implement in subclass")
    

class Random(Player):
    """
    A player that makes bad decisions.
    """

    def play(*args, **kwargs):
        return random.choice(["higher", "lower"])

class Blind(Player):
    """
    A player who cannot card-count at all.

    This player bases their decisions solely on the current card at play.
    """

    def play(self, card_to_beat, *args, **kwargs):
        """
        If we need to beat a 6 or below, we'll guess high.
        If we need to beat an 8 or above, we'll guess low.
        For a 7, we'll guess randomly.
        We never guess 'same'.
        """
        if card_to_beat[0] >= 8:
            # We'll guess low.
            return "lower"

        elif card_to_beat[0] <= 6:
            # We'll guess high.
            return "higher"

        else:
            # A 7, guess randomly.
            if random.getrandbits(1):
                return "lower"
            
            else:
                return "higher"
            
class Counter(Player):
    """
    A player that always makes the best decision, based on which cards are remaining.
    """

    def play(self, card_to_beat, deck, *args, **kwargs):
        """"""
        # First, work out how many cards are of each type.
        choices = [
            ["higher", len([card for card in deck.cards if card[0] > card_to_beat[0] and (not self.ace_rule or card[0] != 1)])],
            ["lower", len([card for card in deck.cards if card[0] < card_to_beat[0] and (not self.ace_rule or card[0] != 1)])],
            # The ace rule does not affect 'same'.
            ["same", len([card for card in deck.cards if card[0] == card_to_beat[0]])]
        ]

        choices.sort(key = lambda item: -(item[1]))
        # Keep only good solutions.
        choices = [choice for choice in choices if choice[1] == choices[0][1]]
        
        # Pick from the remaining solutions.
        # If one is clearly better, just do that.
        # If several are equally likely, guess.
        return random.choice(choices)[0]

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


def play(num_cards, player):
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
                logger.info("Out of cards! Shuffling ... ", end = "")
                shuffles += 1
                # Keep the top most cards, discard everything else.
                home_cards = [[home_cards[index][-1]] for index in range (0, num_cards)]

                # Shuffle other cards into deck.
                deck.reset(exclude = [stack[0] for stack in home_cards])
                deck.shuffle()
                logger.info(" there are now {} cards in the deck".format(len(deck.cards)))

            home_stack = home_cards[index]
            # We need to beat the top-most card.
            card_to_beat = home_stack[-1]
            logger.info("Card {} of {}, trying to beat a {}... ".format(index +1, len(home_cards), card_to_beat[0]), end = "")

            # Get the player's prediction.
            decision = player.play(card_to_beat, deck)
            logger.info("guessing {} ... ".format(decision), end = "")

            # Now draw the card.
            next_card = deck.draw()

            try:
                # Unless the player called same, if we draw an ace, they lose.
                if next_card[0] == 1:
                    if decision == "same" and card_to_beat[0] == 1:
                        logger.info("and got an ace! (Dodged!)")
                        pass
                    
                    else:
                        logger.info("but got an ace")
                        break

                elif decision == "lower" and next_card[0] >= card_to_beat[0]:
                    # Wrong, go again.
                    logger.info("but got a {}".format(next_card[0]))
                    break

                elif decision == "higher" and next_card[0] <= card_to_beat[0]:
                    # Wrong, go again.
                    logger.info("but got a {}".format(next_card[0]))
                    break

                elif decision == "same" and next_card[0] != card_to_beat[0]:
                    # Nope.
                    break

                elif decision not in ["lower", "higher", "same"]:
                   # We didn't understand the player.
                   raise Exception("The player is cheating! I do not understand '{}'".format(decision))

                logger.info("and got a {}!".format(next_card[0]))
                # Have we won?
                if index == len(home_cards) -1:
                    # Yes!
                    logger.info("Finally won after {} rounds!".format(rounds))
                    won = True

            finally:
                # Add card to stack.
                home_stack.append(next_card)

    return rounds, shuffles

        
def main(games, iters = 10000, player_cls = Counter):
    player = player_cls(True)

    headers = ["Num cards", "average rounds", "stddev", "min", "max"] + list(range(1,100))
    print(",".join([str(item) for item in headers]))

    for num_cards in games:

        results = [play(num_cards, player) for iter in range(iters)]
        rounds = [result[0] for result in results]
        shuffles = [result[1] for result in results]

        average = sum(rounds) / len(rounds)
        data = [num_cards, average, statistics.stdev(rounds), min(rounds), max(rounds)]

        odds = {rounds_taken: len([res for res in rounds if res <= rounds_taken]) / iters for rounds_taken in range(1,100)}
    # headers += odds.keys()
        data += odds.values()
        print(",".join([str(item) for item in data]))
    #print(tabulate.tabulate([data], headers= headers))

#    print("For {} cards, average rounds =  {:.1f}  (±{:.1f}), min = {}, max = {}".format(num_cards, average, statistics.stdev(rounds), min(rounds), max(rounds)))
#    print(odds)
    
# If we've been invoked as a program, call main().    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    
    parser.add_argument("num_cards", type = int, nargs = "+")
    parser.add_argument("-i", "--iterations", type = int, default = 10000)
    parser.add_argument("-p", "--player", choices = ["random", "blind", "counter"], default = "blind")

    args = parser.parse_args()
    if args.player == "blind":
        player = Blind
    
    elif args.player == "counter":
        player = Counter
    
    elif args.player == "random":
        player = Random

    sys.exit(main(args.num_cards, args.iterations, player))
    
