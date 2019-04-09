from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


from pymongo import MongoClient
import pprint
from bson.son import SON


numbers=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

'''
this function delete stopwords from the lyrics
'''
def remove_stopwords(word_tokens):
    stop_words = set(stopwords.words('english'))  # store the ordered stopwords of the english vocabulary (take the words just once)
    filtered_sentence = []

    for w in word_tokens:  #
        if w not in stop_words and w not in numbers:
            filtered_sentence.append(w)

    return filtered_sentence

db = MongoClient("mongodb://lyrics:123456789@ds113936.mlab.com:13936/lyricsdb").lyricsdb


pipeline = [
    {"$unwind": "$lyrics"},
    {"$limit": 40000},
    {"$group": {"_id": "$lyrics"}},
    {"$sort": SON([("count", -1), ("_id", -1)])}]


a=list(db.songs.aggregate(pipeline))   #the list of our 40000 lyrics (which are dictionaries....."_id": Lyrics)

b={}

for i in a:
    example_sent = i["_id"]               # it takes the lyrics
    example_sent = example_sent.lower()   # normalizing
    tokenizer = RegexpTokenizer(r'\w+')   # function that tokenize: from entire lyrics to a list of words
    x = tokenizer.tokenize(example_sent)
    e = remove_stopwords(x)               # we use the function defined before
    for i in e:                           # here we create the dictionary of words with the relative frequency
        if i not in b.keys():
            b[i] = 1
        else:
            b[i]+=1

b=sorted(b.items(), key=lambda x: x[1],reverse=True)    # sorting in decreasing order using the values of the dictionary (frequencies)

top10words=b[:20]
j=0
print("The 20 most popular words with the corrisponding frequency:", '\n')    # printing results
for s in top10words:
    j+=1
    print(j, s[0], ": ", s[1], " times")
    

'''
Since between the most common words we have words such as: "love", "like", "baby", "want" we can say that most of the songs are based on love.
Other interpretations could be debatable. As a matter of fact if we consider, for instance, the word "never" we could say that it has a negative meaning, but actually we should know the context in which the word is located for doing assumption on its meaning. 
'''

