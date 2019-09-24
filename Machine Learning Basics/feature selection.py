import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy.stats import norm
from scipy.stats import gamma

# mean = 0
# sigma = 1
# gen = norm(mean, sigma)
# data = gen.rvs(size=1000)
# myHist = plt.hist(data, 20, normed=True, color = "skyblue", ec="yellow", label='histogram of samples')
# plt.title('1000 drawn points out of normal distribution; mu = 0, sigma = 1')
# x = np.linspace(-4, 4, 1000)
# plt.plot(x, norm.pdf(x), color='red', label='pdf of samples')
# plt.legend(loc='best')
# plt.show()

Q = np.array(((0.5*sqrt(3), -0.5*sqrt(3)), (0.5, 0.5)))
D = np.array(((2,0),(0,0.01)))
sigma = np.matmul(np.matmul(Q,D),Q.T)

# sigma = np.identity(2)

mu1 = [0,3/2]
mu2 = [0,-3/2]
data1 = np.random.multivariate_normal(mu1, sigma, 1000)
data2 = np.random.multivariate_normal(mu2, sigma, 1000)
x1, y1 = data1.T
x2, y2 = data2.T
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-6, 6)
ax.set_ylim(-4, 4)
plt.scatter(x1, y1,s=1, marker='*',color = 'g', label='mu = [0,3/2], Covariance matrix = identity 2')
plt.scatter(x2, y2,s=1, marker='*',color = 'b',label='mu = [0,-3/2], Covariance matrix = identity 2')
plt.title('Two populations of samples out of the Normal distribution in 2d')
plt.legend(loc='upper right')
plt.axis('equal')
plt.show()



# plt.subplot(211)
# myHist = plt.hist(x1, density=True,color="orange",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [1, 1]')
# myHist = plt.hist(x2, density=True,color="skyblue",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [-1, -1]')
# plt.legend(loc='upper right')
# plt.title('Histogram of first feature in each population')
#
# plt.subplot(212)
# myHist = plt.hist(y1, density=True,color="orange",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [1, 1]')
# myHist = plt.hist(y2, density=True,color="skyblue",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [-1, -1]')
# plt.legend(loc='upper right')
# plt.title('Histogram of second feature in each population')
#
# plt.show()


# theta = np.radians(45)
# cos, sin = np.cos(theta), np.sin(theta)
# rotate_matrix = np.array(((cos,-sin), (sin, cos)))
# rotated_data1 = np.matmul(rotate_matrix,data1.T)
# rotated_data2 = np.matmul(rotate_matrix,data2.T)
# x1, y1 = rotated_data1
# x2, y2 = rotated_data2
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xlim(-6, 6)
# ax.set_ylim(-4, 4)
# plt.scatter(x1, y1,s=1, marker='*',color = 'g', label='Population with mu = [1, 1]')
# plt.scatter(x2, y2,s=1, marker='*',color = 'b', label='Population with mu = [-1, -1]')
# plt.title('Rotation of the points from question 7.a')
# plt.legend(loc='bottom right')
# plt.axis('equal')
# plt.show()

# plt.subplot(211)
# myHist = plt.hist(x1, density=True,color="orange",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [1, 1]')
# myHist = plt.hist(x2, density=True,color="skyblue",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [-1, -1]')
# plt.legend(loc='upper right')
# plt.title('Histogram of first feature in each population')
#
# plt.subplot(212)
# myHist = plt.hist(y1, density=True,color="orange",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [1, 1]')
# myHist = plt.hist(y2, density=True,color="skyblue",ec='k', alpha=0.7 ,bins=20, label='Population with mu = [-1, -1]')
# plt.legend(loc='upper right')
# plt.title('Histogram of second feature in each population')
#
# plt.show()



