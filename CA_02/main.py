import time

from CA_02.Game import *
from CA_02.MinimaxPlayer import MinimaxPlayer
from CA_02.MinimaxPrunedPlayer import MinimaxPrunedPlayer

if __name__ == '__main__':
    board_size = 8
    game = Game(board_size)
    # human1 = HumanPlayer(board_size)
    # human1.initialize('B')
    # human2 = HumanPlayer(board_size)
    # human2.initialize('W')

#     p2 = RandomPlayer(board_size)
#     p2.initialize('W')

#     p2 = SimplePlayer(board_size)
#     p2.initialize('W')

    p2 = MinimaxPlayer(board_size, 3)
    p2.initialize('W')

#     p2 = MinimaxPrunedPlayer(board_size, 4)
#     p2.initialize('W')

#     p1 = MinimaxPlayer(board_size, 4)
#     p1.initialize('B')
    p1 = MinimaxPrunedPlayer(board_size, 4)
    p1.initialize('B')

    start = time.time()
    game.playOneGame(p1, p2, True)
    end = time.time()

    print("Overal Time: ", end - start)