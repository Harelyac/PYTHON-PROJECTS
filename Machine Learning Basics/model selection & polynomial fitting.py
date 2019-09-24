import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import math
import scipy.stats as stat
from scipy.stats import norm
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
data_X = np.random.uniform(-3.2,2.2, 1500)
epsilon = np.random.normal(0,1)
X_Y = []

for x in data_X:
    f_x = (x+3)*(x+2)*(x+1)*(x-1)*(x-2)
    y = f_x+epsilon  #add noise
    X_Y.append((x,y))
D = np.array(X_Y[:1000]) #for train and validation
T = X_Y[1000:] #for test
S = D[:500] #train only
V = D[500:] #validation onlt

# print("XY", X_Y)
H = []
D_X, D_Y = D.T


# for sample in S:
#     trainSet_X.append(sample[0])
#     trainSet_Y.append(sample[1])



# train on each model / hypothesis class and retrieve its unique prediction
# for d in range(1,16):
#     # print(d, S[0])
#     h_d = np.poly1d(np.polyfit(trainSet_X, trainSet_Y, d))
#     H.append(h_d)
# print("H", H[5])

errors = []
ValidationSet_X = []
ValidationSet_Y = []

# for sample in V:
#     ValidationSet_X.append(sample[0])
#     ValidationSet_Y.append(sample[1])

# search for best hypothesis
# best_h = H[0]
# min_error = np.square(ValidationSet_Y - H[0](ValidationSet_X)).sum()
#
# for h_d in H:
#     error = np.square(ValidationSet_Y - h_d(ValidationSet_X)).sum()
#     errors.append(error)
#     if(error < min_error):
#         min_error = error
#         best_h = h_d
# errors.sort()

# perform actual k - cross validation with k = 5
train_errors = []
validation_errors = []
avg_train_errors = []
avg_validation_errors = []

# seperate D into 5 folds
kf = KFold(5)
kf.get_n_splits(D)

# start the k - cross validation algo on the D data set
for d in np.arange(1,16):
    for train_index, valid_index in kf.split(D):

        # train the model
        h_d = np.poly1d(np.polyfit(D_X[train_index], D_Y[train_index], d, 1e-20))
        H.append(h_d)
        # calculate train error
        error_t = np.sum(((D_Y[train_index] - h_d(D_X[train_index])) ** 2) / len(D_Y[train_index]))
        train_errors.append(error_t)

        # calculate validation error
        error_v = np.sum(((D_Y[valid_index] - h_d(D_X[valid_index])) ** 2) / len(D_Y[valid_index]))
        validation_errors.append(error_v)

    avg_train_errors.append(sum(train_errors)/len(train_errors))
    avg_validation_errors.append(sum(validation_errors)/len(validation_errors))

plt.plot(range(1,16), avg_train_errors, color="blue" , label = "Train Error")
plt.plot(range(1,16), avg_validation_errors, color="yellow", label = "Validation Error")
plt.title("Validation Error vs Train Error", loc= 'center')
plt.legend()
plt.show()

# find h*
index = avg_validation_errors.index(min(avg_validation_errors))
deg_Star = index + 1
print(deg_Star)

print(H)
