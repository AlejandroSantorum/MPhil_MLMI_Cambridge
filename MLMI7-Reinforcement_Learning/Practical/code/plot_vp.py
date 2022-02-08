import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from model import Actions, Model
from world_config import Cell


def plot_vp(model: Model, value_function: np.array, policy: np.array):
    """
    Plot value function and policy on grid.

    :param value_function: 1D array of size `model.num_states` containing
        real values representing the value function at a given state.

    :param policy: 1D array of size `model.num_states` containing
        an action for each state.
    """
    v = value_function[:-1]  # get rid of final absorbing state

    for cell in model.world.obstacle_cells:
        v[model.cell2state(cell)] = -np.inf

    scale = 1.2
    figsize = (scale * model.world.num_cols, scale * model.world.num_rows)
    fig, (ax, cax) = plt.subplots(
        nrows=2, figsize=figsize, gridspec_kw={"height_ratios": [1, 0.05]}
    )
    cmap = mpl.cm.viridis
    cmap.set_bad("black", 1.0)
    im = ax.matshow(
        v.reshape(model.world.num_rows, model.world.num_cols), cmap=cmap
    )
    fig.colorbar(im, cax=cax, orientation="horizontal")

    for cell, marker in [
        (model.world.start_cell, "s"),
        (model.world.goal_cell, "*"),
    ]:
        ax.scatter(
            cell.col,
            cell.row,
            s=600,
            linewidth=1,
            zorder=3,
            marker=marker,
            facecolor="none",
            edgecolor="r",
        )

    U_LUT = {
        Actions.UP: 0,
        Actions.DOWN: 0,
        Actions.LEFT: -1,
        Actions.RIGHT: 1,
    }

    V_LUT = {
        Actions.UP: 1,
        Actions.DOWN: -1,
        Actions.LEFT: 0,
        Actions.RIGHT: 0,
    }

    cols, rows = np.meshgrid(
        range(model.world.num_cols), range(model.world.num_rows)
    )
    U, V = np.zeros_like(cols), np.zeros_like(rows)
    for r, c in zip(rows.flatten(), cols.flatten()):
        action = policy[model.cell2state(Cell(r, c))]
        U[r, c] = U_LUT[action]
        V[r, c] = V_LUT[action]

    ax.quiver(cols, rows, U, V, pivot="mid")

    return fig, ax
