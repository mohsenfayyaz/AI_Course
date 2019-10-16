from time import time

from A_star import A_star
from BFS import BFS
from IDS import IDS
from PriorityQueue import PriorityQueue


def main():
    with open('test3', 'r') as file:
        pac_map = file.read().splitlines()

    characterized_map = list()
    for line in pac_map:
        characterized_map.append(list(line))

    print("Loading...")
    start = time()

    # my_bfs = BFS(characterized_map)
    # my_bfs.start()
    # my_bfs.print_solution(delay=0.2)

    # my_ids = IDS(characterized_map)
    # my_ids.start()
    # my_ids.print_solution(delay=0.1)

    my_a = A_star(characterized_map)
    my_a.start()
    my_a.print_solution(delay=0.1)

    end = time()
    print("Time: " + str(end - start) + "s")


main()
