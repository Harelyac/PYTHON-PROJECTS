import numpy as np

class perceptron:
    def __init__(self):
        self.w = None

    def fit(self,X,y):
        self.w = np.zeros(X.shape[1])
        while True :
            isChanged = False
            for x_i, y_i in zip(X,y):
                h = y_i * np.dot(self.w, x_i)
                if h <= 0 :
                    self.w = self.w + y_i*x_i
                    isChanged = True
            if not isChanged:
                break

    def predict(self,x):
        y = np.dot(self.w, x)
        if y > 0 :
            return 1
        else :
            return -1



    def score(self,X,Y_correct):
        correct_count = 0
        # Make predict vector using the trained w
        Y_predict = np.empty((0, 1), int)
        for point in X :
            y_predict = self.predict(point)
            Y_predict = np.append(Y_predict, [y_predict])
        # Score it
        for i in range(0,len(Y_correct)):
            if Y_predict[i] == Y_correct[i]:
                correct_count += 1
        return correct_count / len(Y_correct)










