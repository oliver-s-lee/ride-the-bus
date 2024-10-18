#!/usr/bin/env python3

import random
import sys
import statistics
import argparse

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

class Game():
    "A class for representing a single game of ride the bus."

    def __init__(self, num_cards: int, player: Player, verbose: bool = False, ace_rule = True):
        self.num_cards = num_cards
        self.player = player
        self.verbose = verbose
        self.rounds = 0
        self.shuffles = 1
        self.deck = Deck()
        # First, draw our home cards.
        self.home_cards = [[self.deck.draw()] for _ in range (0, self.num_cards)]
        self.ace_rule = ace_rule

    def record(self, message, end = "\n"):
        if not self.verbose:
            return
        print(message, end = end, file = sys.stderr)

    def refresh(self):
        "Refresh the deck (because it has run out of cards)."
        # Keep the top most cards, discard everything else.
        self.home_cards = [[self.home_cards[index][-1]] for index in range (0, self.num_cards)]

        # Shuffle other cards into deck.
        self.deck.reset(exclude = [stack[0] for stack in self.home_cards])
        self.deck.shuffle()
        self.shuffles += 1

    def next(self, index):
        "Play the next card. Returns True if the player successfully beats the card."
        home_stack = self.home_cards[index]
        # We need to beat the top-most card.
        card_to_beat = home_stack[-1]
        self.record("Card {} of {}, trying to beat a {}... ".format(index +1, len(self.home_cards), card_to_beat[0]), end = "")

        # Get the player's prediction.
        decision = self.player.play(card_to_beat, self.deck)
        self.record("guessing {} ... ".format(decision), end = "")

        # Now draw the card.
        next_card = self.deck.draw()

        try:
            # If we're playing with the ace rule, an ace is always wrong unless the player called same on an ace.
            if self.ace_rule and next_card[0] == 1:
                if decision == "same" and card_to_beat[0] == 1:
                    self.record("and got an ace! (but dodged it)")
                    pass
                
                else:
                    self.record("but got an ace")
                    return False

            elif decision == "lower" and next_card[0] >= card_to_beat[0]:
                # Wrong, go again.
                self.record("but got a {}".format(next_card[0]))
                return False

            elif decision == "higher" and next_card[0] <= card_to_beat[0]:
                # Wrong, go again.
                self.record("but got a {}".format(next_card[0]))
                return False

            elif decision == "same" and next_card[0] != card_to_beat[0]:
                # Nope.
                return False

            elif decision not in ["lower", "higher", "same"]:
                # We didn't understand the player.
                raise Exception("The player is cheating! I do not understand '{}'".format(decision))

            self.record("and got a {}!".format(next_card[0]))
            return True

        finally:
            # Whatever happens, add the card to the stack.
            home_stack.append(next_card)


    def play(self):
        """
        Play a game of ride-the-bus.

        :param num_cards: How many cards the player needs to beat.
        """
        won = False
        # Play
        while not won:
            # Start again.
            self.rounds +=1
            for index in range(len(self.home_cards)):
                # First, if the deck is empty, refresh.
                if len(self.deck.cards) == 0:
                    self.record("Out of cards! Shuffling ... ", end = "")
                    self.refresh()
                    self.record(" there are now {} cards in the deck".format(len(self.deck.cards)))
                
                # Now play!
                if not self.next(index):
                    # We lost.
                    break

                # Have we won?
                if index == len(self.home_cards) -1:
                    # Yes!
                    self.record("----- Finally won after {} rounds! -----".format(self.rounds))
                    won = True
        
        return self.rounds, self.shuffles


def main(games, iters = 10000, player_cls = Counter, verbose = True, odds = 50, ace_rule = True, csv = True):
    player = player_cls(ace_rule = ace_rule)

    headers = ["Num cards", "average rounds", "stddev", "min", "max"] + list(range(1,100))
    if csv:
        print(",".join([str(item) for item in headers]))

    for num_cards in games:
        results = [Game(num_cards, player, verbose = verbose, ace_rule = ace_rule).play() for iter in range(iters)]
        rounds = [result[0] for result in results]
        shuffles = [result[1] for result in results]

        average = sum(rounds) / len(rounds)
        data = [num_cards, average, statistics.stdev(rounds) if len(rounds) > 1 else 0.0, min(rounds), max(rounds)]

        odds_data = {rounds_taken: len([res for res in rounds if res <= rounds_taken]) / iters for rounds_taken in range(1,odds)}
        data += odds_data.values()
        if csv:
            print(",".join([str(item) for item in data]))

        print("For {} cards, average rounds =  {:.1f}  (±{:.1f}), min = {}, max = {}".format(data[0], data[1], data[2], data[3], data[4]), file = sys.stderr)
    
# If we've been invoked as a program, call main().    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    
    parser.add_argument("num_cards", type = int, nargs = "+")
    parser.add_argument("-i", "--iterations", type = int, default = 10000)
    parser.add_argument("-p", "--player", choices = ["random", "blind", "counter"], default = "blind")
    parser.add_argument("-V", "--verbose", action = "store_true", help = "Show the player's decisions as they play the game")
    parser.add_argument("--odds", type = int, help = "How many rounds to show probabilities for", default = 50)
    parser.add_argument("-a", "--no-ace-rule", help = "Make aces act normally", default = False, action  = "store_true")
    parser.add_argument("-q", "--no-csv", help = "Don't print results in CSV", default = False, action  = "store_true")

    args = parser.parse_args()

    if args.player == "blind":
        player = Blind
    
    elif args.player == "counter":
        player = Counter
    
    elif args.player == "random":
        player = Random

    sys.exit(main(args.num_cards, args.iterations, player, verbose = args.verbose, odds = args.odds, ace_rule = not args.no_ace_rule, csv = not args.no_csv))
    
