import scipy.linalg
import numpy as np
from tqdm import tqdm


def gibbs_sample(G, M, num_iters):
    # number of games
    N = G.shape[0]
    # Array containing mean skills of each player, set to prior mean
    w = np.zeros((M, 1))
    # Array that will contain skill samples
    skill_samples = np.zeros((M, num_iters))
    # Array containing skill variance for each player, set to prior variance
    pv = 0.5 * np.ones(M)
    # number of iterations of Gibbs
    for i in tqdm(range(num_iters)):
        # sample performance given differences in skills and outcomes
        t = np.zeros((N, 1))
        for g in range(N):

            s = w[G[g, 0]] - w[G[g, 1]]  # difference in skills
            t[g] = s + np.random.randn()  # Sample performance
            while t[g] < 0:  # rejection step
                t[g] = s + np.random.randn()  # resample if rejected

        # Jointly sample skills given performance differences
        m = np.zeros((M, 1))
        for p in range(M):
            m[p] =  # TODO: COMPLETE THIS LINE
        iS = np.zeros((M, M))  # Container for sum of precision matrices (likelihood terms)

        for g in range(N):
            # TODO: Build the iS matrix

        # Posterior precision matrix
        iSS = iS + np.diag(1. / pv)

        # Use Cholesky decomposition to sample from a multivariate Gaussian
        iR = scipy.linalg.cho_factor(iSS)  # Cholesky decomposition of the posterior precision matrix
        mu = scipy.linalg.cho_solve(iR, m, check_finite=False)  # uses cholesky factor to compute inv(iSS) @ m

        # sample from N(mu, inv(iSS))
        w = mu + scipy.linalg.solve_triangular(iR[0], np.random.randn(M, 1), check_finite=False)
        skill_samples[:, i] = w[:, 0]
    return skill_samples


