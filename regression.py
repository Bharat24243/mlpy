import pandas as pd data = pd.read_csv('crime_data_processed.csv') 
import numpy as np 
import matplotlib.pyplot as plt

X=data.as_matrix(columns=['avg_hatecrimes_per_100k_fbi','share_voters_voted_trump']) X

maxX = np.max(X, axis=0) minX = np.min(X, axis=0) X = (X-minX)/(maxX-minX) print( X )

X = np.insert(X, 0, 1, axis=1)

y=data.as_matrix(columns=data.columns[12:13])

y

def visualize(X, y, col1=1, col2=2): positive_indexes = np.where(y == 1)[0] negative_indexes = np.where(y == -1)[0]

positive = X[positive_indexes]
negative = X[negative_indexes]

fig, ax = plt.subplots(figsize=(12,8))
ax.scatter(positive[:,1:2], positive[:,2:], s=50, c='b', marker='o', label='Positive')
ax.scatter(negative[:,1:2], negative[:,2:], s=50, c='r', marker='x', label='Negative')
ax.legend()
ax.set_xlabel('col' + str(col1))
ax.set_ylabel('col' + str(col2))

plt.show()
visualize(X,y)

w = np.ones((1,X.shape[1])) def sigmoid(z): return 1/(1+np.exp(-z))

def predict(w, X): y_predict = np.zeros((1,X.shape[0])) z = X@w.T pred_fn = sigmoid(z).T high = (pred_fn>0.5) low = (pred_fn<0.5) y_predict[high] = 1 y_predict[low] = -1 return y_predict.T

def accuracy(y,y_predict): return (y[y==y_predict].shape[0]/(y[y==y_predict].shape[0]+y[y!=y_predict].shape[0]))

y_predict = predict(w,X) print( accuracy(y,y_predict) )

def error(X,y,w): return(np.log(1+np.exp(-y*X@w.T))) def errormean(X,y,w): error(X,y,w) em=np.sum(error(X,y,w)) n=X.shape[0] return(em/n) errormean(X,y,w) print(errormean(X,y,w))

def grad(X,y,w): return (yX)/(1+np.exp(yX@w.T)) def gradmean(X,y,w): grad(X,y,w) n=X.shape[0] xy=(-1/n)*np.sum(grad(X,y,w),axis=0,keepdims=True) return xy print(gradmean(X,y,w))

def fit(X,y,kappa,iter): w = np.zeros((1,X.shape[1])) E = [] for i in range(iter): E.append(errormean(X,y,w)) w = w - kappa*(gradmean(X,y,w)) return w,E

w,E=fit(X,y,6,100) print(w) plt.plot(E) plt.show()

def split_train_test(X,y,pct=80): n = X.shape[0] s = round(n * pct / 100)

indices = np.random.permutation(n)
train_idx, test_idx = indices[:s], indices[s:]

X_train, X_test = X[train_idx,:], X[test_idx,:]
y_train, y_test = y[train_idx,:], y[test_idx,:]

return X_train, y_train, X_test, y_test
X_train, y_train, X_test, y_test = split_train_test(X,y,pct=80) w,E = fit(X_train,y_train,6,1000) print(w) plt.plot(E) plt.show() y_pred = predict(w,X_test) print( accuracy(y_test,y_pred) )

Now checking different parameters of the regression
from sklearn.model_selection import train_test_split X_train, X_test, y_train, y_test = train_test_split(X, y)

from sklearn.linear_model import LogisticRegression logreg = LogisticRegression() logreg.fit(X_train, y_train)

y_pred_class = logreg.predict(X_test) print(y_pred_class)

from sklearn import metrics

print('Accuracy ' + str( metrics.accuracy_score(y_test, y_pred_class)))

print(metrics.confusion_matrix(y_test, y_pred_class))

confusion = metrics.confusion_matrix(y_test, y_pred_class) TP = confusion[1, 1] TN = confusion[0, 0] FP = confusion[0, 1] FN = confusion[1, 0]

print((TP + TN) / float(TP + TN + FP + FN)) print(metrics.accuracy_score(y_test, y_pred_class))

print((FP + FN) / float(TP + TN + FP + FN)) print(1 - metrics.accuracy_score(y_test, y_pred_class))

print(TP / float(TP + FN)) print(metrics.recall_score(y_test, y_pred_class))

print(TN / float(TN + FP))

print(TP / float(TP + FP)) print(metrics.precision_score(y_test, y_pred_class))

logreg.predict(X_test)[0:10]

logreg.predict_proba(X_test)[0:10, :]

y_pred_prob = logreg.predict_proba(X_test)[:, 1]

get_ipython().run_line_magic('matplotlib', 'inline') import matplotlib.pyplot as plt

plt.hist(y_pred_prob, bins=8) plt.xlim(0, 1) plt.title('Histogram of predicted probabilities') plt.xlabel('Predicted probability of crime rate') plt.ylabel('Probability')
