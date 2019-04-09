import os      # Line 7. This module provides a portable way of using operating system dependent functionality.
from bs4 import BeautifulSoup    # Line 16. Beautiful Soup is a Python library for pulling data out of HTML and XML files.
import json
import requests

all=[]
all=list(os.listdir("lyrics_collection"))   # list of the files' names in the folder "lyrics_collection" (songs)


col=[]
for i in all:

    if i.endswith(".html"):  # not all the files were written in html format. (also php files)
        try:
            f = open("lyrics_collection/"+i ,'r', encoding="utf8")
            soup = BeautifulSoup(f, "lxml")                  # parsing the html page on python
            link = soup.find("div", { "id" : "content_h" })  # find the "div" (it's a tag) that contains which "id" is "content_h"
            lyr = (str(link)[31:-6].replace("<br/>", " "))   # take the lyrics
            if len(lyr)>0:                                   # if the lyrics is not empty
                link = soup.find("title")                    # find the title
                tit,art = str(link)[7:-8].split("Lyrics -")  # it takes title and artist
                dict={"artist": art, "title": tit, "lyrics":lyr, "url":i}   # dictionary with everything
                col.append(dict)                             #  the list of dictionaries with a dictionary for each song
        except ValueError:
            continue


#pushing firsts documents
params = {'apiKey': 'RKnHYU5eIIdsSC6h5nhwm2zck7FYFgTp'}      # our apiKey
url = 'https://api.mlab.com/api/1/databases'
response = requests.get(url, params)                         # 200 means that there is a link with the MongoDB database

print(response.status_code)
print(response.text)                                         # the names of the databases we have

dbname = 'lyricsdb'
collection = 'songs'
url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection
headers = {'content-type': 'application/json'}
data = json.dumps(col)

response = requests.post(url, data=data, params=params, headers=headers)  # post request to push the entire collection into the db
print(response.text)
