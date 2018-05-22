import numpy as np
from neuro.sigmoid import sigmoid
from neuro.sigmoid_gradient import sigmoid_gradient


def neural_network_cost_function(nn_params, input_layer_size, hidden_layer_size, num_labels, x, y, lambda_param):

    theta1 = nn_params[0:hidden_layer_size * (input_layer_size + 1)]\
        .reshape([hidden_layer_size, input_layer_size + 1])
    theta2 = nn_params[hidden_layer_size * (input_layer_size + 1):nn_params.shape[0]]\
        .reshape([num_labels, hidden_layer_size + 1])

    m = x.shape[0]

    a1 = np.c_[np.ones(m), x]
    a2 = sigmoid(a1.dot(theta1.T))
    a2 = np.c_[np.ones(m), a2]
    h = sigmoid(a2.dot(theta2.T))

    j = 1 / m * (-np.asscalar(y.T.dot(np.log(h))) - np.asscalar((1-y).T.dot(np.log(1 - h)))) \
        + lambda_param / (2 * m) \
        * sum(np.concatenate((np.delete(theta1, 0, 1).reshape(-1), np.delete(theta2, 0, 1).reshape(-1)), axis=0) ** 2)

    g_delta_1 = np.zeros(theta1.shape)
    g_delta_2 = np.zeros(theta2.shape)

    for t in range(0,m):
        a_1 = np.insert(x[t], 0, [1]).reshape([x.shape[1]+1,1])
        z_2 = theta1.dot(a_1)
        a_2 = np.insert(sigmoid(z_2), 0, [1]).reshape([z_2.shape[0]+1, 1])
        z_3 = theta2.dot(a_2)
        a_3 = sigmoid(z_3)
        delta_3 = a_3 - y[t]
        delta_2 = np.delete(theta2, 0, 1).T.dot(delta_3) * sigmoid_gradient(z_2)
        g_delta_1 += delta_2.dot(a_1.T)
        g_delta_2 += delta_3.dot(a_2.T)

    theta1_grad = 1 / m * g_delta_1
    theta2_grad = 1 / m * g_delta_2

    theta1_grad[:, 1:theta1_grad.shape[1]] += lambda_param / m * theta1[:, 1:theta1.shape[1]]
    theta2_grad[:, 1:theta2_grad.shape[1]] += lambda_param / m * theta2[:, 1:theta2.shape[1]]

    grad = np.concatenate((theta1_grad.reshape(-1), theta2_grad.reshape(-1)), axis=0)

    return j, grad
