from time import time
from BFS import BFS
from IDS import IDS


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

    my_ids = IDS(characterized_map)
    my_ids.start()
    my_ids.print_solution(delay=0.2)

    end = time()
    print("Time: " + str(end - start) + "s")


main()
