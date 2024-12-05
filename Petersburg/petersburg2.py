# Cmput 455 sample code
# Second simulation for the St. Petersburg paradox game.
# Keep playing the St. Petersburg Paradox. 
# Print average and maximum payoff after every 2^n experiments.
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

#-----------------------------------------------------------------------------
random.seed() # initialize random generator
score = 0
printTime = 2
maxWin = 0
for round in range(1000000000):
    win = simulate_petersburg()
    score += win
    if win > maxWin:
        maxWin = win
    if round+1 >= printTime:
        print("Average score after {} rounds: {:.2f}, max. win {}".
            format(round + 1, score/(round+1), maxWin))
        printTime *= 2
