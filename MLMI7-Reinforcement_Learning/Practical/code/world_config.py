# Python code by V Dutordoir (2022). Oringal matlab code from C E Rasmussen,
# who adapted it from earlier work by F Doshi and M P Deisenroth


# ---- Introduction ----
# The model is a gridworld (i.e., checkerboard).  The goal is to travel
# from some (specified) start location to some (specified) final location
# to receive a large reward.  Each action has unit cost, but there may be
# some 'pitfall' locations with large penalties.  The gridbot has four
# control actions: up, down, left, and right.  The execution of these
# actions is noisy, but once completed, the gridbot knows its new state.
from typing import NamedTuple, List


class Cell(NamedTuple):
    """
    Represents a cell in the gridworld. Parameterised using
    a row and col.
    """

    row: int
    col: int


class WorldConfig(NamedTuple):
    """
    Configuration for a world. Contains all the parameters to instantiate a world.
    """

    # set the size of the gridworld (rows and columns) as well as any
    # obstructed and bad cells.
    num_cols: int  # width
    num_rows: int  # height
    start_cell: Cell  # start
    goal_cell: Cell
    obstacle_cells: List[Cell]  # cells that can never be entered
    bad_cells: List[Cell]  # cells for which entering results in a penality

    # set the transition properties of the gridbot: prob_good_trans is the
    # probability that the gridbot does the desired action.  Otherwise, with
    # probability ( 1 - prob_good_trans )*bias, it goes left of the desired action
    # and (1-prob_good_trans)*(1-bias), it goes right of the desired action.
    prob_good_trans: float
    bias: float

    # set the reward parameters: `reward_step` is the cost of an action,
    # `reward_goal` is the reward associated with reaching the goal,
    # and `reward_bad` is the reward for passing through a bad spot.
    reward_step: float
    reward_goal: float
    reward_bad: float  # the same as on Sutton's page
    gamma: float  # discount factor

    # modify the transition model so that any actions taken from the bad states
    # will transition back to the start state. Only used for cliff world.
    return_to_start_from_bad_state: bool = False


# ---- Specific world implementations: ----

cliff_world = WorldConfig(
    num_cols=10,
    num_rows=5,
    start_cell=Cell(4, 0),
    goal_cell=Cell(4, 8),
    obstacle_cells=[
        Cell(0, 9),
        Cell(1, 9),
        Cell(2, 9),
        Cell(3, 9),
        Cell(4, 9),
    ],
    bad_cells=[
        Cell(4, 1),
        Cell(4, 2),
        Cell(4, 3),
        Cell(4, 4),
        Cell(4, 5),
        Cell(4, 6),
        Cell(4, 7),
    ],
    prob_good_trans=1.0,
    bias=0.0,
    reward_step=-1.0,
    reward_goal=10.0,
    reward_bad=-100.0,
    gamma=0.9,
    return_to_start_from_bad_state=True,
)


grid_world = WorldConfig(
    num_cols=12,
    num_rows=9,
    start_cell=Cell(0, 1),
    goal_cell=Cell(7, 8),
    obstacle_cells=[
        Cell(8, 6),
        Cell(7, 6),
        Cell(6, 6),
        Cell(5, 6),
        Cell(4, 6),
        Cell(3, 6),
        Cell(3, 7),
        Cell(3, 8),
        Cell(3, 9),
    ],
    bad_cells=[
        Cell(2, 1),
    ],
    prob_good_trans=0.7,
    bias=0.5,
    reward_step=-1.0,
    reward_goal=10.0,
    reward_bad=-6.0,
    gamma=0.9,
)


small_world = WorldConfig(
    num_cols=4,
    num_rows=4,
    start_cell=Cell(0, 0),
    goal_cell=Cell(3, 3),
    obstacle_cells=[
        Cell(1, 1),
        Cell(2, 1),
        Cell(1, 2),
    ],
    bad_cells=[],
    prob_good_trans=0.8,
    bias=0.5,
    reward_step=-1.0,
    reward_goal=10.0,
    reward_bad=-6,
    gamma=0.9,
)
