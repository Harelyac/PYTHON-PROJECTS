import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

class LR :
    TEST_N = 1000
    def __init__(self):
        self.lr = LogisticRegression()
        self.test_data = []
        self.test_labels = []
        self.train_data = []
        self.train_labels = []

    def readFile(self):
        # Reading the dataframe
        with open("spam.data.txt", "r") as file :
            data = file.read()
            raw_data = data.split("\n")[:-1] # removing eof
            np.random.shuffle(raw_data)

            # Dividing the data into train and set partitions
            test_raw = raw_data[:LR.TEST_N]
            train_raw = raw_data[LR.TEST_N:]


            # Dividing each partition into data and label
            for sample in test_raw :
                self.test_data.append(list(map(float,sample[:-1].split())))
                self.test_labels.append(float(sample[-1]))
            for sample in train_raw :
                self.train_data.append(list(map(float,sample[:-1].split())))
                self.train_labels.append(float(sample[-1]))

    def retrieve_tpr_and_ftr(self, sorted_test_labels):
        NP = np.count_nonzero(sorted_test_labels)
        NN = LR.TEST_N - NP
        TPR_list = np.append([0], np.arange(NP + 1) / NP)  # TPR LIST adding zero for (0.0)
        FPR_list = [0]

        for tp_count in range(1, NP + 1):
            Ni = np.where(sorted_test_labels.cumsum() == tp_count)[0][0] + 1
            # definition :
            # we take the sorted_test_labels and do make cumulative array out of it. then make true/false
            # array corresponds to tp_count then we retrieve the first true value from all true value - notation [0][0]
            # we add one because we start counting from zero
            fp_count = Ni - tp_count
            FPR_list.append(fp_count / NN)
        FPR_list.append(1) # adds 1 to end of fpr as we did earlier on tpr
        return TPR_list, FPR_list
        # NP - number of positives
        # N_i - number of samples the classifier need to tag with label equal 1
        # (false-positive with true-positive) in order to get TPR - (true postiive rate) of i/NP(true positive).
        # FPR - (N_i - i)/NN where NN is negative number. observe that (N_i - i) is the false positive.

    def fit(self):
        # Turning into ndarray
        self.test_data = np.array(self.test_data)
        self.test_labels = np.array(self.test_labels)
        self.train_data = np.array(self.train_data)
        self.train_labels = np.array(self.train_labels)
        self.lr.fit(self.train_data,self.train_labels)



if __name__ == '__main__':
    lr = LR()
    lr.readFile()
    lr.fit()
    unsorted = lr.lr.predict_proba(lr.test_data)
    sorted_indexes = np.argsort(unsorted.T[1])[::-1]
    sorted_test_labels = lr.test_labels[sorted_indexes]
    TPR_list, FPR_list = lr.retrieve_tpr_and_ftr(sorted_test_labels)
    plt.plot(FPR_list,TPR_list)
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("Empirical roc curve")
    plt.show()