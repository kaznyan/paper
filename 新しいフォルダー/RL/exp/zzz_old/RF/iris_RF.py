
import numpy as np
import sklearn
import sklearn.ensemble
from sklearn import datasets
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()
y = np.zeros((len(iris.target), 1 + iris.target.max()), dtype=int)
y[np.arange(len(iris.target)), iris.target] = 1
train_x, test_x, train_y, test_y = train_test_split(iris.data, y, test_size=0.25)
print(test_x.shape)

# rf = sklearn.ensemble.RandomForestClassifier()
rf = sklearn.ensemble.RandomForestRegressor()
rf.fit(train_x, train_y)
prediction = rf.predict(test_x)
accuracy = rf.score(test_x, test_y)
print('accuracy {0:.2%}'.format(accuracy))
