import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import networkx as nx
import heapq
import numpy as np


# Jaccard's Similarity:
def jaccardSim(data1, data2):
    myList1 = []
    for item in data1:
        key = list(item.keys())[0]
        myList1.append(key)

    myList2 = []
    for item in data2:
        key = list(item.keys())[0]
        myList2.append(key)

    intersect = len(set(myList1).intersection(myList2))
    similarityScore = (intersect / ((len(myList1) + len(myList2)) - intersect))

    return similarityScore


#Shortest path function
def Shortest_path(G, start, end):
    if start == end:
        result = 0
    elif nx.has_path(G, start, end):
        neighb = []
        seen = set()
        lis = G[start]
        seen.add(start)
        for i in lis:
            heapq.heappush(neighb, (lis[i]['weight'], i))
        while neighb:
            min_neighb = heapq.heappop(neighb)
            weight = min_neighb[0]
            node = min_neighb[1]
            seen.add(node)
            if node == end:
                return weight
            node_neighb = G[node]
            for j in node_neighb:
                if j not in seen:
                    is_in_neighb = False
                    for i in neighb:
                        if i[1] == j:
                            min_dist = min(i[0], node_neighb[j]['weight'] + weight)
                            is_in_neighb = True
                            neighb.remove(i)
                            heapq.heappush(neighb, (min_dist, j))
                            break
                    if is_in_neighb == False:
                        heapq.heappush(neighb, (node_neighb[j]['weight'] + weight, j))
    else:
        result = float('inf')
    return result


def GN_funct(G, t):
    dic = {}
    for i in G.nodes():
        lst = []
        for j in t:
            if i != j:
                d = Shortest_path(G, i, j)
                if d != float('inf'):
                    lst.append((d, j))
        try:
            min_dist = heapq.heappop(lst)
            dic[i] = min_dist
        except:
            dic[i] = "NaN"

    return dic


datab = input("Choose the database:")

if datab == "reduced":
    f = open('reduced_dblp.json', 'r')
    data = f.read()
    f.close()
if datab == "full":
    f = open('full_dblp.json', 'r')
    data = f.read()
    f.close()

#reading data from json file
dataset = json.loads(data)
type(dataset)

#Creating myDict:
myDict={}
for dic in range(len(dataset)):
    myList=[]
    confID=dataset[dic]['id_conference_int']
    pubID=dataset[dic]['id_publication_int']
    for j in range(len(dataset[dic]['authors'])):
        authorID=(dataset[dic]['authors'][j]['author_id'])
        myList=[{pubID:confID}]
        if authorID not in myDict:
            myDict[authorID]=myList            
        else:
            myDict[authorID].append({pubID:confID})
            

        
#Creating Graph:
G=nx.Graph()

for data in dataset:
    for author in data["authors"]:
        for author2 in data["authors"]:
            G.add_node(author["author_id"])
            G.add_node(author2["author_id"])
            if (author["author_id"] != author2["author_id"]) and (not((G.has_edge(author["author_id"],author2["author_id"])))):
                edgeWeight= 1-jaccardSim(myDict[author["author_id"]],myDict[author2["author_id"]])
                G.add_edge(author["author_id"],author2["author_id"], weight=edgeWeight)

print(nx.info(G))
'''
#Plotting the graph:
plt.figure(figsize=(15, 10))
plt.clf()

options = {
    'node_color': 'black',
    'node_size': 5,
    'edge_color': 'red',
    'linewidths': 0.1,
    'width': 0.5,
}
nx.draw(G, **options)
plt.show()
'''

a = input("enter the number of the exercise you want to run:")

if a == "2a":
    #Getting subgraph of conferences:
    Conferences = {}
    for book in dataset:
        confID = book['id_conference_int']
        for author in book['authors']:
            authorID = author['author_id']
            if confID not in Conferences.keys():
                Conferences[confID] = []
            else:
                Conferences[confID].append(authorID)
    print(Conferences.keys())
        
    confID = int(input("Search confID:"))      
    nodeList = []
    for k,v in myDict.items():
        for j in range(len(v)):
            if(list(v[j].values())[0]==confID):
                nodeList.append(k)
    
    H = G.subgraph(nodeList)
    plt.figure(figsize=(20, 8))
    plt.clf()
    nx.draw(H)
    plt.show()
    
    #Getting centrality:
    degree_centrality = nx.algorithms.centrality.degree_centrality(H)
    closeness_centrality = nx.algorithms.centrality.closeness_centrality(H)
    betweenness_centrality = nx.algorithms.centrality.betweenness_centrality(H)
    #print (degree_centrality, closeness_centrality, betweenness_centrality)

    degree_dict={}
    for key, values in degree_centrality.items():
        if values not in degree_dict.keys():        
            degree_dict[values]=1
        else:
            degree_dict[values]+=1 

    x = np.arange(len(degree_dict))
    y = [i for i in degree_dict.values()]
    plt.figure(figsize=(20, 8))
    plt.bar(x, y)
    plt.title('Degree Centrality',fontsize=20)
    plt.xticks(x, sorted(("%.4f" % a for a in degree_dict.keys())),rotation=90)
    plt.show()
    
    closeness_dict={}
    for key, values in closeness_centrality.items():
        if values not in closeness_dict.keys():        
            closeness_dict[values]=1
        else:
            closeness_dict[values]+=1 
    
    x = np.arange(len(degree_dict))
    y = [i for i in degree_dict.values()]
    plt.figure(figsize=(20, 8))
    plt.bar(x, y)
    plt.title('Closeness Centrality',fontsize=20)
    plt.xticks(x, sorted(("%.4f" % a for a in degree_dict.keys())),rotation=90)
    plt.show()
    
    betweenness_dict={}
    for key, values in betweenness_centrality.items():
        if values not in betweenness_dict.keys():        
            betweenness_dict[values]=1
        else:
            betweenness_dict[values]+=1
    
    x = np.arange(len(betweenness_dict))
    y = [i for i in betweenness_dict.values()]
    plt.figure(figsize=(20, 8))
    plt.bar(x, y)
    plt.title('Betweenness Centrality',fontsize=20)
    plt.xticks(x, sorted(("%.7f" % a for a in betweenness_dict.keys())),rotation=90)
    plt.show()
      
elif a == "2b":
    searchauthorID = int(input("Search authorID: "))
    hopDistance=int(input("Enter Hop Distance: "))
    
    test=nx.ego_graph(G, searchauthorID, radius=hopDistance,center=True) 
    plt.figure(figsize=(20, 8))
    plt.clf()
    nx.draw(test)
    plt.show()
   
elif a == "3a":

    author = int(input("Search the authorID to calculate the shortest path with Aris: "))
    print(Shortest_path(G,256176, author))

elif a == "3b":
    #t = [9503, 255902, 9070, 239007, 189237]
    t = list(map(int,input("insert a list of authors' ID").split()))
    print(GN_funct(G, t))


else:
    print("Invalid input")
























