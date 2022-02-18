import numpy as np
import matplotlib.pyplot as plt

from policy_iteration import policy_iteration
from value_iteration import value_iteration
from sarsa import sarsa
from q_learning import q_learning
from expected_sarsa import expected_sarsa
from model import Model

from world_config import cliff_world

from scipy.ndimage.filters import uniform_filter1d


if __name__ == '__main__':
    model = Model(cliff_world)

    V_sarsa, pi_sarsa, cumR_sarsa, _ = sarsa(model, n_episodes=10000, maxit=100, alpha=0.3, decay_eps=True)
    V_ql, pi_ql, cumR_ql, _ = q_learning(model, n_episodes=10000, maxit=100, alpha=0.3, decay_eps=True)

    y_sarsa = uniform_filter1d(cumR_sarsa, size=200)
    y_ql = uniform_filter1d(cumR_ql, size=200)

    #plt.style.use('seaborn')

    plt.plot(range(len(y_sarsa)), y_sarsa, label='SARSA')
    plt.plot(range(len(y_ql)), y_ql, label='Q Learning')
    min_val = max(np.min(y_sarsa), np.min(y_ql))
    plt.ylim(min_val, 0)
    plt.xlabel("Number of episode")
    plt.ylabel("Cumulated reward")
    plt.title("Rewards obtained in each episode")
    plt.legend()
    plt.show()

    