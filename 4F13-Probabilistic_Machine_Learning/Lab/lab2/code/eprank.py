from scipy.stats import norm
import numpy as np


def eprank(G, M, num_iters):
    """

    :param G: Game outcomes
    :param M: number of players
    :param num_iters: number of iterations of message passing
    :return: mean and precisions for each players skills based on message passing
    """
    # number of games
    N = G.shape[0]

    # prior skill variance (prior mean is always 0)
    pv = 0.5

    # Helper functions
    psi = lambda x: norm.pdf(x)/norm.cdf(x)
    lam = lambda x: psi(x) * (psi(x) + x)

    # intialize marginal means and precisions
    Ms = np.zeros(M)
    Ps = np.zeros(M)

    # initialize matrices of game to skill messages, means and precisions
    Mgs = np.zeros((N, 2))
    Pgs = np.zeros((N, 2))

    # initialize matrices of game to skill to game messages, means and precisions
    Msg = np.zeros((N, 2))
    Psg = np.zeros((N, 2))

    for iter in range(num_iters):
        for p in range(M):  # compute marginal player skills
            games_won = np.where(G[:, 0] == p)[0]
            games_lost = np.where(G[:, 1] == p)[0]
            Ps[p] = 1./pv + np.sum(Pgs[games_won, 0]) + np.sum(Pgs[games_lost, 1])
            Ms[p] = np.sum(Pgs[games_won, 0] * Mgs[games_won, 0]) / Ps[p] \
                + np.sum(Pgs[games_lost, 1] * Mgs[games_lost, 1]) / Ps[p]

        # (2) compute skill to game messages
        Psg = Ps[G] - Pgs
        Msg = (Ps[G] * Ms[G] - Pgs * Mgs) / Psg

        # (3) compute game to performance messages
        vgt = 1 + np.sum(1. / Psg, axis=1)
        mgt = Msg[:, 0] - Msg[:, 1]

        # (4) approximate the marginal on performance differences
        Mt = mgt + np.sqrt(vgt) * psi(mgt / np.sqrt(vgt))
        Pt = 1. / (vgt * (1 - lam(mgt / np.sqrt(vgt))))

        # (5) compute performance to game messages
        ptg = Pt - 1. / vgt
        mtg = (Mt * Pt - mgt / vgt) / ptg

        # (6) compute game to skills messages
        Pgs = 1. / (1 + 1. / ptg[:, None] + 1. / np.flip(Psg, axis=1))
        Mgs = np.stack([mtg, -mtg], axis=1) + np.flip(Msg, axis=1)

    return Ms, Ps
