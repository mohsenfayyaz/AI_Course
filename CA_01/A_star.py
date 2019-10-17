from State import State
from queue import Queue
from time import sleep
import copy
from PriorityQueue import PriorityQueue

from Pac_map_handler import Pac_map_handler

P_CHAR = "P"
Q_CHAR = "Q"
WALL_CHAR = "%"
EMPTY_CHAR = " "
P_FOOD = "1"
Q_FOOD = "2"
BOTH_FOOD = "3"


class A_star:
    def __init__(self, pac_map):
        self.start_state = State(pac_map, None)
        self.explored_states_hash = set()
        self.explored_states_hash_best_depth = dict()
        self.unique_states_hash = set()
        self.num_of_explored_states = 0
        self.num_of_unique_explored_states = 0
        self.goal_state = None
        self.goal_state_is_found = False

        self.frontier_states_queue = PriorityQueue()

    def f(self, state):
        return self.g(state) + self.h(state)

    def g(self, state):
        return state.depth

    def h(self, state):
        pac_map = state.get_map()
        p_nearest_1_distance = Pac_map_handler.nearest_distance(pac_map, P_CHAR, P_FOOD)
        q_nearest_2_distance = Pac_map_handler.nearest_distance(pac_map, Q_CHAR, Q_FOOD)
        p_nearest_3_distance = Pac_map_handler.nearest_distance(pac_map, P_CHAR, BOTH_FOOD)
        q_nearest_3_distance = Pac_map_handler.nearest_distance(pac_map, Q_CHAR, BOTH_FOOD)
        if p_nearest_1_distance + q_nearest_2_distance == 0:
            return min(p_nearest_3_distance, q_nearest_3_distance)
        else:
            return p_nearest_1_distance + q_nearest_2_distance

    def count_explored_state(self, state):
        self.num_of_explored_states += 1;
        if state.get_hash() not in self.unique_states_hash:
            self.unique_states_hash.add(state.get_hash())
            self.num_of_unique_explored_states += 1

    def start(self):
        self.goal_state_is_found = False
        self.frontier_states_queue = PriorityQueue()
        self.frontier_states_queue.push(self.start_state, self.f(self.start_state))
        self.explored_states_hash = set()
        self.explored_states_hash_best_depth = dict()
        self.unique_states_hash = set()
        self.num_of_explored_states = 0
        self.num_of_unique_explored_states = 0

        while not self.frontier_states_queue.empty():
            current_state = self.frontier_states_queue.pop()
            self.count_explored_state(current_state)

            if current_state.get_hash() in self.explored_states_hash and\
                    current_state.depth >= self.explored_states_hash_best_depth[current_state.get_hash()]:
                continue
            else:
                self.explored_states_hash.add(current_state.get_hash())
                self.explored_states_hash_best_depth[current_state.get_hash()] = current_state.depth

            # Pac_map_handler.print_map(current_state.get_map())
            if self.are_constraints_satisfied(current_state):
                self.goal_state = current_state
                self.goal_state_is_found = True
                return True

            self.do_actions(current_state)
            self.explored_states_hash.add(current_state.get_hash())

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
        for line in state.get_map():
            if P_FOOD in line or Q_FOOD in line or BOTH_FOOD in line:
                return False
        return True

    def do_actions(self, current_state):
        pac_map = current_state.get_map()
        p_row, p_col = Pac_map_handler.find_in_map(pac_map, P_CHAR)
        q_row, q_col = Pac_map_handler.find_in_map(pac_map, Q_CHAR)
        # P MOVEMENT
        self.move_p(current_state, pac_map, p_row, p_col)
        # Q MOVEMENT
        self.move_q(current_state, pac_map, q_row, q_col)

    def move_p(self, current_state, pac_map, row, col):
        new_map = Pac_map_handler.move_p_up(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

        new_map = Pac_map_handler.move_p_left(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

        new_map = Pac_map_handler.move_p_down(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

        new_map = Pac_map_handler.move_p_right(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

    def move_q(self, current_state, pac_map, row, col):
        new_map = Pac_map_handler.move_q_up(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

        new_map = Pac_map_handler.move_q_left(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

        new_map = Pac_map_handler.move_q_down(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

        new_map = Pac_map_handler.move_q_right(copy.deepcopy(pac_map), row, col)
        self.add_to_frontier(new_map, current_state)

    def add_to_frontier(self, new_map, current_state):
        new_state = State(new_map, current_state)
        if not new_state.get_hash() in self.explored_states_hash:
            self.frontier_states_queue.push(new_state, self.f(new_state))
