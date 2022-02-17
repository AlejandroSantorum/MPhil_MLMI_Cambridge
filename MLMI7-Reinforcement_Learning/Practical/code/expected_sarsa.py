from re import A
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from world_config import cliff_world, small_world, grid_world
from plot_vp import plot_vp
from model import Model, Actions



def expected_sarsa(model: Model, n_episodes: int = 5000, maxit: int = 200, alpha: float = 0.2, epsilon: float = 0.1):
    '''
        References for some code:
        https://medium.com/analytics-vidhya/q-learning-expected-sarsa-and-comparison-of-td-learning-algorithms-e4612064de97
    '''
    V = np.zeros((model.num_states,))
    pi = np.zeros((model.num_states,))
    Q = np.zeros((model.num_states, len(Actions)))
    cum_r = np.zeros((n_episodes,))


    def choose_eps_greedily(s):
        rand_n = np.random.rand()

        if rand_n < epsilon:
            rand_idx = np.random.randint(0, len(Actions))
            return Actions(rand_idx)
        
        idx = np.argmax(Q[s])
        return Actions(idx)

    
    def greedy_action_selection(s):
        max_q = max(Q[s])
        # there might be cases where there are multiple actions with the same high q_value.
        # Choose randomly then
        count_max_q = np.count_nonzero(Q[s] == max_q)
        if count_max_q > 1:
            # get all the actions with the maxQ
            best_action_indexes = [i for i in range(len(Actions)) if Q[s][i] == max_q]
            action_index = np.random.choice(best_action_indexes)
        else:
            action_index = np.where(Q[s] == max_q)[0]
            
        return Actions(action_index)


    def action_probs(s):
        next_state_probs = [epsilon/len(Actions)] * len(Actions)
        best_action = greedy_action_selection(s)
        next_state_probs[best_action] += (1.0 - epsilon)
        return next_state_probs


    for i in tqdm(range(n_episodes)):
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
            # calculate expected value of the action-value function
            next_state_probs = action_probs(new_s)
            expected_q = sum([a*b for a, b in zip(next_state_probs, Q[new_s])])
            # update Q using SARSA equation
            Q[s][a] = Q[s][a] + alpha*(r + model.gamma*expected_q - Q[s][a])
            # updating state
            s = new_s
            # updating cumulative reward
            cum_r[i] += model.gamma*model.reward(s, a)
            # checking if the new state is terminal
            if s == model.goal_state:
                r = model.reward(s, a)
                Q[s][a] += alpha*(r - Q[s][a])
                break
        
    V = np.amax(Q, axis=1)
    pi = np.argmax(Q, axis=1)
    return V, pi, cum_r



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
        V, pi, _ = expected_sarsa(model, n_episodes=n_episodes)
    else:
        V, pi, _ = expected_sarsa(model)

    plot_vp(model, V, pi)
    plt.show()