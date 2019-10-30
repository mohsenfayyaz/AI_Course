import time

from CA_02.Game import *
from CA_02.MinimaxPlayer import MinimaxPlayer

if __name__ == '__main__':
    game = Game(8)
    # human1 = HumanPlayer(8)
    # human1.initialize('B')
    # human2 = HumanPlayer(8)
    # human2.initialize('W')

    p2 = RandomPlayer(8)
    p2.initialize('W')

    p1 = MinimaxPlayer(8)
    p1.initialize('B')

    start = time.time()
    game.playOneGame(p1, p2, False)
    end = time.time()

    print(end - start)