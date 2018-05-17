import numpy as np
from neuro.predict import predict
from neuro.load_data import load_data
from neuro.combine_data import combine_data
from neuro.normalize_data import normalize_data


# done
def predict_order(features_url, new_menu_items_url, user_id):
    features = load_data(features_url)
    new_menu_items = load_data(new_menu_items_url)

    mu, sigma = np.load("neuro/params/" + str(user_id) + "/normalization.npy")
    theta1, theta2 = np.load("neuro/params/" + str(user_id) + "/weights.npy")

    x = normalize_data(combine_data(new_menu_items, features), mu, sigma)

    p = predict(theta1, theta2, x)

    return np.column_stack((new_menu_items[:, 1], p*100))
