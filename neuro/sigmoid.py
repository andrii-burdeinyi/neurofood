import numpy as np


# done
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))
