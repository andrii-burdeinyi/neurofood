from neuro.load_data import load_data_from_dict
from neuro.learn_neural_network_per_user import learn_neural_network_per_user
from neuro.generate_features import generate_features
import numpy as np
import multiprocessing as mp
from functools import partial


def learn_neural_network(food_features, chances_and_prices, menu_items, orders):
    food_features = load_data_from_dict(food_features)
    chances_and_prices = load_data_from_dict(chances_and_prices)
    menu_items = load_data_from_dict(menu_items)
    orders = load_data_from_dict(orders)

    features = generate_features(food_features, chances_and_prices)

    users = orders[:, 2]
    users = np.unique(users)
    users = users.astype(int)

    learn_partial = partial(closure, features=features, menu_items=menu_items, orders=orders)

    with mp.Pool(mp.cpu_count()) as p:
        p.map(learn_partial, users)

    return True


def closure(user, features, menu_items, orders):
    index_from = np.where(orders[:, 2] == user)[0][0]
    index_to = np.where(orders[:, 2] == user)[0][-1] + 1

    learn_neural_network_per_user(features, menu_items, orders[int(index_from):int(index_to), 0:2], user)

    return
