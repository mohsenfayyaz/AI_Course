import random
import time
from copy import deepcopy
from os import system, name
from IPython.core.display import clear_output
import numpy as np

from CA_02.Game import Game, Player


class MinimaxPlayer(Game, Player):
    def __init__(self, n, maxDepth=3):
        super().__init__(n)
        self.maxDepth = maxDepth - 1  # 0 based

    def initialize(self, side):
        self.side = side
        self.name = "MINIMAX"

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
        n = len(moves)
        if n == 0:
            return []
        else:
            start = time.time()
            bestMove = self.minimax(board, self.side)
            end = time.time()
            cls()
            print("Turn Time: " + str(end - start))
            return bestMove

    def evaluateFunction(self, board):
        selfPieces = 0
        opponentPieces = 0
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == self.side:
                    selfPieces += 1
                if board[r][c] == self.opponent(self.side):
                    opponentPieces += 1
        return (len(self.generateMoves(board, self.side)) + selfPieces) - \
               (len(self.generateMoves(board, self.opponent(self.side))) + opponentPieces)

    def minimax(self, board, currentSide, depth=0):
        moves = self.generateMoves(board, currentSide)
        if depth > self.maxDepth or len(moves) == 0:
            return self.evaluateFunction(board)

        if currentSide == self.side:  # MAXIMIZE
            maxAlpha = -np.inf
            for move in moves:
                newBoard = self.nextBoard(board, currentSide, move)
                moveValue = self.minimax(newBoard, self.opponent(currentSide), depth + 1)
                if moveValue > maxAlpha:
                    maxAlpha = moveValue
                    bestMove = move

            if depth == 0:
                return bestMove
            else:
                return maxAlpha

        else:  # MINIMIZE
            minBeta = np.inf
            for move in moves:
                newBoard = self.nextBoard(board, currentSide, move)
                moveValue = self.minimax(newBoard, self.opponent(currentSide), depth + 1)
                if moveValue < minBeta:
                    minBeta = moveValue

            return minBeta


def cls():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    clear_output(wait=True)
