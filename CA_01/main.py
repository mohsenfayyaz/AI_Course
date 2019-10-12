import copy
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import system, name
from time import sleep
from queue import Queue

P_CHAR = "P"
Q_CHAR = "Q"
WALL_CHAR = "%"
EMPTY_CHAR = " "
P_FOOD = "1"
Q_FOOD = "2"
BOTH_FOOD = "3"


def main():
    with open('test', 'r') as file:
        pac_map = file.read().splitlines()

    characterized_map = list()
    for line in pac_map:
        characterized_map.append(list(line))

    my_bfs = BFS(characterized_map)
    my_bfs.start()
    my_bfs.print_solution()


def find_in_map(the_map, char):
    for line in the_map:
        if char in line:
            return the_map.index(line), line.index(char)


class State:
    def __init__(self, map_data, parent=None):
        self.map_data = map_data
        self.parent = parent
        self.hash = ''.join(''.join(item) for item in map_data).replace("%", "")

    def get_hash(self):
        return self.hash

    def get_map(self):
        return self.map_data

    def get_parent(self):
        return self.parent


class Pac_map_handler:
    @staticmethod
    def is_in_map(pac_map: list, row, col):
        return 0 <= row < len(pac_map) and 0 <= col < len(pac_map[0])

    @staticmethod
    def can_p_goto(pac_map: list, row, col):
        return Pac_map_handler.is_in_map(pac_map, row, col) and pac_map[row][col] in {P_FOOD, EMPTY_CHAR, BOTH_FOOD}

    @staticmethod
    def can_q_goto(pac_map: list, row, col):
        return Pac_map_handler.is_in_map(pac_map, row, col) and pac_map[row][col] in {Q_FOOD, EMPTY_CHAR, BOTH_FOOD}

    # P MOVEMENT
    @staticmethod
    def move_p_right(pac_map, row, col):
        if Pac_map_handler.can_p_goto(pac_map, row, col + 1):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row][col + 1] = P_CHAR
        return pac_map

    @staticmethod
    def move_p_left(pac_map, row, col):
        if Pac_map_handler.can_p_goto(pac_map, row, col - 1):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row][col - 1] = P_CHAR
        return pac_map

    @staticmethod
    def move_p_up(pac_map, row, col):
        if Pac_map_handler.can_p_goto(pac_map, row - 1, col):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row - 1][col] = P_CHAR
        return pac_map

    @staticmethod
    def move_p_down(pac_map, row, col):
        if Pac_map_handler.can_p_goto(pac_map, row + 1, col):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row + 1][col] = P_CHAR
        return pac_map

    # Q MOVEMENT
    @staticmethod
    def move_q_right(pac_map, row, col):
        if Pac_map_handler.can_q_goto(pac_map, row, col + 1):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row][col + 1] = Q_CHAR
        return pac_map

    @staticmethod
    def move_q_left(pac_map, row, col):
        if Pac_map_handler.can_q_goto(pac_map, row, col - 1):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row][col - 1] = Q_CHAR
        return pac_map

    @staticmethod
    def move_q_up(pac_map, row, col):
        if Pac_map_handler.can_q_goto(pac_map, row - 1, col):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row - 1][col] = Q_CHAR
        return pac_map

    @staticmethod
    def move_q_down(pac_map, row, col):
        if Pac_map_handler.can_q_goto(pac_map, row + 1, col):
            pac_map[row][col] = EMPTY_CHAR
            pac_map[row + 1][col] = Q_CHAR
        return pac_map


class BFS:
    def __init__(self, pac_map):
        self.start_state = State(pac_map, None)
        self.explored_states_hash = set()
        self.frontier_states = Queue()
        self.goal_state = None

    def start(self):
        self.frontier_states = Queue()
        self.frontier_states.put(self.start_state)
        self.explored_states_hash = set()
        counter = 0
        while not self.frontier_states.empty():
            print(counter)
            counter += 1;
            current_state = self.frontier_states.get()
            self.print_map(current_state.get_map())
            if self.are_constraints_satisfied(current_state):
                self.goal_state = current_state
                return True

            self.explored_states_hash.add(current_state.get_hash())
            if self.do_actions(current_state):
                return True

        return False

    def print_solution(self):
        if self.goal_state is None:
            print("No Solution!")
        else:
            current_state = self.goal_state
            while current_state is not None:
                clear()
                self.print_map(current_state.get_map())
                current_state = current_state.get_parent()
                sleep(1)

    def print_map(self, pac_map):
        print('\n'.join(''.join(item) for item in pac_map))

    def are_constraints_satisfied(self, state: State):
        for line in state.get_map():
            if P_FOOD in line or Q_FOOD in line or BOTH_FOOD in line:
                return False
        return True

    def do_actions(self, current_state):
        pac_map = current_state.get_map()
        p_row, p_col = find_in_map(pac_map, P_CHAR)
        q_row, q_col = find_in_map(pac_map, Q_CHAR)
        # P MOVEMENT
        if self.move_p(current_state, pac_map, p_row, p_col):
            return True
        # Q MOVEMENT
        if self.move_q(current_state, pac_map, q_row, q_col):
            return True

    def move_p(self, current_state, pac_map, row, col):
        new_map = Pac_map_handler.move_p_right(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        new_map = Pac_map_handler.move_p_left(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        new_map = Pac_map_handler.move_p_up(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        new_map = Pac_map_handler.move_p_down(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        return False

    def move_q(self, current_state, pac_map, row, col):
        new_map = Pac_map_handler.move_q_right(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        new_map = Pac_map_handler.move_q_left(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        new_map = Pac_map_handler.move_q_up(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        new_map = Pac_map_handler.move_q_down(copy.deepcopy(pac_map), row, col)
        if self.add_to_frontier(new_map, current_state):
            return True

        return False

    def add_to_frontier(self, new_map, current_state):
        new_state = State(new_map, current_state)
        if not new_state.get_hash() in self.explored_states_hash:
            self.frontier_states.put(new_state)
            if self.are_constraints_satisfied(new_state):
                self.goal_state = new_state
                return True
        return False

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


main()
