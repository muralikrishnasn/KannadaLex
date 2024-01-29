# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 14:14:10 2018

@author: Shreya Aithal
"""
import pandas as pd
from sklearn import svm
import numpy as np
import sys
from sklearn.model_selection import train_test_split
import pickle

start = u'\u0C80'
end = u'\u0CCD'

currord = startord = ord(start)
endord = ord(end)

count = 0

letters = []
ids = []


while currord <= endord:
    letters.append(chr(currord))
    ids.append(count)
    count = count + 1
    currord = currord + 1
    
letter2id = dict(zip(letters, ids))
id2letter = dict(zip(ids, letters))    



data = pd.read_csv("FeatureSet", encoding='utf-8', on_bad_lines='skip', index_col=0 )

X = data.iloc[:,3:7]
y = data.iloc[:, 7]

X = X.values#as_matrix(columns=X.columns[0:])
y = y.values#as_matrix()
print('Training start')


from sklearn.svm import SVC

clf = SVC()
clf.fit(X,y)

print('Training end')

filename = 'svmSaved.sav'
pickle.dump(clf,open(filename, 'wb'))
print('Saved')

word = u'ಕಾಲದಲ್ಲಿ'
#
def predictit(word):
    root = ''
    found = 0
    filename = 'svmSaved.sav'
    clf = pickle.load(open(filename, 'rb'))
    predictions = []
    currID = 0
    
    for i in range(len(word)+1):
        prefix = word[0:i]
        suffix = word[i:len(word)]
    
        if len(prefix) >= 1:
            currletter = prefix[len(prefix)-1]
            
            currID = letter2id[currletter]
        else:
            currletter = ''
            currID = 0
        
        suff1 = 0
        suff2 = 0
        suff3 = 0
        
        for letter in suffix:
            if suff1 * 78 + letter2id[letter] < sys.maxsize:
                suff1 = suff1 * 78 + letter2id[letter] 
            elif suff2 * 78 + letter2id[letter] < sys.maxsize:
                suff2 = suff2 * 78 + letter2id[letter]
            else:
                suff3 = suff3 * 78 + letter2id[letter]    
            
        predarr = [[currID, suff1,suff2,suff3]]
        
        split = clf.predict(predarr)
        print('prefix:', prefix)
        print (split)
        predictions.append(split[0])        
        if split[0] == 1:
            root = prefix
            found = 1
            
        
        
    print(predictions)
    if found == 0:
        root = word
    
    print(root)
    return root
    
    
   
            

print('Training 75% and Test 25% Cross validation- 5-fold')
train_X, test_X, train_y, test_y = train_test_split(X,y,test_size=0.25, random_state=0)
clf = SVC()
clf.fit(train_X,train_y)
print('Mean score of accuray is:')
print(clf.score(test_X, test_y))

print('Cross validation score is:')
from sklearn.model_selection import cross_val_score
clf = SVC()
scores = cross_val_score(clf, X,y,cv=5)
print(scores.mean(), scores.std() * 2)
print('Process Completed')
