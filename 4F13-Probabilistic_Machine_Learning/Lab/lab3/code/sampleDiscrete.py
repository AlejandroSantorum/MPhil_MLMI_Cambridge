import numpy as np

def sampleDiscrete(p, ran=None):
    """
    Helper method for sampling from an unnormalized discrete random variable using (generalized) inverse CDF sampling
    :param p: probability mass function over {0,...,num_values-1}
    :return: x \in {0,...,num_values-1} a sample drawn according to p
    """
    normalization_constant = np.sum(p)
    uniform_number = ran or np.random.rand()
    r = uniform_number * normalization_constant
    a = p[0]
    i = 0
    while a < r:
        i += 1
        a += p[i]
    return i