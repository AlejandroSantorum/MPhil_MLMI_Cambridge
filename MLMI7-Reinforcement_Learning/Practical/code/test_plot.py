import numpy as np
import matplotlib.pyplot as plt

from policy_iteration import policy_iteration
from value_iteration import value_iteration
from sarsa import sarsa
from q_learning import q_learning
from expected_sarsa import expected_sarsa
from model import Model

from world_config import cliff_world, small_world, grid_world


if __name__ == '__main__':
    model = Model(cliff_world)


    # V_pi, pi_pi = policy_iteration(model)
    # V_vi, pi_vi = value_iteration(model)
    V_sarsa, pi_sarsa, cumR_sarsa = sarsa(model)
    V_ql, pi_ql, cumR_ql = q_learning(model)
    #V_es, pi_es, cumR_es = expected_sarsa(model)

    from scipy.ndimage.filters import uniform_filter1d
    y_sarsa = uniform_filter1d(cumR_sarsa, size=200)
    y_ql = uniform_filter1d(cumR_ql, size=200)

    plt.style.use('seaborn')

    plt.plot(range(len(y_sarsa)), y_sarsa, label='sarsa')
    plt.plot(range(len(y_ql)), y_ql, label='ql')
    min_val = min(np.min(y_sarsa), np.min(y_ql))
    plt.ylim(min_val, 0)
    plt.legend()
    plt.show()

    