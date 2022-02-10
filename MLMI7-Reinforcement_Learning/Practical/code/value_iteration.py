from typing import Callable
from tqdm import tqdm
import numpy as np

from model import Model, Actions



def value_iteration(model: Model, maxit: int = 100):
    # Initialise values arbitrarily, e.g. V_0(s) = 0 for every s state
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

    def policy_improvement():
        V_new = np.zeros((model.num_states,))
        for s in model.states:
            action_values = [compute_value(s, a, model.reward) for a in Actions]
            action_val = np.max(action_values)
            action_index = np.argmax(action_values)
            V_new[s] = action_val
            pi[s] = Actions(action_index)
        return V_new
    
    for i in tqdm(range(maxit)):
        V_new = policy_improvement()
        if all(V_new == V):
            print("breaking")
            break
        V = V_new

    return V, pi



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
            model = Model(grid_word)
        else:
            print("Error: unknown world type:", sys.argv[1])
    else:
        model = Model(small_world)

    V, pi = value_iteration(model)
    plot_vp(model, V, pi)
    plt.show()