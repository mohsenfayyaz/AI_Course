from State import State
from queue import Queue
from time import sleep
import copy
from Pac_map_handler import Pac_map_handler

P_CHAR = "P"
Q_CHAR = "Q"
WALL_CHAR = "%"
EMPTY_CHAR = " "
P_FOOD = "1"
Q_FOOD = "2"
BOTH_FOOD = "3"


class IDS:
    def __init__(self, pac_map):
        self.start_state = State(pac_map, None)

        self.all_explored_states_hash = set()
        self.all_explored_states_hash_best_depth = dict()

        self.one_DFS_explored_states_hash = set()
        self.one_DFS_explored_states_hash_best_depth = dict()

        self.unique_states_hash = set()
        self.num_of_explored_states = 0
        self.num_of_unique_explored_states = 0
        self.goal_state = None
        self.goal_state_is_found = False

        self.hash_maps_to_food_number = dict()

    def init_attributes(self):
        self.goal_state_is_found = False
        self.one_DFS_explored_states_hash = set()
        self.one_DFS_explored_states_hash_best_depth = dict()
        # self.unique_states_hash = set()
        # self.num_of_explored_states = 0
        # self.num_of_unique_explored_states = 0

    def count_explored_state(self, state):
        self.num_of_explored_states += 1;
        if state.get_hash() not in self.unique_states_hash:
            self.unique_states_hash.add(state.get_hash())
            self.num_of_unique_explored_states += 1

    def DFS(self, state, max_depth, current_depth=0, explored=list()):
        self.count_explored_state(state)

        if current_depth >= max_depth:
            return False

        if self.are_constraints_satisfied(state):
            self.goal_state_is_found = True
            self.goal_state = state
            return True

        if state.get_hash() in explored:
            return False

        # < COMMENT FOR MEMORY OF the neighbors of a single path through the search tree

        # CAN'T GO TO AN EXPLORED STATE IN THIS DFS LEVEL UNLESS WITH SMALLER DEPTH
        if state.get_hash() in self.one_DFS_explored_states_hash and \
                current_depth >= self.one_DFS_explored_states_hash_best_depth[state.get_hash()]:
            return False

        # CAN'T GO TO AN EXPLORED STATE IN ALL DFS LEVELS UNLESS WITH SMALLER OR EQUAL DEPTH
        if state.get_hash() in self.all_explored_states_hash and \
                current_depth > self.all_explored_states_hash_best_depth[state.get_hash()]:
            return False

        self.all_explored_states_hash.add(state.get_hash())
        self.all_explored_states_hash_best_depth[state.get_hash()] = current_depth
        self.one_DFS_explored_states_hash.add(state.get_hash())
        self.one_DFS_explored_states_hash_best_depth[state.get_hash()] = current_depth

        # COMMENT FOR MEMORY OF the neighbors of a single path through the search tree />

        explored.append(state.get_hash())

        pac_map = state.get_map()
        p_row, p_col = Pac_map_handler.find_in_map(pac_map, P_CHAR)
        q_row, q_col = Pac_map_handler.find_in_map(pac_map, Q_CHAR)

        # P -------
        new_map = Pac_map_handler.move_p_left(copy.deepcopy(pac_map), p_row, p_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        new_map = Pac_map_handler.move_p_down(copy.deepcopy(pac_map), p_row, p_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        new_map = Pac_map_handler.move_p_up(copy.deepcopy(pac_map), p_row, p_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        new_map = Pac_map_handler.move_p_right(copy.deepcopy(pac_map), p_row, p_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        # Q -------------
        new_map = Pac_map_handler.move_q_left(copy.deepcopy(pac_map), q_row, q_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        new_map = Pac_map_handler.move_q_right(copy.deepcopy(pac_map), q_row, q_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        new_map = Pac_map_handler.move_q_up(copy.deepcopy(pac_map), q_row, q_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        new_map = Pac_map_handler.move_q_down(copy.deepcopy(pac_map), q_row, q_col)
        new_state = State(new_map, state)
        if self.DFS(new_state, max_depth, current_depth + 1):
            return True

        explored.pop()
        return False

    def start(self):
        ids_max_depth = 0
        self.all_explored_states_hash = set()
        self.all_explored_states_hash_best_depth = dict()
        self.unique_states_hash = set()
        self.num_of_explored_states = 0
        self.num_of_unique_explored_states = 0
        print("Current IDS Depth:", end=" ");
        while True:
            ids_max_depth += 1
            print(ids_max_depth, end=" ->\n ")
            self.init_attributes()

            self.DFS(self.start_state, ids_max_depth)
            if self.goal_state_is_found:
                return True

        return False

    def print_solution(self, delay=0.2):
        if self.goal_state is None:
            print("No Solution!")
        else:
            current_state = self.goal_state
            states_list = list()
            while current_state is not None:
                states_list.append(current_state)
                current_state = current_state.get_parent()

            for state in reversed(states_list):
                Pac_map_handler.print_map(state.get_map())
                sleep(delay)

            print("Explored States: " + str(self.num_of_explored_states))
            print("Explored Unique States: " + str(self.num_of_unique_explored_states))
            print("Goal Depth: " + str(len(states_list)))

    def are_constraints_satisfied(self, state: State):
        for line in state.get_hash():
            if P_FOOD in line or Q_FOOD in line or BOTH_FOOD in line:
                return False
        return True
