import numpy as np


def normalize_data(x, mu, sigma):
    x_norm = np.zeros(x.shape)
    for i in range(0, x_norm.shape[1]):
        x_norm[:, i] = (x[:, i] - mu[i]) / sigma[i]
    return x_norm
