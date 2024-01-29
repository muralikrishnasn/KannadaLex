# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:39:00 2018

@author: Shreya Aithal
"""
import os
import re




#Aggregate data and extract required information
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def kannadaword(word):
    if word == '':
        return False
    flag = 0
    for y in word:
        if re.match(u'[\u0C80-\u0CEF]',y):
            continue
        else:
            flag = 1
            return False
        
    if flag == 0:
        return True

directory = "Data"
datalist = ''

for filename in os.listdir(directory):
    rel_path = "Data/" + filename
    f = open(rel_path, 'r', encoding="utf8")
    lines = f.read().splitlines()
    f.close()
    
    for line in lines:
        morphword = ''
        fs = ''
        errflag = 0
        words = line.split(" ")
        for word in words:
            if word.find("af=") == -1:
                continue
            else:
                fs = word[4:len(word)-1]
                for word in words:
                    if word.find("name=") != -1:
                        morphword= word[6:len(word)-2]
                        if not kannadaword(morphword) :
                            errflag = 1
                        break
                break    
            
        if errflag == 0 and morphword != '':
            datalist = datalist + morphword + ',' + fs + '\n'
            print(morphword + ',' + fs + '\n')
    

with open("datarefined", "a") as f:
    f.write(datalist.encode("UTF-8"))
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
