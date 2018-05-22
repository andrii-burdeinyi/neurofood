import numpy as np


def rand_initialize_weights(l_in, l_out):
    epsilon_init = 0.12
    return np.random.random((l_out, 1 + l_in)) * 2 * epsilon_init - epsilon_init
