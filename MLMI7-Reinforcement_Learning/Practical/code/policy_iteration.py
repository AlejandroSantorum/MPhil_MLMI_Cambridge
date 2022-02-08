from cgitb import small
from typing import Callable
from matplotlib.pyplot import grid
from tqdm import tqdm
import numpy as np

from model import Model, Actions


def policy_iteration(model: Model, maxit: int = 100):

    V = np.zeros((model.num_states,))
    pi = np.zeros((model.num_states,))

    def compute_value(s, a, reward: Callable):
        return np.sum(
            [
                model.transition_probability(s, s_, a)
                * (reward(s, a) + model.gamma * V[s_])
                for s_ in model.states
            ]
        )

    def policy_evaluation():
        for s in model.states:
            R = model.reward(s, pi[s])
            V[s] = compute_value(s, pi[s], lambda *_: R)

    def policy_improvement():
        for s in model.states:
            action_index = np.argmax(
                [compute_value(s, a, model.reward) for a in Actions]
            )
            pi[s] = Actions(action_index)

    for i in tqdm(range(maxit)):
        for _ in range(5):
            policy_evaluation()
        pi_old = np.copy(pi)
        policy_improvement()
        if all(pi_old == pi):
            print("breaking")
            break

    return V, pi


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from world_config import cliff_world, small_world, grid_world
    from plot_vp import plot_vp

    model = Model(cliff_world)
    V, pi = policy_iteration(model)
    plot_vp(model, V, pi)
    plt.show()
