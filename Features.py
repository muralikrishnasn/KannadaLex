# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 18:03:19 2018

@author: Shreya Aithal
"""

import pandas as pd
import numpy as np
import sys

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


finaldf = pd.read_csv("Dataset", encoding='utf-8', error_bad_lines=False, index_col=0 , dtype = {'Prefix': unicode, 'Suffix': unicode, 'Addition'  : unicode} ) 
finaldf = finaldf.replace(np.nan, '', regex=True)

data = pd.DataFrame(columns = ['Prefix1','Prefix2', 'Prefix3','Current', 'Suffix1', 'Suffix2', 'Suffix3', 'Split' , 'PrefixLen' , 'SuffixLen' , 'Addition'], dtype = np.uint64)

for row in crazydf.itertuples():
   
    prefix = row.Prefix
    if len(prefix) >= 1:
        currletter = prefix[len(prefix)-1]
        currID = letter2id[currletter]
    else:
        currletter = ''
        currID = 0
    
    
    print(row.Index)
    
    pref1 = 0
    pref2 = 0
    pref3 = 0
    
    suffix = row.Suffix
    suff1 = 0
    suff2 = 0
    suff3 = 0
    
    addition = row.Addition
    addf = 0
    
    for letter in prefix:
        if pref1* 78 + letter2id[letter] < sys.maxsize:
            pref1 = pref1 * 78 + letter2id[letter] 
        elif pref2 * 78 + letter2id[letter] < sys.maxsize:
            pref2 = pref2 * 78 + letter2id[letter]
        else:
            pref3 = pref3 * 78 + letter2id[letter]
            
    
    for letter in suffix:
        if suff1 * 78 + letter2id[letter] < sys.maxsize:
            suff1 = suff1 * 78 + letter2id[letter] 
        elif suff2 * 78 + letter2id[letter] < sys.maxsize:
            suff2 = suff2 * 78 + letter2id[letter]
        else:
            suff3 = suff3 * 78 + letter2id[letter]    
    
        
    for letter in addition:
        if letter == '.':
            continue
        else:
            addf = addf * 78 + letter2id[letter]     
     
        
    data.loc[len(data)] = [pref1,pref2,pref3, currID, suff1,suff2, suff3, row.Split, row.PrefixLen, row.SuffixLen, addf] 
    
    
data.to_csv('FeatureSet', encoding='utf-8') 



   