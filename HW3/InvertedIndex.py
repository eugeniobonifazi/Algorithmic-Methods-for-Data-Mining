from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
 
from collections import Counter
from pymongo import MongoClient
from bson.son import SON
import json
import requests
ps = PorterStemmer()





params = {'apiKey': 'RKnHYU5eIIdsSC6h5nhwm2zck7FYFgTp'}
dbname = 'lyricsdb'
collection = 'Index'
url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection
headers = {'content-type': 'application/json'}



numbers=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

#this function removes stopwords and stem the lyrics

def remove_stopwords(word_tokens):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words and w not in numbers:
            filtered_sentence.append(ps.stem(w))      # the words are stemmed, cleaned from stopwords and numbers

    return filtered_sentence

    


db = MongoClient("mongodb://lyrics:123456789@ds113936.mlab.com:13936/lyricsdb").lyricsdb

pipeline = [
    {"$addFields": {"_id": "$lyrics", "url": "$url", "artist": "$artist"}},
    {"$project": {"title": False, "lyrics": False }},
    {"$limit": 35000},
    {"$sort": SON([("count", -1), ("_id", -1)])}]


a=list(db.songs.aggregate(pipeline))


document=0   #the count for each doc that will be used as identifier of the songs
b = []
lyr={}
url_artist={}
'''
here we create two dictionaries: the first one (lyr) with the identifier as a key and the "dirty" lyrics as value; the second one containing urls and artists' names.
Both of the dictionaries have the same identifiers for the songs.
'''
for i in a:
    document+=1    # counter of the documents
    for key, values in i.items():
        url_artist[document] = {}
        lyr[document] = {}
        url_artist[document][i['url']]=i['artist']   # { 1: { **.html : bob dylan } }
        lyr[document]['_id']=i['_id']
'''
Now we create: the "lyrics" dictionary containing the lyrics cleaned; the "frequency" dictionary in which we have the counter of each song; 
the vocabulary containing all the words in our lyrics (without repetitions) and the relative value we assigned to them; and, finally, the "index" in which we have our identifier (and we have the related word in the vocabulary) and the relative tf for each document in which it compares. 
'''
lyrics = {}      # lyrics cleaned
index = {}       # word_id : (doc - tf of the words)
vocabulary = {}  # word_id - word
frequency = {}   # id
count=0

for keys, values in lyr.items():
    example_sent = values["_id"]
    example_sent = example_sent.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    x = tokenizer.tokenize(example_sent)
    e = remove_stopwords(x)      #end of cleaning part
    freq=Counter(e)
    lyrics[keys]=e
    frequency[keys]=freq

    for j in e:
        if j not in vocabulary:
           count+=1
           vocabulary[j]=count
    for key in freq:        
        if vocabulary[key] not in index:
            index[vocabulary[key]]={}
            index[vocabulary[key]][keys]=freq[key]
        else:
            index[vocabulary[key]][keys]=freq[key]

'''CODE FOR UPLOADING THE INDEX ON MLAB 
#our index took too much space for being uploaded for free
data = json.dumps(index)
response = requests.post(url, data=data, params=params, headers=headers)
print(response.text)
'''


'''HERE WE CREATE THE JSON FILES
print('done')
with open('vocabulary.json', 'w', encoding="utf-8") as outfile:
    json.dump(vocabulary, outfile)

with open('index.json', 'w', encoding="utf-8") as outfile:
    json.dump(index, outfile)

with open('frequency.json', 'w', encoding="utf-8") as outfile:
    json.dump(frequency, outfile)

with open('lyrics.json', 'w', encoding="utf-8") as outfile:
    json.dump(lyrics, outfile)
    
with open('url_artist.json', 'w', encoding="utf-8") as outfile:
    json.dump(url_artist, outfile)
'''
