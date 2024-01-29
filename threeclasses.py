# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:06:46 2018

@author: Shreya
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

word = u'ಕಾಲದಲ್ಲಿ'
#
def fill(suff):
    #suff = suff.item()
    while suff * 10 < sys.maxsize and suff * 10 > 0:
        suff = suff * 10
    return suff


def predictAddn(features):
    filename = 'svmAddn.sav'
    addnstr = ''
    
    clf = pickle.load(open(filename, 'rb'))
   
    predarr = [features]


    
    addn = clf.predict(predarr)
    addn = addn[0]
    addnt = addn
    rem = 0
    while addnt > 0:
        rem = addnt % 78
        char = id2letter[rem]
        addnstr = char + addnstr
        addnt = addnt // 78
    return addnstr

def predictit(word):
    root = ''
    found = 0
    filename = 'svm3class.sav'
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
            
#        suff1 = fill(suff1)
#        suff2 = fill(suff2)
#        suff3 = fill(suff3)
#        
        predarr = [[currID, suff1,suff2,suff3]]
        
        split = clf.predict(predarr)
        print ('prefix:', prefix)
        print (split)
        predictions.append(split[0])        
        if split[0] == 1 and found == 0:
            root = prefix
            found = 1
        elif split[0] == 2 and found == 0:
            root = prefix
            found = 2
            
        
        
    print(predictions)
    if found == 0:
        root = word
    elif found == 2:
        root = root + predictAddn([currID, suff1,suff2,suff3])
    
    print(root)
    return root
    

# predictit(word)



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#==============================================================================================================



#
#
#data = pd.read_csv("FeatureSet", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#
#addndata = pd.DataFrame(columns = ['Prefix1','Prefix2', 'Prefix3','Current', 'Suffix1', 'Suffix2', 'Suffix3', 'Split' , 'PrefixLen' , 'SuffixLen' , 'Addition'], dtype = np.uint64)
#
#for row in data.itertuples():
#    
#    if row.Split == 1 and row.Addition != 0:
#        split = 2
#        data.loc[row.Index, 'Split'] =  2
#        addndata.loc[len(addndata)] = [row.Prefix1,row.Prefix2,row.Prefix3, row.Current, row.Suffix1,row.Suffix2, row.Suffix3, split, row.PrefixLen, row.SuffixLen, row.Addition] 
#
#addndata.to_csv('FeaturesAddn', encoding='utf-8')
#data.to_csv('Feature3class', encoding='utf-8')    
#
#
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
#data = pd.read_csv("Feature3classNew", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#X = data.iloc[:,3:7]
#y = data.iloc[:, 7]
#
#X = X.as_matrix(columns=X.columns[0:])
#y = y.as_matrix()
#
#print 'Scaling'
#
#from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#scaler.fit(X)
#X = scaler.transform(X)
#
#print 'Scaling ends'
#
#
#
#print 'Training start'
#
#from sklearn.svm import SVC
#
#clf = SVC()
#clf.fit(X,y)
#
#print 'Training end'
#
#filename = 'svm3classNew1.sav'
#pickle.dump(clf,open(filename, 'wb'))
#
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#data = pd.read_csv("Feature3classNew", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#X = data.iloc[:,3:7]
#y = data.iloc[:, 7]
#
#X = X.as_matrix(columns=X.columns[0:])
#y = y.as_matrix()
#
#from sklearn.svm import SVC
#from sklearn.model_selection import cross_val_score
#clf = SVC()
#scores = cross_val_score(clf, X,y,cv=5)
#print scores.mean(), scores.std() * 2
#
#
#
#
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
#data = pd.read_csv("FeaturesAddnNew", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#X = data.iloc[:,3:7]
#yd = data.iloc[:, 10]
#
#X = X.as_matrix(columns=X.columns[0:])
#yd = yd.as_matrix()
#
#from sklearn.svm import SVC
#from sklearn.model_selection import cross_val_score
#clf = SVC()
#scores = cross_val_score(clf, X,yd,cv=2)
#print scores.mean(), scores.std() * 2
#
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#data = pd.read_csv("FeaturesAddnNew", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#X = data.iloc[:,3:7]
#yd = data.iloc[:, 10]
#
#X = X.as_matrix(columns=X.columns[0:])
#yd = yd.as_matrix()
#
#train_X, test_X, train_y, test_y = train_test_split(X,yd,test_size=0.25, random_state=0)
#
#clf = SVC()
#clf.fit(train_X,train_y)
#print clf.score(test_X, test_y)
#
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
#data = pd.read_csv("FeaturesAddnNew", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#X = data.iloc[:,3:7]
#yd = data.iloc[:, 10]
#
#X = X.as_matrix(columns=X.columns[0:])
#yd = yd.as_matrix()
#
#
#print 'Scaling'
#
#from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#scaler.fit(X)
#X = scaler.transform(X)
#
#print 'Scaling ends'
#
#
#
#
#print 'Training start'
#
#
#from sklearn.svm import SVC
#
#clf = SVC()
#clf.fit(X,yd)
#
#print 'Training end'
#
#filename = 'svmAddnNew1.sav'
#pickle.dump(clf,open(filename, 'wb'))
#
#
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#def fill(suff):
#    suff = suff.item()
#    while suff * 10 < sys.maxsize and suff * 10 > 0:
#        suff = suff * 10
#    return suff
#
#data = pd.read_csv("Feature3class", encoding='utf-8', error_bad_lines=False, index_col=0 ) 
#
#for row in data.itertuples():
#    print row.Index
#    
#    suff1 = fill(row.Suffix1)
#    suff2 = fill(row.Suffix2)
#    suff3 = fill(row.Suffix3)
#    
#    print row.Index
#    data.loc[row.Index, 'Suffix1'] =  suff1
#    data.loc[row.Index, 'Suffix2'] =  suff2
#    data.loc[row.Index, 'Suffix3'] =  suff3
#
#
#data.to_csv('Feature3classNew', encoding='utf-8') 
#
#
#data = pd.read_csv("FeaturesAddn", encoding='utf-8', error_bad_lines=False, index_col=0 )
#for row in data.itertuples():
#    print row.Index
#    
#    suff1 = fill(row.Suffix1)
#    suff2 = fill(row.Suffix2)
#    suff3 = fill(row.Suffix3)
#    
#    print row.Index
#    data.loc[row.Index, 'Suffix1'] =  suff1
#    data.loc[row.Index, 'Suffix2'] =  suff2
#    data.loc[row.Index, 'Suffix3'] =  suff3
#data.to_csv('FeaturesAddnNew', encoding='utf-8') 
#
#
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   