# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 14:38:26 2018

@author: Shreya
"""
import numpy as np


#Read all suffixes

filename = 'Set 4 16451 to  16741'
suffixlist = ''
f = open(filename, 'r', encoding="utf8")
lines = f.read().splitlines()
f.close()

for line in lines:
    words = line.split(" ")
    for word in words:
        if word.find("af=") == -1:
            continue
        else:
            word = word[4:len(word)-2]
            parts = word.split(',')
            if len(parts) == 8:
                if parts[6] != '0' and parts[6] != '':
                    suffixes = parts[6].split('+')
                    for suffix in suffixes:
                        suffixlist = suffixlist + suffix +'\n'
#print suffixlist


listofsuffixes = suffixlist.splitlines()
series = np.unique(listofsuffixes).tolist()

finallist = ''
for item in series:
    finallist = finallist + item + '\n'
print(finallist)

with open("suffixlist"+filename, "a", encoding="utf-8") as f:
    f.write(finallist)
f.close()