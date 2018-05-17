from urllib.request import urlopen
import numpy as np


# done
def load_data(filename):
    f = urlopen(filename)
    data = np.loadtxt(f, skiprows=1, delimiter=",")
    return data
