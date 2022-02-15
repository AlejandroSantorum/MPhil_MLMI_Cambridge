from policy_iteration import policy_iteration
from value_iteration import value_iteration
from sarsa import sarsa
from q_learning import q_learning
from expected_sarsa import expected_sarsa
from model import Model

from world_config import cliff_world, small_world, grid_world


if __name__ == '__main__':
    model = Model(small_world)


    V_sarsa, pi_sarsa = sarsa(model)
    V_pi, pi_pi = policy_iteration(model)
    V_vi, pi_vi = value_iteration(model)
    V_ql, pi_ql = q_learning(model)
    V_es, pi_es = expected_sarsa(model)

    