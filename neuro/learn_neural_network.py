import os
import numpy as np
from neuro.load_data import load_data
from neuro.combine_data import combine_data
from neuro.gradient_descent import gradient_descent
from neuro.generate_features import generate_features
from neuro.feature_normalize import feature_normalize
from neuro.prepare_target_values import prepare_target_values
from neuro.rand_initialize_weights import rand_initialize_weights


def learn_neural_network(food_feature_url, chance_and_price_url, menu_items_url, orders_url, user_id):
    orders = load_data(orders_url)
    menu_items = load_data(menu_items_url)
    features = generate_features(food_feature_url, chance_and_price_url)

    x = combine_data(menu_items, features)
    x, mu, sigma = feature_normalize(x)
    y = prepare_target_values(menu_items, orders)

    if not os.path.exists("neuro/params/" + str(user_id)):
        os.makedirs("neuro/params/" + str(user_id))
    np.save("neuro/params/" + str(user_id) + "/normalization", [mu, sigma])

    input_layer_size = 74
    hidden_layer_size = 25
    num_labels = 1

    initial_theta1 = rand_initialize_weights(input_layer_size, hidden_layer_size)
    initial_theta2 = rand_initialize_weights(hidden_layer_size, num_labels)
    initial_nn_params = np.concatenate((initial_theta1.reshape(-1), initial_theta2.reshape(-1)), axis=0)

    alpha = 4
    num_iters = 200
    lambda_param = 0.5

    nn_params, j_history = gradient_descent(initial_nn_params, input_layer_size,
                                              hidden_layer_size, num_labels, x, y, lambda_param, alpha, num_iters)

    theta1 = nn_params[0:hidden_layer_size * (input_layer_size + 1)]\
        .reshape([hidden_layer_size, input_layer_size + 1])
    theta2 = nn_params[hidden_layer_size * (input_layer_size + 1):nn_params.shape[0]]\
        .reshape([num_labels, hidden_layer_size + 1])

    np.save("neuro/params/" + str(user_id) + "/weights", [theta1, theta2])

    return True
