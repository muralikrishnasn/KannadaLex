# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:23:07 2018

@author: Shreya
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
#x = [[1,2,3]]
#y = [[2,4,6]]
#
#plt.xlabel('X axis')
#plt.ylabel('Y axis')
#plt.scatter(x,y, marker = ".")
#plt.show()
Y = [[0]]
directory = "Features"

for filename in os.listdir(directory):
    rel_path = "Features/" + filename
    print(filename)
    checkdf = pd.read_csv(rel_path, encoding='utf-8')
    y = checkdf.iloc[:,2]
    y = [y.as_matrix()]
    #WordLength = checkdf.iloc[:,2]
    #PhonemeCount = checkdf.iloc[:,4]
    #SyllableCount = checkdf.iloc[:,7]
    #ComplexSyllableCount = checkdf.iloc[:,8]
    Y = np.concatenate((Y,y), axis = 1)

plt.ylabel('Frequency')
X = [[0]]

for filename in os.listdir(directory):
    rel_path = "Features/" + filename
    checkdf = pd.read_csv(rel_path, encoding='utf-8')
    WordLength = checkdf.iloc[:,3]
    WordLength = WordLength.as_matrix()
    #PhonemeCount = checkdf.iloc[:,5]
    #SyllableCount = checkdf.iloc[:,8]
    #ComplexSyllableCount = checkdf.iloc[:,9]
    X = np.concatenate((X,WordLength), axis = 1)
    
plt.xlabel('WordLength')
plt.scatter(X,Y, marker = ".")
plt.show()