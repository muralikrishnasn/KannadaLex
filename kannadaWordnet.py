import pickle
import sys

import matplotlib
import pyiwn
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

def fill(suff):
    #suff = suff.item()
    while suff * 10 < sys.maxsize and suff * 10 > 0:
        suff = suff * 10
    return suff


def predictAddn(features):
    filename = 'svmSaved.sav'  # 'svmAddnNew.sav'
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
    filename = 'svmSaved.sav'  # 'svm3classNew.sav'
    clf = pickle.load(open(filename, 'rb'))
    predictions = []
    currID = 0

    for i in range(len(word) + 1):
        prefix = word[0:i]
        suffix = word[i:len(word)]

        if len(prefix) >= 1:
            currletter = prefix[len(prefix) - 1]

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

        suff1 = fill(suff1)
        suff2 = fill(suff2)
        suff3 = fill(suff3)

        predarr = [[currID, suff1, suff2, suff3]]

        split = clf.predict(predarr)
        # print 'prefix:'+ prefix
        # print (split)
        predictions.append(split[0])
        if split[0] == 1 and found == 0:
            root = prefix
            found = 1
        elif split[0] == 2 and found == 0:
            root = prefix
            found = 2
    #print(predictions)
    if found == 0:
        root = word
    elif found == 2:
        root = root + predictAddn([currID, suff1, suff2, suff3])

    #print(root)
    return root



iwn = pyiwn.IndoWordNet(pyiwn.Language.KANNADA)
print(len(iwn.all_words(pos=pyiwn.PosTag.NOUN)))
# for word in iwn.all_words(pos=pyiwn.PosTag.VERB):
#     if '_' not in word and '-' not in word:
#         try:
#             print(word,'\t', predictit(word))
#             if(word != predictit(word)):
#                 print('Split found')
#                 print(word, predictit(word))
#         except:
#             print('Key Error')
