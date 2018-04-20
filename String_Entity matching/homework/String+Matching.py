
# coding: utf-8

# In[2]:


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import string


# In[3]:


def editdist(s1, s2):
    c = len(s1) + 1
    r = len(s2) + 1
    # initialize matrix
    M = [[0 for x in range(c)] for y in range(r)]
    for i in range(0,c):
        M[0][i] = i
    for j in range(0,r):
        M[j][0] = j
    # dynamic programming
    for i in range(1,r):
        for j in range(1,c):
            if s1[j-1] == s2[i-1]:
                M[i][j] = M[i-1][j-1]
            else:
                M[i][j] = min(M[i-1][j-1], M[i-1][j], M[i][j-1]) + 1

    
    return M[r-1][c-1]


# In[4]:


fodors_raw = list()
with open("fodors.csv", "r") as f:
    i = 0
    for line in f.readlines():
        fodors_raw.append(line.split(","))
        
        if len(line.split(",")) != 3:
            print str(i) + "---" + line
        i += 1


# In[5]:


# clean data
fodors_raw[15] = [fodors_raw[15][0], fodors_raw[15][1].split(". ")[0], "\"" + fodors_raw[15][1].split(". ")[1]]
fodors_raw[23] = [fodors_raw[23][0], fodors_raw[23][1].split("DIVE ")[0]+ "3483\"", "\"" + fodors_raw[23][1].split("DIVE ")[1]]
tmp = len(fodors_raw) - 1
for i in [229, 277, 333,506]:
    fodors_raw.append([fodors_raw[i][0],fodors_raw[i][3],fodors_raw[i][4]])
    fodors_raw[i] = [fodors_raw[i][0],fodors_raw[i][1],fodors_raw[i][4]]

mfodors = {tmp : 228, tmp +1 : 276, tmp + 2 : 332, tmp + 3 : 505}


# In[6]:


zagats_raw = list()
with open("zagats.csv", "r") as f1:
    i=0
    for line in f1.readlines():
        zagats_raw.append(line.split(","))
        if len(line.split(",")) != 3:
            print str(i) + "---" + line
        i += 1


# In[7]:


zagats_raw[236] = [zagats_raw[236][0][:-13], zagats_raw[236][0][-13:-1], zagats_raw[236][1]]
zagats_raw[245] = [zagats_raw[245][0], zagats_raw[245][1][0:14], zagats_raw[245][1][14:]]
zagats_raw[276] = [zagats_raw[276][0]+ zagats_raw[276][1], zagats_raw[276][2], zagats_raw[276][3]]


# In[8]:


# remove header
fodors = fodors_raw[1:]
zagats = zagats_raw[1:]
len(fodors)


# In[10]:


# initialize distance matrix
c = len(zagats)
r = len(fodors)
# addrDist = [[0 for x in range(c)] for y in range(r)]  # 533 * 331
telDist = np.zeros((len(fodors), len(zagats)))
# compare input and get edit distance
for i in range(0, r):
    for j in range(0, c):
#         addrDist[i][j] += editdist(fodors[i][0], zagats[j][0])
        telDist[i][j] += editdist(fodors[i][1].translate(None, string.punctuation), zagats[j][1].translate(None, string.punctuation))
#         cuiDist[i][j] += editdist(fodors[i][2], zagats[j][2])


# In[12]:


np.histogram(telDist)


# In[13]:


unique, counts = np.unique(telDist, return_counts=True)
dict(zip(unique, counts))


# In[14]:


cand = np.where(telDist <=1)


# In[15]:


cand


# In[16]:


# map back the indexes
for i in cand[0][cand[0]>= tmp]:
    cand[0][cand[0]>= tmp] = mfodors[i]


# In[17]:


# calculate edit dist for addr and cuisine
addrDist = []
cuiDist = []
for i in range(len(cand[0])):
    str1 = fodors[cand[0][i]][0].translate(None, string.punctuation)
    str2 = zagats[cand[1][i]][0].translate(None, string.punctuation)
    
    add = editdist(str1, str2) *1.0 / min(len(str1),len(str2))
    
    addrDist.append(add)
    if add >= 0.95: 
        print "Big dist in addr--------"
        print str1
        print str2
    
    cstr1 = fodors[cand[0][i]][2]
    cstr2 = zagats[cand[1][i]][2]
    cui = editdist(cstr1, cstr2)
    if cui >= 21:
        print "Big dist in cui--------"
        print str1
        print str2
    cuiDist.append(cui)


# In[18]:


# looks like using edit dist on cuisine is bad, therefore use normalized edit dist on addr only
np.histogram(addrDist)


# In[19]:


# filter out those cands with addr dist more than 0.95
with open ("output.txt","w") as out:
    for i in range(len(addrDist)):
        if addrDist[i] < 0.95:
            out.write("zagats.csv:" + str(cand[1][i]) + "\t" + "fodors.csv:" + str(cand[0][i]) + "\n")

        

