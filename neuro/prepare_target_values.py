import numpy as np


def prepare_target_values(menu_items, orders):
    m = menu_items.shape[0]
    y = np.zeros(m)
    for i in range(0, orders.shape[0]):
        index = np.where(menu_items[:, 0] == orders[i, 0])
        y[index] = 1
    return y
