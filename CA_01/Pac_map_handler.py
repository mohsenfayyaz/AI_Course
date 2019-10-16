from os import system, name
import sys
from IPython.display import clear_output

P_CHAR = "P"
Q_CHAR = "Q"
WALL_CHAR = "%"
EMPTY_CHAR = " "
P_FOOD = "1"
Q_FOOD = "2"
BOTH_FOOD = "3"


class Pac_map_handler:
    @staticmethod
    def find_in_map(the_map, char):
        for line in the_map:
            if char in line:
                return the_map.index(line), line.index(char)

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

    @staticmethod
    def print_map(pac_map):
        cls()
        print('\n'.join(''.join(item) for item in pac_map))


def cls():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

    clear_output(wait=True)