import numpy
import matplotlib.pyplot as plt

# make a matrix with 100000 sequences (rows) of 1000 tosses each (column)
data = numpy.random.binomial(1,0.25,(100000,1000))

epsilon_list = [0.5,0.25,0.1,0.01,0.001]
asnwer_b = [[0 for i in range(1000)] for j in range(100000)]
asnwer_a = [[0 for k in range(1000)] for d in range(6)]

for row in range(6):
    sum = 0
    for col in range(1000):
        sum += data[row][col]
        asnwer_a[row][col] = sum /(col+1)
    # after creating a row directly plot it
    plt.plot(range(1,1001),asnwer_a[row],label="Sequence {}".format(row+1))
    plt.ylabel("Mean")
    plt.xlabel("Tosses (m)")
    plt.title("The average based on number of tosses(m) on each sequence out of 5:")
    plt.legend(loc="upper-right")
plt.show()


def chebyshev(epsilon,m):
    return min((1 / (4*m*(epsilon**2))),1)

def hoefding(epsilon,m):
    return min((2 * numpy.exp(-2 * m * (epsilon ** 2))),1)



for epsilon in epsilon_list:
    cheby_upper_bound = list()
    hoef_upper_bound = list()
    sum_list = [0]*100000
    percentages = list()
    for m in range(1,1001):
        satisfy_count = 0
        cheby_upper_bound.append(chebyshev(epsilon,m))
        hoef_upper_bound.append(hoefding(epsilon, m))
    for col in range(1000):
        sum = 0
        sum_satisfy = 0
        for row in range(100000):
            sum_list[row] += data[row][col]
            mean = sum_list[row] /(col+1)
            if abs((mean - 0.25)) >= epsilon:
                sum_satisfy += 1
        percentage = sum_satisfy / 100000
        percentages.append(percentage)


    plt.plot(range(1, 1001), cheby_upper_bound, label="Chebyshev upper bound")
    plt.plot(range(1, 1001), hoef_upper_bound, label="Hoefding upper bound")
    plt.plot(range(1, 1001), percentages, label="Percentage of sequences satisfy inequality")
    plt.ylabel("Bound")
    plt.xlabel("Tosses (m)")
    plt.title("The bounds(Hoefding and Checbyshev) based on {}".format(epsilon))
    plt.legend(loc="upper right")
    plt.show()








