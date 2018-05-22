import numpy as np
from neuro.normalize_data import normalize_data


def feature_normalize(x):
    m = x.shape[0]
    mu = sum(x)/m
    sigma = np.std(x, axis=0)
    x_norm = normalize_data(x, mu, sigma)
    return x_norm, mu, sigma
