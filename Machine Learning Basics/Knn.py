from Question8 import *
from scipy.spatial import distance
import matplotlib.pyplot as plt
import math

class Knn():

    def __init__(self,k):
        self.k = k
        self.X = None
        self.Y = None

    def fit(self,X,Y):
        self.X = X
        self.Y = Y

    def get_majority(self,X,Y,x):
        distances = []
        response1 = 0
        response0 = 0


        # calculating distance of each sample in test sample from the test sample
        for sample in X:
            dist = distance.euclidean(x,sample)
            distances.append(dist)

        # getting the indices of the original array changed for sort purpose
        sorted_indices = np.argsort(distances)[:k] # getting the first k lowest distances

        # go over the Y label vector according the sorted indices
        for index in sorted_indices:
            if Y[index] == 1:
                response1 += 1
            else :
                response0 += 1
        if response1 >= response0 :
            return 1
        else :
            return 0

    def predict(self,X,Y):
        Y_PREDICT = np.empty((0,1),dtype=float)
        for x in X:
            majority_label = self.get_majority(X,Y,x)
            # determine prediction according to majority count
            Y_PREDICT = np.append(Y_PREDICT,[majority_label])

        return Y_PREDICT

if __name__ == '__main__':
    lr = LR()
    lr.readFile()
    lr.fit()
    error_list = []
    for k in [1,2,5,10,100]:
        error_counter = 0
        knn = Knn(k)
        knn.fit(lr.train_data, lr.train_labels)
        Y_PREDICT = knn.predict(lr.test_data,lr.test_labels)

        # check error rate after prediction
        for index in range(len(lr.test_labels)):
            if Y_PREDICT[index] != lr.test_labels[index] :
                error_counter += 1
        error_list.append(error_counter/len(lr.test_labels))

    plt.plot([1,2,5,10,100],error_list)
    plt.ylabel("error")
    plt.xlabel("K")
    plt.title("Error of KNN model as k grows")
    plt.show()
