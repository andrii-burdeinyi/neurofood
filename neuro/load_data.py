import numpy as np


def load_data_from_csv(filename):
    data = np.genfromtxt(filename, delimiter=",")
    return data


def load_data_from_dict(dict_data):
    data = []
    for item in dict_data:
        data.append(list(item.values()))

    return transform_data(data)


def transform_data(data):
    return np.array(data)
