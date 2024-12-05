# Cmput 455 sample code
# Alphabeta algorithm, depth-limited
# Written by Martin Mueller

from search_basics import INFINITY

# depth-limited alphabeta
def alphabetaDL(state, alpha, beta, depth):
    if state.endOfGame() or depth == 0:
        return state.staticallyEvaluateForToPlay() 
    for m in state.legalMoves():
        state.play(m)
        value = -alphabetaDL(state, -beta, -alpha, depth - 1)
        if value > alpha:
            alpha = value
        state.undoMove()
        if value >= beta: 
            return beta   # or value in failsoft (later)
    return alpha

# initial call with full window
def callAlphabetaDL(rootState, depth):
    return alphabetaDL(rootState, -INFINITY, INFINITY, depth)
