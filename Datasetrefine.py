# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 15:05:11 2018

@author: Shreya Aithal
"""

import pandas as pd
#Cleaning - stage 1

#Suffixes that can be split without need for grammar rules :into intdf
#Those that need further processing : into procdf

intdf = pd.DataFrame(columns = ['Word','Prefix', 'Suffix'])

newdf = pd.DataFrame(columns = ['Word','Prefix', 'Suffix', 'ActualRoot'])
procdf = pd.DataFrame(columns =  ['Word', 'Root', 'Suffix', 'Suffixwx'])
procdf2 = pd.DataFrame(columns =  ['Word', 'Root', 'Suffix', 'Suffixwx'])

checkdf = pd.read_csv("datarefined", encoding='utf-8', error_bad_lines=False, names = ['Word', 'Root', 'POS','NaN','sg/pl','3','d/o','Suffix', 'Suffixwx']) 
checkdf = checkdf.drop(['POS', 'NaN', 'sg/pl', '3', 'd/o'], axis=1)
checkdf = checkdf.dropna(axis=0, how='any')
checkdf = checkdf.drop_duplicates(subset = ['Word', 'Root'])
for row in checkdf.itertuples():
    if row.Root.find('\'') == 0:
        checkdf.loc[row.Index, 'Root'] =  checkdf.loc[row.Index, 'Root'][1:]

for row in checkdf.itertuples():
    #print row.Word
    if row.Suffix == '0':
        intdf.loc[len(intdf)] = [row.Word, row.Root, ''] 
    elif row.Word.find(row.Root) == 0:
        intdf.loc[len(intdf)] = [row.Word, row.Root, row.Word[len(row.Root):]]
    else:
        procdf.loc[len(procdf)] = [row.Word, row.Root, row.Suffix, row.Suffixwx]


for row in procdf.itertuples():
    count = 2
    root = row.Root
    found = 0
    while count >= 0:
        root = root[:len(root)-1]
        count = count - 1
        if row.Word.find(root) == 0:
            newdf.loc[len(newdf)] = [row.Word, root, row.Word[len(root):], row.Root]
            found = 1
            break
    if found == 0:
        procdf2.loc[len(procdf2)] = [row.Word, row.Root, row.Suffix, row.Suffixwx]




##forming finaldf from intdf:
##
#
finaldf = pd.DataFrame(columns = ['Prefix', 'Suffix', 'Split', 'PrefixLen', 'SuffixLen', 'Addition'])         


for row in intdf.itertuples():
    print row.Word
    word = row.Word
    root = row.Prefix
    for i in range(len(word)+1):
        pre = word[0:i]
        suf = word[i:len(word)] 
        splitflag = 0
        prelen = len(pre)
        suflen = len(suf)
        if pre == root:
            splitflag = 1
        finaldf.loc[len(finaldf)] = [pre, suf, splitflag, prelen, suflen, '']
            


for row in newdf.itertuples():
    print(row.Word)
    word = row.Word
    root = row.Prefix
    actualroot = row.ActualRoot
    
    addition = ''
    
    for i in range(len(word)+1):
        pre = word[0:i]
        suf = word[i:len(word)] 
        splitflag = 0
        prelen = len(pre)
        suflen = len(suf)
        if pre == root:    
            splitflag = 1
            addition = actualroot[len(root):]
        else:
            addition = ''
            
        finaldf.loc[len(finaldf)] = [pre, suf, splitflag, prelen, suflen, addition] 

finaldf.to_csv('Dataset', encoding='utf-8')
