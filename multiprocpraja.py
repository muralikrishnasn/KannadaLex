# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:28:37 2018

@author: Shreya
"""
import json
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib 
import requests
import re
import urlparse
import time




def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    
    if isinstance(element, Comment):
        return False
    return True

#def notMenu(css_class):
#    return css_class is not 'menubg'

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    #print(soup.prettify)
    #soup.find('nav',id='sports-menu-wrapper').decompose()
    node = soup.find('div', attrs={'class': 'body'})
    texts = node.findAll(text=True)
    #texts = soup.find_all(text=True)
    #print(texts)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


def word_print(html, filename):
    alltext = text_from_html(html.text)
    data = alltext.split(".")
    count = 0
    for sentence in data:
        #print(sentence)
        sentence = sentence.strip();
        words = sentence.replace(';',' ').replace(',',' ').replace('(',' ').replace(')',' ').split(" ")
        sentenceFlag = 1
        for x in words :        
            if len(x) == 0:
                continue
            flag = 0
            for y in x:
                if re.match(u'[\u0C80-\u0CEF]',y):
                    continue
                else:
                    flag = 1
                    break
            if flag == 0:
                #print(x + " : " + str(len(x)))
                s = x + '\n'
                with open(filename, "a") as f:
                   f.write(s.encode("UTF-8"))
                count =  count + 1
            else:
                sentenceFlag = 0
                
        if sentenceFlag == 1:
            sentence = sentence  + '\n'
            with open("Sentence/" + filename, "a") as f:
                   f.write(sentence.encode("UTF-8"))
           
    return count












from multiprocessing import Process

#def f(name):
#    print 'hello', name
#
#if __name__ == '__main__':
#    p = Process(target=f, args=('bob',))
#    p.start()
#    p.join()
    
    

def proctarget(y, post_params, urlNews, url):
    
    prox = {'http': '172.16.19.10:80'}
    
    dateno = ['01','02','03', '04', '05', '06' ,'07','08','09']
    for x in range (10,32):
        dateno.append(str(x))
    
    month = ['01','02', '03', '04', '05', '06' ,'07','08','09', '10', '11', '12']
    mdays = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    years = ['2011','2012','2013','2014','2015','2016','2017']

    
    
    for m in range(0,12):
        for i in range(1,mdays[m]+1,3):
            time.sleep(10)
            post_params['arcDate'] = "" + years[y] + "-" + month[m] + "-" + dateno[i-1] 
            #post_params['arcDate'][:8] + dateno[i-1]
            print (post_params)
#            with open("Folder/"+post_params['arcDate'], "w") as f:
#                f.write('YES')
            cnt = 0
            titlelist = []
            
            html = requests.post(url, proxies=prox,data = post_params)
#            with open("yes", "w") as f:
#                f.write(html.text.encode("UTF-8"))
            
            loaded_json = json.loads(html.text)
            #print(loaded_json)
            if not loaded_json:
                print "empty"
            else:
                for head,contentlist in loaded_json.items():
                    for line in contentlist:
                        #print line[u'url']
                        
                        titlefound = 0
                        
                        for titles in titlelist:
                            #print(line[u'title'], titles)
                            if line[u'title'] == titles:
                                titlefound = 1
                                break
                        if titlefound == 1:
                            continue
                        
                        #print(line[u'title'])
                        titlelist.append(line[u'title'])
                        #print('\n\n', titlelist)
        
                        recuLink = line[u'url']
                        recuLink = urlNews + recuLink
                        #print(recuLink)
                        html = requests.get(recuLink, proxies=prox)
                        cnt = cnt + word_print(html, "WordData/" + post_params['arcDate'])
            
            print cnt
        
    



post_params = {"arcDate" : "2011-01-01"}
#post_args = urllib.urlencode(post_params)
urlNews = 'http://www.prajavani.net/news'

url = 'http://www.prajavani.net/mobile/archive'

dateno = ['01','02','03', '04', '05', '06' ,'07','08','09']
for x in range (10,32):
    dateno.append(str(x))

month = ['01','02', '03', '04', '05', '06' ,'07','08','09', '10', '11', '12']
mdays = [31,28,31,30,31,30,31,31,30,31,30,31]

years = ['2011','2012','2013','2014','2015','2016','2017']

totcount = 0
procs = []

for y in range(0,7):     #for each cluster:
    if __name__ == '__main__':
        p = Process(target=proctarget, args=(y,post_params, urlNews, url))
        procs.append(p)
        p.start()
    
for p in procs:
    p.join()    
