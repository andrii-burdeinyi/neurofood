import numpy as np


def combine_data(menu_items, features):
    m = menu_items.shape[0]
    n = features.shape[1]-1
    x = np.zeros([m, n])
    for i in range(0, m):
        x[i, :] = features[int(menu_items[i, 1])-1, 1:]
    return x
