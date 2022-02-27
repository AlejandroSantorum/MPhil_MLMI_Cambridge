import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from world_config import cliff_world, small_world, grid_world
from plot_vp import plot_vp
from model import Model, Actions


def sarsa(model: Model, n_episodes: int=1000, maxit: int=100, alpha: float=0.3, epsilon: float=0.1, decay_alpha=False, decay_eps=False):
    V = np.zeros((model.num_states,))
    pi = np.zeros((model.num_states,))
    Q = np.zeros((model.num_states, len(Actions)))
    cum_r = np.zeros((n_episodes,))
    cum_iter = np.zeros((n_episodes,))

    def choose_eps_greedily(s, eps):
        rand_n = np.random.rand()

        if rand_n < eps:
            rand_idx = np.random.randint(0, len(Actions))
            return Actions(rand_idx)
        
        idx = np.argmax(Q[s])
        return Actions(idx)

    for i in tqdm(range(n_episodes), disable=False):
        # init state
        s = model.start_state
        # init action eps-greedily
        a = choose_eps_greedily(s, epsilon) if not decay_eps else choose_eps_greedily(s, 1/(i+1))

        if i > 0:
                cum_iter[i] = cum_iter[i-1]

        for _ in range(maxit):
            cum_iter[i] += 1
            # calculate reward
            r = model.reward(s, a)
            # get new state after taking action a
            acts_probs_dict = model._possible_next_states_from_state_action(s, a)
            new_s = np.random.choice(list(acts_probs_dict.keys()), p=list(acts_probs_dict.values()))
            # get new action eps-greedily
            new_a = choose_eps_greedily(new_s, epsilon) if not decay_eps else choose_eps_greedily(new_s, 1/(i+1))
            # update Q using SARSA equation
            if decay_alpha: alpha = 1/(i+1)
            Q[s][a] = Q[s][a] + alpha*(r + model.gamma*Q[new_s][new_a] - Q[s][a])
            # updating cumulative reward
            cum_r[i] += r
            # updating state and action
            s = new_s
            a = new_a
            # checking if the new state is terminal
            if s == model.goal_state:
                r = model.reward(s, a)
                cum_r[i] += r
                Q[s][a] += alpha*(r - Q[s][a])
                break
    
    V = np.amax(Q, axis=1)
    pi = np.argmax(Q, axis=1)
    return V, pi, cum_r, cum_iter




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
    
    if len(sys.argv) > 2:
        n_episodes = int(sys.argv[2])
        V, pi, _, _ = sarsa(model, n_episodes=n_episodes)
    else:
        V, pi, _, _ = sarsa(model)

    plot_vp(model, V, pi)
    plt.show()