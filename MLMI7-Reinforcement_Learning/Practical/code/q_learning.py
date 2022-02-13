import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from world_config import cliff_world, small_world, grid_world
from plot_vp import plot_vp
from model import Model, Actions



def q_learning(model: Model, max_epochs: int = 100, maxit: int = 50, alpha: float = 0.2, epsilon: float = 0.1):
    V = np.zeros((model.num_states,))
    pi = np.zeros((model.num_states,))
    Q = np.zeros((model.num_states, len(Actions)))

    def choose_eps_greedily(s):
        rand_n = np.random.rand()

        if rand_n < epsilon:
            rand_idx = np.random.randint(0, len(Actions))
            return Actions(rand_idx)
        
        idx = np.argmax(Q[s])
        return Actions(idx)

    for _ in tqdm(range(max_epochs)):
        # init state
        s = model.start_state

        for _ in range(maxit):
            # choose action eps-greedily
            a = choose_eps_greedily(s)
            # get new state after taking action a
            acts_probs_dict = model._possible_next_states_from_state_action(s, a)
            new_s = np.random.choice(list(acts_probs_dict.keys()), p=list(acts_probs_dict.values()))
            # calculate reward
            r = model.reward(s, a)
            q = np.max(Q[new_s])
            # update Q using SARSA equation
            Q[s][a] = Q[s][a] + alpha*(r + model.gamma*q - Q[s][a])
            # updating state
            s = new_s
            # checking if the new state is terminal
            if s == model.goal_state:
                break
        
        # checking convergence
        V_new = np.amax(Q, axis=1)
        pi_new = np.argmax(Q, axis=1)
        if all(pi_new == pi):
            break
        
        V = V_new
        pi = pi_new

    return V, pi



if __name__ == "__main__":

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

    V, pi = q_learning(model)
    plot_vp(model, V, pi)
    plt.show()