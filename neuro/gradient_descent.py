import numpy as np
from neuro.neural_network_cost_function import neural_network_cost_function


def gradient_descent(nn_params, input_layer_size, hidden_layer_size, num_labels, x, y, lambda_param, alpha, num_iters):
    j_history = np.zeros(num_iters)

    theta1 = nn_params[0:hidden_layer_size * (input_layer_size + 1)]\
        .reshape([hidden_layer_size, input_layer_size + 1])
    theta2 = nn_params[hidden_layer_size * (input_layer_size + 1):nn_params.shape[0]]\
        .reshape([num_labels, hidden_layer_size + 1])

    for i in range(0, num_iters):
        j, grad = neural_network_cost_function(nn_params, input_layer_size, hidden_layer_size, num_labels,
                                               x, y, lambda_param)

        grad1 = grad[0:theta1.shape[0] * theta1.shape[1]].reshape([theta1.shape[0], theta1.shape[1]])
        grad2 = grad[theta1.shape[0] * theta1.shape[1]:grad.shape[0]].reshape([theta2.shape[0], theta2.shape[1]])

        theta1 = theta1 - alpha * grad1
        theta2 = theta2 - alpha * grad2

        nn_params = np.concatenate((theta1.reshape(-1), theta2.reshape(-1)), axis=0)

        j_history[i] = j

    return nn_params, j_history
