# Python code by V Dutordoir (2022). Oringal matlab code from C E Rasmussen,
# who adapted it from earlier work by F Doshi and M P Deisenroth
import numpy as np


from typing import List, TypeVar
from collections import defaultdict
from enum import IntEnum


from world_config import WorldConfig, Cell


State = TypeVar("State", bound=int)
"""
Type for state (0..num_states-1) that behaves like an integer.
It can be used for indexing arrays, for example.
"""


class Actions(IntEnum):
    """
    For your convenience, you can use the following variables instead of
    having to use the indices for each action:
    """

    UP: int = 0
    DOWN: int = 1
    LEFT: int = 2
    RIGHT: int = 3


class Model:
    """
    Creates a model based on the parameters.  Each cell is a state, numbered
    from 0...num_states-1 across rows and then down columns.  Obstructed states are
    treated as states that can never be entered. For computational
    convenience, the obstructed states and goal state transition to a
    fictional absorbing end state.
    """

    def __init__(self, world: WorldConfig):
        self.world = world
        self.gamma = world.gamma  # quick access to discount factor
        self.start_state = self.cell2state(world.start_cell)
        self.goal_state = self.cell2state(world.goal_cell)

        # Number of states, including the fictional end state
        self.num_states = world.num_cols * world.num_rows + 1

        self.fictional_end_state = self.num_states - 1

        self.bad_states = [self.cell2state(cell) for cell in world.bad_cells]
        self.obstacle_states = [
            self.cell2state(cell) for cell in world.obstacle_cells
        ]

    @property
    def states(self) -> List[State]:
        """Returns list with state integers [0, 1, ..., num_states-1]"""
        return [s for s in range(self.num_states)]

    def cell2state(self, cell: Cell) -> State:
        """From cell(row, col) to state index"""
        value = cell.row * self.world.num_cols + cell.col
        return value

    def state2cell(self, state: State) -> Cell:
        """Reverse from cell2state"""
        row = state // self.world.num_cols
        col = state % self.world.num_cols
        return Cell(row, col)

    def reward(self, s: State, a: Actions) -> float:
        """
        Reward for performing action `a` in state `s`.
        """
        if s == self.goal_state:
            # return `reward_goal` independently of the action
            return self.world.reward_goal
        elif s == self.fictional_end_state:
            # arrived at fictional end state, return 0 independently of the action
            return 0
        elif s in self.bad_states:
            # arrived at one of the bad states, return `reward_bad` independently of the action
            return self.world.reward_bad
        else:
            # otherwise we simply made a valid step, and return the reward for this
            return self.world.reward_step

    def transition_probability(self, s1: State, s2: State, a: Actions) -> float:
        """
        Transition probability from state `s1` to `s2` given action `a`.
        """
        if s1 == self.fictional_end_state and s2 == self.fictional_end_state:
            # self transition for fictional end state independently of the action
            return 1.0
        elif s1 == self.fictional_end_state and s2 != self.fictional_end_state:
            # impossible to escape from fictional end state
            return 0.0

        if s1 in self.obstacle_states or s1 == self.goal_state:
            # check if s is a goal or an obstructed state - transition to end
            if s2 == self.fictional_end_state:
                # certain transition from obstacle or goal state to fictional end state
                return 1.0
            else:
                return 0.0

        # Any actions taken from the bad "cliff" states will transition back to the start state.
        # We only do this for the cliff world, where `return_to_start_from_bad_state` is set
        # to True.
        if s1 in self.bad_states and self.world.return_to_start_from_bad_state:
            if s2 == self.start_state:
                return 1.0
            else:
                return 0.0

        next_states = self._possible_next_states_from_state_action(s1, a)
        # if s2 is one of the possible next states, return the probability of this
        # happening, else return 0.0 (i.e. zero probability of reaching s2 from s1 using action a).
        return next_states.get(s2, 0.0)

    def _possible_next_states_from_state_action(self, s: State, a: Actions):
        """
        Returns the possible next states (with their probability) that can occur when
        executing action `a` in state `s`.
        """
        LEFT_LUT = {
            Actions.UP: Actions.LEFT,
            Actions.DOWN: Actions.RIGHT,
            Actions.LEFT: Actions.DOWN,
            Actions.RIGHT: Actions.UP,
        }
        RIGHT_LUT = {
            Actions.UP: Actions.RIGHT,
            Actions.DOWN: Actions.LEFT,
            Actions.LEFT: Actions.UP,
            Actions.RIGHT: Actions.DOWN,
        }
        # look up table
        cell = self.state2cell(s)

        result = defaultdict(lambda: 0)

        # intended action
        next_cell = self._result_action(cell, a)
        result[self.cell2state(next_cell)] += self.world.prob_good_trans

        # bias to left
        next_cell = self._result_action(cell, LEFT_LUT[a])
        prob_bad_trans = 1.0 - self.world.prob_good_trans
        result[self.cell2state(next_cell)] += prob_bad_trans * self.world.bias

        # bias to right
        next_cell = self._result_action(cell, RIGHT_LUT[a])
        result[self.cell2state(next_cell)] += prob_bad_trans * (
            1.0 - self.world.bias
        )

        return result

    def _result_action(self, cell: Cell, action: Actions) -> Cell:
        """
        Performs an action (UP, DOWN, etc.) to a cell. If the action
        leads to an unvalid cell (i.e. a cell outside of the domain of the grid)
        the current cell is returned.
        """

        if action == Actions.UP:
            next_cell = Cell(cell.row - 1, cell.col)
        elif action == Actions.DOWN:
            next_cell = Cell(cell.row + 1, cell.col)
        elif action == Actions.LEFT:
            next_cell = Cell(cell.row, cell.col - 1)
        elif action == Actions.RIGHT:
            next_cell = Cell(cell.row, cell.col + 1)
        else:
            raise Exception("Unknown action")

        if not self._can_player_enter(next_cell):
            next_cell = cell

        return next_cell

    def _can_player_enter(self, cell: Cell) -> bool:
        """
        Determines whether the cell can be entered. Only True if cell is
        inside the boundary of the world and not on an obstance.
        """
        inside_boundary = (cell.row in range(self.world.num_rows)) and (
            cell.col in range(self.world.num_cols)
        )
        on_obstacle = cell in self.world.obstacle_cells
        return inside_boundary and not on_obstacle
