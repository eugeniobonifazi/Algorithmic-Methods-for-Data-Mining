from pymongo import MongoClient

from bson.son import SON
import matplotlib.pyplot as plt


db = MongoClient("mongodb://lyrics:123456789@ds113936.mlab.com:13936/lyricsdb").lyricsdb

pipeline = [
    {"$unwind": "$artist"},
    {"$group": {"_id": "$artist", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}]

col=list(db.songs.aggregate(pipeline))


out=["Band","&amp;","The", "Of", "And","A","B","C", "D", "E","F","G","H","I","J","K", "L","M","N", "O","P", "Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"]
#ter = []
#count = 0

dic={}
#main part
for i in col:
    for key in i:   # since the structure is {"_id": 'author', "count": 'freq'}

        x=(i['_id']).split() # split the entire name of the artist
        y=i['count']         # take the freq
        for j in x:
            if j not in out: # looking if any compon is inside the out list
                name=j
                break        # stop the "for" at the first name that is ot in the list
    if name not in dic.keys(): # if it's the first time we meet the name
        freq=1                 # it's the first time the name appears
        dic[name]={}           # empty dictionary in the dic (with the name as the key)
        r = (freq,y)           # tuple of the frequency
        dic[name]=r            # append the tuple in the dict
        #ter.append(name)
        #count+=1
    else:
        lst = list(dic[name])  # transform the tuple into a list
        lst[0] = dic[name][0]+1  # add 1 to the frequency of the name
        lst[1] = dic[name][1] + y  # add the number of songs for the new "name"
        t = tuple(lst)           # again tuple
        dic[name] = t            # re-append the tuple in the dict

sorting = []
for y,z in dic.items():
    sorting.append(z)            # append the values (tuples) to the empty list
kk = sorted(sorting)             # order the tuples in increasing order (by frequency)
kk = kk[-10:]                    # take the last 10 (the higher ones)

'''
The ten most common singer names
'''

for ii in kk:                     # for the names and tuples
    for bb, zz in dic.items():    # for each tuple
        if ii == zz:              #
            print(bb, list(ii)[0], "times")


x_list =  []
y_list = []
for key, value in dic.items():     # the average value of the # of songs for each artist
    x_list.append(value[0])
    y_list.append(value[1]/value[0])
plt.scatter(x_list,y_list)
plt.xlabel("Frequency of the artists")
plt.ylabel("The average of songs for artist's frequency")
plt.show()

#matplotlib part of code

list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []

for key ,value in dic.items():
    if value[0] ==1:
        list1.append(value[1]/value[0])
    if value[0] ==2:
        list2.append(value[1]/value[0])
    if value[0] ==3:
        list3.append(value[1]/value[0])
    if value[0] ==4:
        list4.append(value[1]/value[0])
    if value[0] ==5:
        list5.append(value[1]/value[0])
    if value[0] ==6:
        list6.append(value[1]/value[0])
data = [list1,list2,list3,list4,list5,list6]
plt.boxplot(data)
plt.xlabel("Frequency of the artists")
plt.ylabel("The average of songs for artist's frequency")
plt.show()


'''COMMENTS
Since we have to visualize if there is any relation between number of songs written
and the name of the artist we have calculated the average of songs written for the
artist whose name appears more than once. For artist whose name is unique in our database we took into account the number of songs written by
the artists. Plotting the boxplot it's appreciable a light relation between the two variable.
Artists whose name is unique tend to write less songs than artist whose name is repeated.
'''