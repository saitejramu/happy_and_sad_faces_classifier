import numpy as np
import os
from PIL import Image
import scipy.linalg as sp
import pickle
from numpy.linalg import eigh
from matplotlib import pyplot as plt
from numpy.linalg import inv


#getting all the required arrays from pickle files
f = open('eigenvalues.pkl', 'rb')
eigenvalues = pickle.load(f)
f.close()
f = open("eigenvectors.pkl","rb")
eigenvectors = pickle.load(f)
f.close()
f = open("input.pkl","rb")
X = pickle.load(f)
f.close()
f = open("happy.pkl","rb")
happy_X = pickle.load(f)
f.close()
f = open("sad.pkl","rb")
sad_X = pickle.load(f)
f.close()

#assigning K a value
K = 20

#applying PCA to reduce the dimention from 10201 to K
happy_Y = (np.dot(eigenvectors[-K:],happy_X.T)).T
sad_Y = (np.dot(eigenvectors[-K:],sad_X.T)).T

#find class covariance matrix
S = np.dot(happy_Y.T,happy_Y)+np.dot(sad_Y.T,sad_Y)

#mean vector in the direction joining the means of two classes
M = np.mean(happy_Y,axis=0)-np.mean(sad_Y,axis=0)

# computing W = (S^-1)*M
W = np.dot(inv(S),M)

# projecting on to W
Y1 = np.dot(W,happy_Y.T)
Y2 = np.dot(W,sad_Y.T)

# loading test data from pickle files generated by testdata.py
f = open("happy_test.pkl","rb")
happy_test_X = pickle.load(f)
f.close()
f = open("sad_test.pkl","rb")
sad_test_X = pickle.load(f)
f.close()

happy_test_Y = (np.dot(eigenvectors[-K:],happy_test_X.T)).T
sad_test_Y = (np.dot(eigenvectors[-K:],sad_test_X.T)).T
Y1_test = np.dot(W,happy_test_Y.T)
Y2_test = np.dot(W,sad_test_Y.T)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(Y1,np.zeros_like(Y1), color='red', linewidth=3)
ax.scatter(Y2,np.zeros_like(Y2), color='blue', marker='^')
ax.scatter(Y1_test,np.ones_like(Y1_test), color='orange', linewidth=1)
ax.scatter(Y2_test,np.ones_like(Y2_test), color='green', marker='^')
plt.savefig("test_K_%s.png"%(K))
plt.show()
