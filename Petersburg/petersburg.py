# Cmput 455 sample code
# Simulation for the St. Petersburg paradox game.
# Play the St. Petersburg Paradox. 
# Place one bet, then the game is simulated 1000 times.
# Written by Martin Mueller

import random

def coinFlip():
    return random.random() < 0.5

def simulate_petersburg():
    pot = 2 # The bank puts $2 in the pot originally
    while True:
        if coinFlip(): # Each round you flip a coin
            return pot # If tail, the game ends and you win the whole pot
        else:
            pot *= 2 # If head, the bank doubles the pot

def record(histogram, value):
        if value in histogram:
            histogram[value] += 1
        else:
            histogram[value] = 1

def print_histogram(histogram):
    for key in sorted(histogram.keys()):
        print("{} occurred {} times".format(key, histogram[key]))

#-----------------------------------------------------------------------------
random.seed() # initialize random generator
bet = int(input("Your bet: "))
score = 0
histogram = dict()
for round in range(100):
    win = simulate_petersburg()
    print("You bet {} and gained {}, your win/loss is {}".format(bet, win, win - bet))
    score += win - bet
    record(histogram, win)
    print("Score after {} rounds: {}".format(round + 1, score))
print_histogram(histogram)
