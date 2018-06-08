import os
import numpy as np
from neuro.combine_data import combine_data
from neuro.gradient_descent import gradient_descent
from neuro.feature_normalize import feature_normalize
from neuro.prepare_target_values import prepare_target_values
from neuro.rand_initialize_weights import rand_initialize_weights
from neuro import neuro_train_params_path


def learn_neural_network_per_user(features, menu_items, orders, user_id):
    x = combine_data(menu_items, features)
    x, mu, sigma = feature_normalize(x)
    y = prepare_target_values(menu_items, orders)

    if not os.path.exists(neuro_train_params_path + str(user_id)):
        os.makedirs(neuro_train_params_path + str(user_id))
    np.save(neuro_train_params_path + str(user_id) + "/normalization", [mu, sigma])


    input_layer_size = features.shape[1] - 1
    hidden_layer_size = 25
    num_labels = 1

    initial_theta1 = rand_initialize_weights(input_layer_size, hidden_layer_size)
    initial_theta2 = rand_initialize_weights(hidden_layer_size, num_labels)
    initial_nn_params = np.concatenate((initial_theta1.reshape(-1), initial_theta2.reshape(-1)), axis=0)

    alpha = os.getenv('ALPHA', 4)
    num_iters = os.getenv('NUM_ITERS', 200)
    lambda_param = os.getenv('LAMBDA_PARAM', 0.5)

    nn_params, j_history = gradient_descent(initial_nn_params, input_layer_size,
                                              hidden_layer_size, num_labels, x, y, float(lambda_param), int(alpha), int(num_iters))

    theta1 = nn_params[0:hidden_layer_size * (input_layer_size + 1)]\
        .reshape([hidden_layer_size, input_layer_size + 1])
    theta2 = nn_params[hidden_layer_size * (input_layer_size + 1):nn_params.shape[0]]\
        .reshape([num_labels, hidden_layer_size + 1])

    np.save(neuro_train_params_path + str(user_id) + "/weights", [theta1, theta2])

    return True
