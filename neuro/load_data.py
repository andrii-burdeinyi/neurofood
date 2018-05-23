import numpy as np


def load_data_from_csv(filename):
    data = np.genfromtxt(filename, delimiter=",")
    return data

def transform_data(data):
    return np.array(data)