import numpy as np
from scipy.stats import truncnorm
from scipy.special import expit as activation_function


@np.vectorize
def sigmoid(x):
    return 1 / (1 + np.e ** -x)


def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


class NeuralNetwork:

    def __init__(self,
                 no_of_in_nodes,
                 no_of_out_nodes,
                 no_of_hidden_nodes,
                 weights_in_hidden=None,
                 weights_hidden_out=None):
        self.no_of_in_nodes = no_of_in_nodes
        self.no_of_out_nodes = no_of_out_nodes
        self.no_of_hidden_nodes = no_of_hidden_nodes
        self.create_weight_matrices(weights_in_hidden, weights_hidden_out)

    def create_weight_matrices(self, weights_in_hidden, weights_hidden_out):
        if weights_in_hidden is None and weights_hidden_out is None:
            rad = 1 / np.sqrt(self.no_of_in_nodes)
            X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
            self.weights_in_hidden = X.rvs((self.no_of_hidden_nodes,
                                            self.no_of_in_nodes))
            rad = 1 / np.sqrt(self.no_of_hidden_nodes)
            X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
            self.weights_hidden_out = X.rvs((self.no_of_out_nodes,
                                             self.no_of_hidden_nodes))
        else:
            self.weights_in_hidden = weights_in_hidden
            self.weights_hidden_out = weights_hidden_out

    def run(self, input_vector):
        input_vector = np.array(input_vector, ndmin=2).T
        input_hidden = activation_function(self.weights_in_hidden @ input_vector)
        output_vector = activation_function(self.weights_hidden_out @ input_hidden)
        return output_vector
