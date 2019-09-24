"""
===================================================
     Introduction to Machine Learning (67577)
===================================================

Skeleton for the AdaBoost classifier.

Author: Gad Zalcberg
Date: February, 2019

"""
import numpy as np
import math

class AdaBoost(object):

    def __init__(self, WL, T):
        """
        Parameters
        ----------
        WL : the class of the base weak learner
        T : the number of base learners to learn
        """
        self.WL = WL
        self.T = T
        self.h = [None]*T     # list of base learners
        self.w = np.zeros(T)  # weights

    def train(self, X, y):
        """
        Parameters
        ----------
        X : samples, shape=(num_samples, num_features)
        y : labels, shape=(num_samples)
        Train this classifier over the sample (X,y)
        After finish the training return the weights of the samples in the last iteration.
        """
        m = X.shape[0]
        D_t = np.full((1, m), 1 / m, dtype=float)
        D_t = D_t.reshape((m,))
        for t in range(self.T):
            self.h[t] = self.WL(D_t, X, y)
            predictions = self.h[t].predict(X)
            epsilon_t = [D_t[i] * (y[i] != predictions[i]) for i in range(m)]
            epsilon_t = np.sum(epsilon_t)
            self.w[t] = 0.5 * math.log((1 / epsilon_t) - 1)
            new_D_vals = [D_t[i] * math.exp(-self.w[t] * y[i] * predictions[i])
                          for i in range(m)]
            denominator = np.sum(new_D_vals)
            D_t = np.array([new_D_vals[i] / denominator for i in range(m)]).reshape((m,))

    def predict(self, X, max_t):
        """
        Parameters
        ----------
        X : samples, shape=(num_samples, num_features)
        :param max_t: integer < self.T: the number of classifiers to use for the classification
        :return: y_hat : a prediction vector for X. shape=(num_samples)
        Predict only with max_t weak learners,
        """
        y_hat = 0
        for t in range(max_t):
            y_hat += self.w[t] * self.h[t].predict(X)
        return np.sign(y_hat).astype(int)

    def error(self, X, y, max_t):
        """
        Parameters
        ----------
        X : samples, shape=(num_samples, num_features)
        y : labels, shape=(num_samples)
        :param max_t: integer < self.T: the number of classifiers to use for the classification
        :return: error : the ratio of the wrong predictions when predict only with max_t weak learners (float)
        """
        return (self.predict(X, max_t) !=y).sum() / X.shape[0]

