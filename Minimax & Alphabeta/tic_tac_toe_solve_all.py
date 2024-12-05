# Cmput 455 sample code
# Solve all TicTacToe states in the DAG model
# Written by Martin Mueller

from game_basics import BLACK, WHITE, EMPTY, opponent
from tic_tac_toe import TicTacToe
from boolean_negamax_tt import negamaxBoolean
from transposition_table_simple import TranspositionTable

def printToPlayStats(d, toPlay, toPlayScoreAtDepth, oppScoreAtDepth):
    assert sum(toPlayScoreAtDepth) == sum(oppScoreAtDepth)
    bWins = oppScoreAtDepth[1]
    wWins = toPlayScoreAtDepth[0]
    draws = toPlayScoreAtDepth[1] - oppScoreAtDepth[1]
    if toPlay == WHITE: # swap colors
        bWins, wWins = wWins, bWins

    print("Depth {0}: {1} black, {2} draws, {3} white, {4} total positions".
          format(d, bWins, draws, wWins, sum(toPlayScoreAtDepth)))

def printStats(whiteScoreAtDepth, blackScoreAtDepth):
    toPlay = BLACK
    for d in range(10):
        if toPlay == BLACK:
            printToPlayStats(d, toPlay, 
                             blackScoreAtDepth[d], whiteScoreAtDepth[d])
        else:
            printToPlayStats(d, toPlay,
                             whiteScoreAtDepth[d], blackScoreAtDepth[d])
        toPlay = opponent(toPlay)

def solveTTTForColor(t, color, tt):
    t.setDrawWinner(color)
    scoreAtDepth = [x[:] for x in[[0] * 2] * 10]
    solveAtDepth(t, 0, scoreAtDepth, tt)
    return scoreAtDepth

def solveTTT():
    t = TicTacToe()
    ttw = TranspositionTable()
    whiteScoreAtDepth = solveTTTForColor(t, WHITE, ttw)
    ttb = TranspositionTable()
    blackScoreAtDepth = solveTTTForColor(t, BLACK, ttb)
    printStats(whiteScoreAtDepth, blackScoreAtDepth)

def solveAtDepth(state, depth, scoreAtDepth, tt):
    result = negamaxBoolean(state, tt)
    scoreAtDepth[depth][result] += 1
    if state.endOfGame():
        return
    for i in range(9):
        if state.board[i] == EMPTY:
            state.play(i)
            solveAtDepth(state, depth + 1, scoreAtDepth, tt)
            state.undoMove()

print("Solve all TicTacToe states black win/draw/white win")
solveTTT()
