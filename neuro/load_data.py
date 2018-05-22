import numpy as np


def load_data(filename):
    data = np.genfromtxt(filename, delimiter=",")
    return data
