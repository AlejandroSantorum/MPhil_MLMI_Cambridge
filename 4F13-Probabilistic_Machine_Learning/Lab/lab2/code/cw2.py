import matplotlib.pyplot as plt
import numpy as np


def sorted_barplot(P, W):
    """
    Function for making a sorted bar plot based on values in P, and labelling the plot with the
    corresponding names
    :param P: An array of length num_players (107)
    :param W: Array containing names of each player
    :return: None
    """
    M = len(P)
    xx = np.linspace(0, M, M)
    plt.figure(figsize=(20, 20))
    sorted_indices = np.argsort(P)
    sorted_names = W[sorted_indices]
    plt.barh(xx, P[sorted_indices])
    plt.yticks(np.linspace(0, M, M), labels=sorted_names[:, 0])
    plt.ylim([-2, 109])
    plt.show()

