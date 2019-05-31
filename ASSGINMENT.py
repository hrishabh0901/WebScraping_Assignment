#!/usr/bin/env python
# coding: utf-8

# ## Assignment

# ### Number of Task :: 3
# ####  1. A list of all cricket players who have ever played ODI matches
# ####  2. Runs they have made every year in their career
# ####  3. Cummulify the scores by year for each player
# 
# 
# 

# ##### **Note :: All the data are fetched from http://howstat.com

#  

# ### TASK 1

# #### Importing all the Library

# In[ ]:


import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import numpy as np


# <p> The below cell extracts all the playerid and in the next segment while fetching the runs we will fetch the names, as the present url from which the playerid is fetched does not contain the full name. <br> Function "find_odi_player" is defined which takes an href tag and checks whether that particular link starts with  "PlayerOverview_ODI.asp?PlayerID=" if its True that means that particular player has played atleast one ODI <br> soup.find_all(href=find_odi_player) returns list of tags which is then passed through the lambda function to extract the playerid and store it in List_Of_Player<p>

# In[ ]:


List_Of_Player = []
for group in range(65,67):
    url = f'http://howstat.com/cricket/Statistics/Players/PlayerList.asp?Country=ALL&Group={chr(group)}'
    source = requests.get(url).text
    soup = BeautifulSoup(source,'lxml')
    def find_odi_player(href):
        return True if href and href.startswith('PlayerOverview_ODI.asp?PlayerID=') else False
    List_Of_Player += list(map(lambda x: x['href'].split('=')[1] , soup.find_all(href=find_odi_player))) 


# ### Task 2

# <p> The below code defines "d" which is of type dictionary and is going to store data for each player, the keys are Name and years from (1971-2019). Assume this as a matrix because this will be converted into dataframe in the end, I could have taken directly a matrix but for my convenience I did with dict()
# <p>

# In[ ]:


XLen = len(List_Of_Player)
d = dict()
d['Name'] = [None]*XLen
d['Country'] = [None]*XLen
for i in range(1971,2020):
    d[str(i)] = [0]*XLen


# In[ ]:


df


# <p>
# The for-loop takes up each playerid from "List_Of_Player" and the appends it, to get the final url and using request and bs4 the the HTML is parsed.<br>
# The HTML contains details about every innings played by particular player which is fetched into "tables" using appropriate filter.<br>
# name : The Full Name of the Player<br>
# country : Country of the player<br>
# Then the entire table is traversed and the year of that inning and run scored is extracted, the edge-case were runs are appended with asterisk is also handled.<br>
# Lastly run is added "d[year][playerid] += run", which adds to previously scored runs of that playerid in that year.
# <p>
# <h6>**Note : I did not run the entire List_Of_Player(2547) together instead I used batches of 300 playerid<h6>

# In[ ]:


for playerid in range(0,XLen):
    if playerid%10 == 0:
        print(playerid)
    url = f'http://howstat.com/cricket/Statistics/Players/PlayerProgressBat_ODI.asp?PlayerID={List_Of_Player[playerid]}'
    source = requests.get(url).text
    soup = BeautifulSoup(source,'lxml')
    tables = soup.find_all('tr',bgcolor=re.compile('^#'))
    name = soup.find('td',class_='Banner2').text.strip().split("(")[0]
    country = re.findall(r"[\w']+", soup.find('td',class_='Banner2').text.strip())[-4]
    for row in tables:
        year = row.find('a').text.split("/")[-1]
        d['Name'][playerid] = name
        d['Country'][playerid] = country
        run = 0
        try:
            if row.find('td',class_="AsteriskSpace"):
                k = row.find('td',class_="AsteriskSpace").text.strip()
                if k != '-':
                    run = int(k)
            else:
                run = int(row.find('td',align="right").text.strip()[:-1])
        except:
            run = 0
        d[year][playerid] += run


# #### Converting dictionary into dataframe

# In[ ]:


df = pd.DataFrame(d) 


# #### Storing the dataframe into file

# In[ ]:


df.to_csv('player.csv', sep=',', encoding='utf-8')


# ### Task 3

# <p> Final task was to calculate the cumulative score, so I ran loop from 1972 and added current column data
# with previous column<p>

# In[ ]:


for i in range(1972,2020):
    df[str(i)] += df[str(i-1)]

