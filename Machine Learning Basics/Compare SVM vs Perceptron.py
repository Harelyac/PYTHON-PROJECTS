import numpy as np
from perceptron import *
from sklearn.svm import SVC
import matplotlib.pyplot as plt


def Draw_random_ractangle(correct_y):
    if correct_y == 1:
        x = np.random.uniform(-3,1)
        y = np.random.uniform(1,3)
    else:
        correct_y = -1
        x = np.random.uniform(-1, 3)
        y = np.random.uniform(-3, -1)
    return x,y

# Draw training/test points from D1 and D2
# Return - matrix load with sample and y vector of true classification

def Draw_points_from_D1(w,size):
    X_D1 = np.random.multivariate_normal(np.zeros(2, dtype=int),np.identity(2, dtype=int),size)
    Y_D1 = np.sign(np.dot(X_D1,w))
    return X_D1,Y_D1


def Draw_points_from_D2(size):
    X_D2 = np.empty((0, 2), int)
    Y_D2 = np.array(np.random.choice([1,-1], size=size))
    for point in range(size):
        x,y = Draw_random_ractangle(Y_D2[point])
        X_D2 = np.append(X_D2, np.array([[x, y]]), axis=0)
    return X_D2,Y_D2


# Main function
if __name__ == '__main__':
    NUMBER_TEST_POINTS = 10000
    ROUNDS = 500
    sample_sizes = [5,10,15,25,70]
    w = [0.3,-0.5]

    array_svm_mean_D1_accuracy = []
    array_svm_mean_D2_accuracy = []
    array_percp_mean_D1_accuracy = []
    array_percp_mean_D2_accuracy = []

    percp_D1 = perceptron()
    svm_D1 = SVC(C=1e10,kernel= 'linear')
    percp_D2 = perceptron()
    svm_D2 = SVC(C=1e10, kernel='linear')

    for sample_complexity in sample_sizes:
        svm_sum_D1_accuracy = 0
        svm_sum_D2_accuracy = 0
        percp_sum_D1_accuracy = 0
        percp_sum_D2_accuracy = 0
        for iteration in range(ROUNDS):
            # Draw points from both distributions
            X_D1_train,Y_D1_train_correct = Draw_points_from_D1(w,sample_complexity)
            while len(np.unique(Y_D1_train_correct)) < 2:
                X_D1_train, Y_D1_train_correct = Draw_points_from_D1(w,sample_complexity)
            X_D2_train, Y_D2_train_correct = Draw_points_from_D2(sample_complexity)
            while len(np.unique(Y_D2_train_correct)) < 2:
                X_D2_train, Y_D2_train_correct = Draw_points_from_D2(sample_complexity)


            # Train percp and svm on both distributions
            svm_D1.fit(X_D1_train, Y_D1_train_correct)
            svm_D2.fit(X_D2_train, Y_D2_train_correct)
            percp_D1.fit(X_D1_train, Y_D1_train_correct)
            percp_D2.fit(X_D2_train, Y_D2_train_correct)


            # Draw test points from both distribution
            X_D1_test, Y_D1_test_correct = Draw_points_from_D1(w,NUMBER_TEST_POINTS)
            X_D2_test, Y_D2_test_correct = Draw_points_from_D2(NUMBER_TEST_POINTS)

            # predict and get score on each distribution on both learnning models/algorithems - svm & perceptron
            svm_sum_D1_accuracy += svm_D1.score(X_D1_test, Y_D1_test_correct)
            svm_sum_D2_accuracy += svm_D2.score(X_D2_test, Y_D2_test_correct)
            print(svm_D2.score(X_D2_test, Y_D2_test_correct))
            percp_sum_D1_accuracy += percp_D1.score(X_D1_test, Y_D1_test_correct)
            percp_sum_D2_accuracy += percp_D2.score(X_D2_test, Y_D2_test_correct)
            print(percp_D2.score(X_D2_test, Y_D2_test_correct))

        array_svm_mean_D1_accuracy.append(svm_sum_D1_accuracy / ROUNDS)
        array_svm_mean_D2_accuracy.append(svm_sum_D2_accuracy / ROUNDS)
        array_percp_mean_D1_accuracy.append(percp_sum_D1_accuracy / ROUNDS)
        array_percp_mean_D2_accuracy.append(percp_sum_D2_accuracy / ROUNDS)


    plt.plot(sample_sizes, array_svm_mean_D2_accuracy, label="SVM")
    plt.plot(sample_sizes, array_percp_mean_D2_accuracy, label="PERCEPTRON")
    plt.xlabel("Sample Size")
    plt.ylabel("Mean Accuracy")
    plt.title("Mean Accuracy of SVM and Perceptron vs number of Samples - D2")
    plt.legend()
    plt.show()

    plt.plot(sample_sizes, array_svm_mean_D1_accuracy, label="SVM")
    plt.plot(sample_sizes, array_percp_mean_D1_accuracy, label="PERCEPTRON")
    plt.xlabel("Sample Size")
    plt.ylabel("Mean Accuracy")
    plt.title("Mean Accuracy of SVM and Perceptron vs number of Samples - D1")
    plt.legend()
    plt.show()