import numpy as np
from neuro.predict import predict
from neuro.combine_data import combine_data
from neuro.normalize_data import normalize_data
from neuro.generate_features import generate_features
from neuro.load_data import load_data_from_dict
from neuro import neuro_train_params_path


def predict_order(food_features, chances_and_price, new_menu_items, user_id):
    food_features = load_data_from_dict(food_features)
    chances_and_price = load_data_from_dict(chances_and_price)
    new_menu_items = load_data_from_dict(new_menu_items)

    features = generate_features(food_features, chances_and_price)

    mu, sigma = np.load(neuro_train_params_path + str(user_id) + "/normalization.npy")
    theta1, theta2 = np.load(neuro_train_params_path + str(user_id) + "/weights.npy")

    x = normalize_data(combine_data(new_menu_items, features), mu, sigma)

    p = predict(theta1, theta2, x)

    return np.column_stack((new_menu_items[:, 0], p*100))
