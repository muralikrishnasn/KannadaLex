# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 09:59:03 2018

@author: Shreya
"""

import numpy as np
from sklearn import svm, datasets

iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target

from sklearn.svm import SVC

clf = SVC()
clf.fit(X,y)
clf.predict([[5,2.9],[6,2.9]])