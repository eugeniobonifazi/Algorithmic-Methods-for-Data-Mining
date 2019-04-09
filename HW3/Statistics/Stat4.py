from pymongo import MongoClient
from bson.son import SON
import json
import matplotlib.pyplot as plt



params = {'apiKey': 'RKnHYU5eIIdsSC6h5nhwm2zck7FYFgTp'}
dbname = 'lyricsdb'
collection = 'Index'
url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection
headers = {'content-type': 'application/json'}


db = MongoClient("mongodb://lyrics:123456789@ds113936.mlab.com:13936/lyricsdb").lyricsdb

pipeline = [
    {"$unwind": "$lyrics"},
    {"$limit": 40000},
    {"$group": {"_id": "$lyrics"}},
    {"$sort": SON([("count", -1), ("_id", -1)])}]

a=list(db.songs.aggregate(pipeline))



lyrics = {}   # we create a dictionary assigning a number to each lyric
num=0
for i in a:
    num+=1
    lyrics[num]=i['_id']


# here we count the lenght of each lyric and fix it to the corrisponding number (the same of dictionary lyrics)
d = {}
for i in range(1,len(lyrics)+1):
    lyric = lyrics[i]         # take each lyric
    words = lyric.split(' ')  # split it into words
    d[i] = len(words)         # append the length of the i-th lyrics to dictionary



d2 = {}    # since we have
for key, values in d.items():
    if values<=1200:
        d2[key]=values




plt.hist([i for i in d2.values()], bins=20, width=15)
plt.title("Songs length")
plt.xlabel("Number of words")
plt.ylabel("Number of artists")
plt.show()
