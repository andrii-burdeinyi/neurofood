import numpy as np


def generate_features(food_features, chance_and_price):
    food_count = np.unique(food_features[:, 0:1]).shape[0]
    addition_features_count = chance_and_price.shape[1] - 1
    features_count = addition_features_count + np.unique(food_features[:, 1:2]).shape[0]

    features = np.zeros([food_count, features_count])
    features[:, 0:addition_features_count] = chance_and_price[:, 1:addition_features_count + 1]

    for i in food_features:
        features[int(i[0]) - 1][int(i[1]) + 1] = 1

    return features
