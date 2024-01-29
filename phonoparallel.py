# -*- coding: utf-8 -*-
"""
Created on Thu Mar 01 10:39:31 2018

@author: Shreya
"""
import os
import pandas as pd
import numpy as np

def subcost(x, y):
    if x == y:
        return 0
    else:
        return 1

    

def mineditdist(w1,w2):
    fail = 0
    m = len(w1) + 1
    n = len(w2) + 1
    dist = np.zeros((m,n))
    dist[0,0] = 0
    for i in range(0, m):
        dist[i,0] = i
    for j in range(0, n):
        dist[0,j] = j
    for i in range(1,m):
        for j in range(1,n):
            dist[i,j] = min(dist[i-1,j]+1, dist[i,j-1]+1, dist[i-1,j-1] + subcost(w1[i-1],w2[j-1]))
        if (dist[i,] > 1).sum() == m:
            fail = 1
            break    
    
    #print dist
    if fail == 1:
        return False
    if dist[m-1,n-1] == 1:
        return True
    else:
        return False

def AllPhono(x, word):
    neighs = word
    directory = "Features1"
    count = 0
    freq = 0
    for filename in os.listdir(directory):
        rel_path = os.path.join(directory,filename)
        checkdf = pd.read_csv(rel_path, encoding='utf-8')
        for row in checkdf.itertuples():
            #print row.PhonologicalRep
            w1 = x.split('-')
            w2 = row.PhonologicalRep.split('-')
            

            isNeigh = mineditdist(w1,w2)

            if isNeigh == True:
               neighs = neighs + ',' + row.Word
               count = count + 1
               freq = freq + row.Freq
               
    neighs = neighs +'\n'
    with open('Phono', "a") as f:
        f.write(neighs.encode("UTF-8"))
        #count = count + int(checkdf.loc[checkdf['Syllable'] == syll, 'Freq'])
        #print syll, int(checkdf.loc[checkdf['Syllable'] == syll, 'Freq'])
    return count, freq

directory = "FeaturesNew"
filename = "2011-01-01"
#for filename in os.listdir(directory):


def proctarget(dirname):
    print dirname
    for filename in os.listdir(dirname):
        rel_path = os.path.join(dirname, filename)
        checkdf = pd.read_csv(rel_path, encoding='utf-8')
        print rel_path
        for row in checkdf.itertuples():
            count, freq = AllPhono(row.PhonologicalRep, row.Word)
            print [row.Index, count]
            if count != 0:
                meanfreq = freq / count
            else:
                meanfreq = 0
            checkdf = checkdf.set_value(row[0],'PhonNeighDensity', count)
            checkdf = checkdf.set_value(row[0],'PhonNeighMeanFreq', meanfreq)
        
        checkdf['PhonNeighDensity'] = checkdf['PhonNeighDensity'].astype(int)
        checkdf['PhonNeighMeanFreq'] = checkdf['PhonNeighMeanFreq'].astype(int)
        
        checkdf.to_csv(rel_path, encoding='utf-8', index=False)


#
#
#newdf = checkdf[:1885]
#newdf['PhonNeighDensity'] = newdf['PhonNeighDensity'].astype(int)
#newdf['PhonNeighMeanFreq'] = newdf['PhonNeighMeanFreq'].astype(int)
#newdf.to_csv("2011-01-01withall", encoding='utf-8', index=False)


from multiprocessing import Process
directory = "FeaturesNew"
procs = []

for dirname in os.listdir(directory):
    dirnow = os.path.join(directory,dirname)
    if os.path.isdir(dirnow):
       
        if __name__ == '__main__':
            print dirnow
            p = Process(target=proctarget, args=(dirnow,))
            procs.append(p)
            p.start()
        
for p in procs:
    p.join()    


