# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:03:10 2018

@author: Shreya
"""

import pandas as pd

import re

import os

import codecs

def phonologicalrep (x):
    phono = ''
    for i in range(0,len(x)):
        if i == len(x) - 1 and re.match(u'[\u0C95-\u0CB9]',x[i]):            
            phono = phono + x[i] +u'\u0CCD'+ '-'+ u'\u0C85'+'-'
            
        elif  re.match(u'[\u0C95-\u0CB9]',x[i]) and not(re.match(u'[\u0CBE-\u0CCD]',x[i+1])) and  not(re.match(u'[\u0C82-\u0C83]',x[i+1]))   :            
            phono = phono+ x[i]+ u'\u0CCD'+ '-'+u'\u0C85'+'-'
            
        elif re.match(u'[\u0C95-\u0CB9]',x[i]) and x[i+1] == u'\u0CCD':
            phono = phono+ x[i]+ u'\u0CCD'+ '-'
            
        elif re.match(u'[\u0C95-\u0CB9]',x[i]):
            phono = phono+ x[i]+ u'\u0CCD'+ '-'
            
        elif re.match(u'[\u0CBE-\u0CCC]',x[i]):
            phono = phono + unichr(ord(x[i])-56) +'-'
        
        elif x[i] == u'\u0CCD':
            pass
        
        else:
            phono = phono + x[i] + '-'
    
    phono = phono[:len(phono)-1]
    return phono

def syllabicrep(x):
    x = x.split('-')
    syll = ''
    syllabic = ''
    for phonemes in x:
        if re.match(u'[\u0C95-\u0CB9]',phonemes[0]):
            syll = syll + 'C'
            syllabic = syllabic + phonemes + '-'
        elif re.match(u'[\u0C82-\u0C94]',phonemes[0]):
            syll = syll + 'V-'
            syllabic = syllabic + phonemes + ':'
            
    
    #print syll.count('-')
    syll = syll[:len(syll)-1]    
    #print syll        
    
    syllabic = syllabic[:len(syllabic)-1]
    return  syll, syllabic

def complexsyllables(x):
    count = 0
    x = x.split('-')
    for parts in x:
        if parts == 'CCV' or parts == 'CCCV':
            count = count + 1        
    return count


def insertsyllabic(x):
    syllables = x.split(':')
    for syll in syllables:
        
        rel_path = "Syllables"           
        if os.stat(rel_path).st_size == 0:
            checkdf = pd.DataFrame(columns=['Syllable','Freq'])

        else:
            checkdf = pd.read_csv(rel_path, encoding='utf-8')
            if (checkdf['Syllable'] == syll).any():
                checkdf.loc[checkdf['Syllable'] == syll, 'Freq'] += 1
                checkdf.to_csv(rel_path, encoding='utf-8', index=False)
                continue
            
        
        #print syll

        smalldf = pd.DataFrame([[syll, 1]], columns = ['Syllable','Freq'])
        checkdf = checkdf.append(smalldf, ignore_index=True)
        
        checkdf.to_csv(rel_path, encoding='utf-8', index=False)


def findtotalcount(x):
    syllables = x.split(':')
    count = 0 
    for syll in syllables:
        rel_path = "Syllables"
        checkdf = pd.read_csv(rel_path, encoding='utf-8')
        #print syll, checkdf.loc[checkdf['Syllable'] == syll, 'Freq']
        count = count + int(checkdf.loc[checkdf['Syllable'] == syll, 'Freq'])
        
    return count

def insertBIsyllabic(x):
    syllables = x.split(':')
    for i in range(0,len(syllables)-1):
        bigram = syllables[i] +':'+ syllables[i+1]
        rel_path = "BigramSyllables"           
        if os.stat(rel_path).st_size == 0:
            checkdf = pd.DataFrame(columns=['BigramSyllable','Freq'])
        
        else:
            checkdf = pd.read_csv(rel_path, encoding='utf-8') 
            
            if (checkdf['BigramSyllable'] == bigram).any():
                checkdf.loc[checkdf['BigramSyllable'] == bigram, 'Freq'] += 1
                checkdf.to_csv(rel_path, encoding='utf-8', index=False)
                continue
        
        #print bigram
        smalldf = pd.DataFrame([[bigram, 1]], columns = ['BigramSyllable','Freq'])
        checkdf = checkdf.append(smalldf, ignore_index=True)
        
        checkdf.to_csv(rel_path, encoding='utf-8', index=False)
        


def findtotalBIcount(x):
    syllables = x.split(':')
    count = 0 
    for i in range(0,len(syllables)-1):
        rel_path = "BigramSyllables"
        checkdf = pd.read_csv(rel_path, encoding='utf-8')
        bigram = syllables[i] +':'+ syllables[i+1]
        count = count + int(checkdf.loc[checkdf['BigramSyllable'] == bigram, 'Freq'])
        #print bigram, int(checkdf.loc[checkdf['BigramSyllable'] == bigram, 'Freq'])
    return count
##################################################################################################################################
##################################################################################################################################


filename = '2011-02-01'

dateno = ['01','02','03', '04', '05', '06' ,'07','08','09']
for x in range (10,32):
    dateno.append(str(x))

directory = "WordData"
for filename in os.listdir(directory):
    rel_path = "WordData/" + filename
    print filename
    
    f = file(rel_path, 'r')
    words = f.read().decode('utf8').splitlines()
    f.close()
    
    df = pd.DataFrame(columns=['Word','Freq'])
    
    allwords_string = filename
    
    
    for x in words:
        df = df.append({'Word':x},  ignore_index=True)
        
        
    #print df
    answer = df['Word'].value_counts().to_frame()
    #answer['count'] = answer['Word']
    #answer['Word'] = answer.index
    answer = answer.reset_index()
    answer = answer.rename(index=str, columns={"index": "Word", "Word": "Freq"})
    del df
    
    
    
    
    for row in answer.itertuples():
        #print row[1], row[2], type(row[2])
    
        presentflag = 0
        f = codecs.open('Allwords', encoding='utf-8')
        for line in f:
    #        print line
            allwords = line.split(',')
    #        print allwords
            if row[1] in allwords[1:]:
                #print row[1]
    #            
                rel_path = "Features/" + allwords[0].encode('ascii','ignore')
    ###            
    ###            
                checkdf = pd.read_csv(rel_path, encoding='utf-8')
    ###            
                checkdf.loc[checkdf['Word'] == row[1], 'Freq'] += int(row[2])
                
                #print row[1], checkdf.loc[checkdf['Word'] == row[1], 'Freq']
    #            
                #print checkdf[0:5]
                checkdf.to_csv(rel_path, encoding='utf-8', index=False)
    #            
    #            
                answer = answer.drop(row[0])
                
                presentflag = 1
                break
    #            #continue
    #            #read the table from file
    #            #change frequency
    #            #write back
    #            #drop column
        f.close()
        if presentflag == 1 :
            continue
        
        
        
        phono = phonologicalrep(row[1])
        
        #remove abbreviations and few stop words
        if(phono.count('-') + 1 <= 3):
            answer = answer.drop(row[0])
            continue
        
        #Word length
        answer = answer.set_value(row[0],'WordLength', len(row[1]))
        
        #phonological rep and phoneme count
        answer = answer.set_value(row[0],'PhonologicalRep', phono)
        phonemecount = phono.count('-') + 1
        answer = answer.set_value(row[0],'PhonemeCount', phonemecount)
        
        #syllabic rep and syllable counts
        CVpattern, syllabic = syllabicrep(phono)
        insertsyllabic(syllabic)
        insertBIsyllabic(syllabic)
        answer = answer.set_value(row[0],'SyllabicRep', syllabic)
        answer = answer.set_value(row[0],'CVPattern', CVpattern)
        syllablecount = CVpattern.count('-') + 1
        answer = answer.set_value(row[0],'SyllableCount', syllablecount)
        complexsyll = complexsyllables(CVpattern)
        answer = answer.set_value(row[0],'ComplexSyllableCount', complexsyll)
    
        #store encountered words
        allwords_string = allwords_string + ',' + row[1]
        
    
    answer['WordLength'] = answer['WordLength'].astype(int)
    answer['PhonemeCount'] = answer['PhonemeCount'].astype(int)
    answer['SyllableCount'] = answer['SyllableCount'].astype(int)
    answer['ComplexSyllableCount'] = answer['ComplexSyllableCount'].astype(int)
    
    answer = answer.reset_index(drop=True)
    #print answer    
    
    answer.to_csv('Features/'+filename, encoding='utf-8')
    
    allwords_string = allwords_string + '\n'
    with open('Allwords', "a") as f:
        f.write(allwords_string.encode("UTF-8"))

#
#
#directory = "FeaturesNew"
#for filename in os.listdir(directory):
#    rel_path = "FeaturesNew/" + filename
#    print filename
#    checkdf = pd.read_csv(rel_path, encoding='utf-8')
#    for row in checkdf.itertuples():
##        summed = findtotalBIcount(row.SyllabicRep)
#        print row.Index
#        checkdf = checkdf.set_value(row[0],'SummedBigramSyllable', summed)
#    checkdf['SummedBigramSyllable'] = checkdf['SummedBigramSyllable'].astype(int)
#    checkdf.to_csv(rel_path, encoding='utf-8', index=False)
#        insertsyllabic(row.SyllabicRep)
#        insertBIsyllabic(row.SyllabicRep)