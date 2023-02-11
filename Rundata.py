'''
constructing time: 2019/12

enviroment: anoconda base + spyder

package: time, numpy, sklearn, matplotlib

author: P16081203

objective:
Using MLPRegressor to regress data to learn an unknown mapping
'''


import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor


# reading the data using pandas
Xi = pd.read_csv('All.csv')
X = []
X.append( Xi.values[:,1].flatten().tolist() )
X.append( Xi.values[:,2].flatten().tolist() )
X.append( Xi.values[:,3].flatten().tolist() )
X.append( Xi.values[:,4].flatten().tolist() )
X = np.transpose( np.array(X) )
Y = []
Y.append( Xi.values[:,0].flatten().tolist() )
Y = np.transpose( np.array(Y) )

# split data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size = 0.75, random_state = 42, shuffle = True)

# MLP model
model = MLPRegressor(hidden_layer_sizes = (70,40,),
                      activation = 'relu',
                      solver = 'adam',
                      learning_rate = 'adaptive',
                      learning_rate_init = 0.001,
                      max_iter = 10000,
                      verbose = True,
                      momentum = 0.9)
# start to count
start = time.time()

# fit (training)
model.fit(X_train, Y_train)

# stop to count
end = time.time()
timecost = start - end
print('time cost: %.5f sec' %timecost)

# predict and result
Pred = model.predict(X_test)

# we use abs(true value - predict value) to analyize
#result = [ Pred[i] - Y_test[i] for i in range(M_ts) ]

# data construction
col = ['x[1]', 'x[2]', 'x[3]', 'x[4]', 'y from real function (A)', 'y from prediction (B)', 'relative error (B-A)/A']
data = []
for i in range(len(Y_test)):
    tmp = [ X_test[i][0], X_test[i][1], X_test[i][2], X_test[i][3], Y_test[i][0], Pred[i], (Pred[i] - Y_test[i][0]) / Y_test[i][0] ]
    data.append(tmp)

# using pandas to output
# dataframe
df = pd.DataFrame(data, columns = col)
df.to_csv('Compare.csv')

# using matplotlib
# base line
y_b = np.linspace(3000,12000)# (,)之間的值 
# show scatter
fig1, axs1 = plt.subplots()
axs1.plot(y_b, y_b, 'r--')
axs1.scatter(Y_test, Pred)
axs1.set_xlabel('real index')
axs1.set_ylabel('predict index')
