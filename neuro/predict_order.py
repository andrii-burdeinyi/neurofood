import numpy as np
from neuro.predict import predict
from neuro.combine_data import combine_data
from neuro.normalize_data import normalize_data
from neuro.generate_features import generate_features


def predict_order(food_feature_url, chance_and_price_url, new_menu_items, user_id):
    features = generate_features(food_feature_url, chance_and_price_url)

    mu, sigma = np.load("neuro/params/" + str(user_id) + "/normalization.npy")
    theta1, theta2 = np.load("neuro/params/" + str(user_id) + "/weights.npy")

    x = normalize_data(combine_data(new_menu_items, features), mu, sigma)

    p = predict(theta1, theta2, x)

    return np.column_stack((new_menu_items[:, 0], p*100))
