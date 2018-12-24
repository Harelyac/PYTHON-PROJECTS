import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = "kc_house_data.csv"
data = pd.read_csv(file)


# remove unnecessary columns
data.drop(["id","date",'sqft_living','long','lat','condition','yr_renovated','sqft_living15','sqft_lot15'],axis=1,inplace=True)

# remove rows with axis are null
data.dropna(axis=0,how="any",inplace=True)

# make dummies columns by converting the original column of zipcode feature
data = pd.get_dummies(data,columns=['zipcode'])


# drop rows with irrational data in them
data.drop(data[data['price']<=0].index ,inplace=True)
data.drop(data[data['bathrooms']<=0].index ,inplace=True)
data.drop(data[data['floors']<0].index ,inplace=True)
data.drop(data[data['bedrooms']<=0].index ,inplace=True)


# insert intercept column to data-set
data.insert(loc=0,column="intercept",value = [1 for i in range(len(data))])


def divide_data(x):
    rows = np.random.rand(len(data)) < x/100
    train_sample = data[rows]
    test_sample = data[~rows]
    return train_sample,test_sample

def calculate_error(predicted_y,y):
    return (np.linalg.norm(predicted_y - y)**2)/len(y)

def regression():
    test_error_arr = list()
    train_error_arr = list()

    for x in range(1,100):
        train ,test = divide_data(x)

        # get the train price and test price
        train_price , test_price = train['price'], test['price']

        # drop price on both samples
        train = train.drop(['price'],axis=1)
        test = test.drop(['price'],axis=1)

        # get psuedo inverse of X transpose
        psuedo_inverse = np.linalg.pinv(train)
        w = np.dot(psuedo_inverse,train_price)

        # calculate errors of train and test
        train_error_arr.append(calculate_error(np.dot(train,w),train_price))
        test_error_arr.append(calculate_error(np.dot(test,w),test_price))

    # plot train and test error
    plt.plot([i for i in range(1,100)],train_error_arr,label="train error(mse)")
    plt.plot([i for i in range(1,100)],test_error_arr,label="test error(mse)")
    plt.xlabel("percentage of data trained")
    plt.ylabel("mse")
    plt.title("mse as a function of how much trained data")
    plt.legend()
    plt.show()
regression()