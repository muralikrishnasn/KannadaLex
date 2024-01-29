# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 10:52:28 2018

@author: Shreya
"""
import os 
import numpy as np

lines = []
directory = "Suffixes"
for filename in os.listdir(directory):
        rel_path = "Suffixes/" + filename
        f = open(rel_path, 'r', encoding="utf8")
        lines = lines + f.read().splitlines()
        

series = np.unique(lines).tolist()

finallist = ''
for item in series:
    finallist = finallist + item + '\n'
print(finallist)

with open("finallist", "a") as f:
    f.write(finallist.encode("UTF-8"))         