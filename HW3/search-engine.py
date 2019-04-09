from math import *
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from _heapq import *
from wordcloud import WordCloud
import json
import matplotlib.pyplot as plt
import numpy as np
ps = PorterStemmer()

with open('vocabulary.json', 'r', encoding='utf-8') as json_data:
    vocabulary = json.load(json_data)
    json_data.close()

with open('lyrics.json', 'r', encoding='utf-8') as json_data:
    lyrics = json.load(json_data)
    json_data.close()

with open('index.json', 'r', encoding='utf-8') as json_data:
    index = json.load(json_data)
    json_data.close()

with open('frequency.json', 'r', encoding='utf-8') as json_data:
    frequency = json.load(json_data)
    json_data.close()

with open('url_artist.json', 'r', encoding='utf-8') as json_data:
    url_artist = json.load(json_data)
    json_data.close()


# defining heapsort to sort the heap structure
def heapsort(iterable):

    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for i in range(len(h))]

# intersection
def intersect(a, b):

    return list(set(a) & set(b))


# setting the query
a = input("enter the set:").split()
query = list(map(lambda x: ps.stem(x), a))

# retrieving the id of the query to find it inside the inverted index
ind = [vocabulary[i] for i in query]

type = int(input("which type of query would you perform? (just digit '1' or '2')"))

if type == 1:

    # norm of query
    normq = sqrt(len(query))

    # we will use N in the idf values
    N = len(frequency)

    # idf calculated for each word
    idf = {}
    for j in index.keys():
        idf[j] = log(N/len(index[j]))

    # set of document we are interested in
    a = []
    d = []
    for j in ind:
        a.append(index[str(j)].keys())
    for i in a:
        d += i
    d = set(d)   # contains the list of the documents that contain at least one word of the query

    # this list will host the tf-idf cosine values
    h = []
    # this dict will contain the tf-idf cosine values linked to the n. of document which refears
    final_dic = {}
    for i in d:
        doc = []
        q = []
                            # norm of document
        normd = []
        f = (frequency[str(i)])
        for key, values in f.items():
            normd.append(values*idf[str(vocabulary[key])])
        normdoc = np.linalg.norm(normd)
                            # dot product
        for wd in query:
            try:
                doc.append(frequency[str(i)][wd]*(idf[str(vocabulary[wd])]))        # tf*idf
                q.append(1)
            except KeyError:
                doc.append(0)
                q.append(0)
        # numerator
        numerator = (np.dot(q, doc))
        # cosine
        cos = numerator/(normq*float(normdoc))
        final_dic[cos] = i
        h.append(cos)

    # sorting the list with heapsort and getting back the 10 greatest values
    a = heapsort(h)
    nv = a[-10:]

    # getting back the number of documents according to the cosine values and the dictonary final_dic
    result = []
    co = 1
    for i in nv:
        w = url_artist[str(final_dic[i])]
        for i, k in w.items():
            pl = i.split('_')[0].replace('+', ' ').title()
            print(co, ". Name of the song: " + pl + "   Name of the singer: " + k)
            co += 1

if type==2:
    # TYPE 2

    # getting all the songs that contains all the terms present in the query
    songs = {}
    for key, values in lyrics.items():
        if all(words in values for words in query):
            songs[key] = values


    # set of words we are interested in
    a = []
    words = []
    for j in songs.values():
        a.append(j)
    for i in a:
        words += i
    words = set(words)

    # wordsind contains all the id of the words given by the vocabulary collection ('love'->613)
    wordsind = [vocabulary[i] for i in words]

    # we want to calculate the idf of each word but in a restricted set of songs. For this reason we make the intersection between the two lists
    list1 = songs.keys()
    list2=[]
    wordsidf = {}
    for i in wordsind:
        list2 = index[str(i)].keys()
        wordsidf[i] = log(len(songs)/len(intersect(list1, list2)))

    # we are creating the vector of each documents in the space of the terms of the vocabulary.
    data = [] # data will host the tf idf normalized vectors after used for the clusters
    dictofdata = {}  # dict of data that stores the id count to the key of document. Used in the next lines to link the vector to other informations as artist, title, lyrics
    count = 0
    for key, values in songs.items():
        vector = []
        count += 1
        denom = 0
        for i in words:
            try:
                vector.append((wordsidf[vocabulary[i]] * frequency[key][i]))        # tf*idf vector
                denom += wordsidf[vocabulary[i]] * frequency[key][i]                # denom for normalizing
            except KeyError:
                vector.append(0)
        try:
            vector[:] = [x / denom for x in vector]
        except ZeroDivisionError:
            break
        dictofdata[count] = key
        data.append(vector)

    print("Your query is matching with ", len(songs), "songs. ")

    # asking user the number of cluster
    nclus = int(input("Please enter number of cluster:"))

    # here we use kmeans algorithm to create cluster, 300 iterations as default
    kmeans = KMeans(n_clusters=nclus, init='random')
    kmeans.fit(data)
    c = kmeans.predict(data)

    # we use this lines to append at the end of the vector in position -2 the cluster which each vector belongs and in
    # position -1 the id that links the vector to the original document according to the dictofdata dictionary

    mergeddata = []
    count = 0
    for row in range(0, len(data)):
        count += 1
        line = data[row][:]
        line.append(c[row])
        line.append(count)
        mergeddata.append(line)

    # first for loop creates the cluster one by one
    for c in range(0, nclus):
        result = []
        co = 1
        worcloud_send = []
        cluster = []
        print("cluster", c)
        for i in mergeddata:
            if i[-2] == c:
                cluster.append(i)

        # printing list of songs and artists per cluster
        for item in cluster:
            w = url_artist[dictofdata[item[-1]]]
            for z, k in w.items():
                pl = z.split('_')[0].replace('+', ' ').title()
                print(co, ". Name of the song: " + pl + "   Name of the singer: " + k)
                co += 1

        # printing the wordcloud for each cluster
        for item in cluster:
            wl = lyrics[dictofdata[item[-1]]]
            for j in wl:
                worcloud_send.append(j)
            s = ' '.join(worcloud_send)

        wordcloud = WordCloud().generate(s)
        wordcloud = WordCloud(max_font_size=40).generate(s)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        plt.close()