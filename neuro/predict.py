import numpy as np
from neuro.sigmoid import sigmoid


def predict(theta1, theta2, x):
    m = x.shape[0]
    a2 = sigmoid(np.c_[np.ones(m), x].dot(theta1.T))
    p = sigmoid(np.c_[np.ones(m), a2].dot(theta2.T))
    return p
