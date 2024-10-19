#!/usr/bin/env python3

import sys
import csv
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

def main():
    datas = {
        "counter_aceless.csv": {"color": (1., 0.258823529, 0.054901961)},
        #"blind_aceless.csv": {"color": (0, 0.270588235, 0.525490196)}
    }

    plt.xlabel("No. Cards")
    plt.ylabel("No. Rounds (average)")
    
    for filename in datas:
        with open(Path("Results", filename)) as csvfile:
            reader = csv.reader(csvfile)
            data = np.array(list(reader))
        
        # Discard header and convert to float
        numdata = data[1:9].astype(float)
        
        x = numdata[:,0]
        y = numdata[:,1]
        error = numdata[:,2]
        color = datas[filename]["color"]

        plt.plot(x, y, 'x-', color = color)
        plt.fill_between(x, y-error, y+error, edgecolor = (color[0], color[1], color[2], 1), facecolor = (color[0], color[1], color[2], 0.25))

    plt.show()
    
# If we've been invoked as a program, call main().    
if __name__ == '__main__':
#    parser = argparse.ArgumentParser(
#        prog='ProgramName',
#        description='What the program does',
#        epilog='Text at the bottom of help')
#    
#    parser.add_argument("num_cards", type = int, nargs = "+")
#    parser.add_argument("-i", "--iterations", type = int, default = 10000, help = "How many times to repeat each game")
#    parser.add_argument("-p", "--player", choices = ["random", "blind", "counter"], default = "blind", help = "The type of player. Default is 'blind'")
#    parser.add_argument("-V", "--verbose", action = "store_true", help = "Show the player's decisions as they play the game")
#    parser.add_argument("--odds", type = int, help = "How many rounds to show probabilities for", default = 50)
#    parser.add_argument("-a", "--no-ace-rule", help = "Make aces act normally", default = False, action  = "store_true")
#    parser.add_argument("-q", "--no-csv", help = "Don't print results in CSV", default = False, action  = "store_true")
#
#    args = parser.parse_args()
#
#    if args.player == "blind":
#        player = Blind
#    
#    elif args.player == "counter":
#        player = Counter
#    
#    elif args.player == "random":
#        player = Random
#
#    sys.exit(main(args.num_cards, args.iterations, player, verbose = args.verbose, odds = args.odds, ace_rule = not args.no_ace_rule, csv = not args.no_csv))
    sys.exit(main())
    
