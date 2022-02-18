from cgitb import small
from typing import Callable
from matplotlib.pyplot import grid
from tqdm import tqdm
import numpy as np
import sys

from model import Model, Actions


def policy_iteration(model: Model, n_episodes: int = 100):

    V = np.zeros((model.num_states,))
    pi = np.zeros((model.num_states,))
    diff_per_episode = []

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

    for i in tqdm(range(n_episodes)):
        for _ in range(5):
            policy_evaluation()
        pi_old = np.copy(pi)
        policy_improvement()
        diffs = sum((pi_old != pi))
        diff_per_episode.append(diffs)
        if all(pi_old == pi):
            break

    return V, pi, np.array(diff_per_episode)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from world_config import cliff_world, small_world, grid_world
    from plot_vp import plot_vp

    if len(sys.argv) > 1:
        if sys.argv[1] == 'cliff':
            model = Model(cliff_world)
        elif sys.argv[1] == 'small':
            model = Model(small_world)
        elif sys.argv[1] == 'grid':
            model = Model(grid_world)
        else:
            print("Error: unknown world type:", sys.argv[1])
    else:
        model = Model(small_world)
    
    if len(sys.argv) > 2:
        n_episodes = int(sys.argv[2])
        V, pi, _ = policy_iteration(model, n_episodes=n_episodes)
    else:
        V, pi, _ = policy_iteration(model)

    plot_vp(model, V, pi)
    plt.show()
