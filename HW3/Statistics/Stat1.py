from pymongo import MongoClient  # just to connect with Mongodb
from bson.son import SON         #
import statistics as stat
import matplotlib.pyplot as plt


db = MongoClient("mongodb://lyrics:123456789@ds113936.mlab.com:13936/lyricsdb").lyricsdb

pipeline = [
    {"$unwind": "$artist"},  # Deconstructs an array field from the input documents to output a document for each element. Not match ------> single value, we want all the artists
    {"$group": {"_id": "$artist", "count": {"$sum": 1}}},  #  group......$sum it's an <accumulator> "ignore no numeric values
    {"$sort": SON([("count", -1), ("_id", -1)])}]   # sorting based on the frequency of artist's song

a=list(db.songs.aggregate(pipeline))

print('Total number of artists:', len(a))

'''
SOME STATISTICS
'''

print('\n','SOME STATISTICS')

#artists with less than 11 songs

freq_1=[]
for i in range(len(a)):
    if a[i]['count']<=11:
        freq_1.append(a[i]['_id'])
print('a) ','Number of artists with less than 11 songs:', len(freq_1), 'percentage:', "%.2f"% ((len(freq_1)/len(a))*100),'%')


#artists with more than 200 songs

freq_2=[]
for i in range(len(a)):
    if a[i]['count']>=200:
        freq_2.append(a[i]['_id'])
print('b) ','Number of artists with more than 200 songs:', len(freq_2), 'percentage:', "%.2f"% ((len(freq_2)/len(a))*100),'%')

#minimum, maximum, mean and median
c=[]   
for i in range(len(a)):
    c.append(int(a[i]['count']))

print('c) ', 'min:', min(c), 'max:', max(c), 'mean:', "%.2f"%(stat.mean(c)), 'median:', stat.median(c))

'''
ARTIST WITH MOST SONGS
'''
    
print('\n','ARTIST WITH MOST SONGS:')

print(a[0]['_id'], 'with', a[0]['count'], 'songs')
    
'''
HISTOGRAM of the number of songs per Artist divided into 20 classes
'''
print('\n','HISTOGRAM: ', '\n')
plt.hist([i["count"] for i in a], bins=20, width=8)
plt.title("Songs per artist")
plt.xlabel("Number of songs")
plt.ylabel("Number of artists")
plt.show()

'''
TEN MOST PRODUCTIVE ARTISTS IN OUR D.B.
'''

print('\n','THE TEN MOST PRODUCTIVE ARTISTS IN OUR D.B.:')

for i in range(0,10):
    print(a[i]['_id'])

'''

COMMENTS:

As we can see in the histogram, the highest frequency corresponds to the artists that wrote (in our database) a number of songs minor or equal to 11 (almost equal to the 32% of the artists).
On the contrary, the artists that wrote more than 200 are the 7% of the total. Considering the artists in the first ten positions we can make some remarks:
artists like David Bowie, Elton John, Rolling Stones (rock icons) and Dolly Parton (country songwriter) that are on the scene since the '60 so that's why they are so 'productive'; 
Regarding Lil Wayne, Eminem and Snoop Dogg, even if they are younger than the others, they belong to a musical genre (rap/hip-hop) in which artists tent to be very productive for the number of songs written;
Elvis Presley and Frank Sinatra are true icons for the modern music and, even if they died almost young, they wrote a lot of songs;
In the end, the last voice 'Various Artists' maybe corresonds to songs written by various artists not specified.

'''
