from neuro.sigmoid import sigmoid


# done
def sigmoid_gradient(z):
    return sigmoid(z)*(1 - sigmoid(z))
