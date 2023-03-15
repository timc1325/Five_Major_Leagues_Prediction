import time
import pandas as pd
import sys
if "convert" not in sys.path:
    #!!!path needs to change per user!!!
    sys.path.insert(0,"convert")

from convert_res import *
matches = pd.read_csv("data/match.csv")

start = time.time()
temptime= time.time()
for idx in range(0,matches.shape[0]):
    step = time.time()
    temp = pd.read_html(matches["url"][idx],header=1)
    #append information on the right of match csv: team name, score, formation?
    temp1 = pd.read_html(matches["url"][idx])
    result = convert_outcome(temp1[2])
    result.to_csv("data/outcome/"+str(idx)+".csv")

    # get hometeam, away team, 
    for i in temp[3:9]:
        i.set_index(["Player","Nation","#","Pos","Age","Min"],inplace=True)
    for i in temp[10:16]:
        i.set_index(["Player","Nation","#","Pos","Age","Min"],inplace=True)
    homestat = pd.concat(temp[3:9],axis=1).drop(pd.concat(temp[3:9],axis=1).index[-1]) #-1 is for deleting the total sum row
    #extract gk row and combine with table 10
    homegk = homestat.iloc[homestat.shape[0]-1:,:]
    temp[9][["#","Pos"]]=[homestat.index[-1][2],homestat.index[-1][3]]
    temp[9].set_index(["Player","Nation","#","Pos","Age","Min"],inplace=True)
    homegk = pd.concat([homegk,temp[9]],axis=1).reset_index()

    #similar as above
    awaystat = pd.concat(temp[10:16],axis=1).drop(pd.concat(temp[10:16],axis=1).index[-1])
    awaygk = awaystat.iloc[awaystat.shape[0]-1:,:]
    temp[16][["#","Pos"]]=[awaystat.index[-1][2],awaystat.index[-1][3]]
    temp[16].set_index(["Player","Nation","#","Pos","Age","Min"],inplace=True)
    awaygk = pd.concat([awaygk,temp[16]],axis=1).reset_index()

    #get rid of gk
    awaystat = awaystat.drop(awaystat.index[-1]).reset_index()
    homestat = homestat.drop(homestat.index[-1]).reset_index()

    #local save 
    homestat.to_csv("data/stat/"+str(idx)+"_homestat.csv")
    awaystat.to_csv("data/stat/"+str(idx)+"_awaystat.csv")
    homegk.to_csv("data/stat/"+str(idx)+"_homegk.csv")
    awaygk.to_csv("data/stat/"+str(idx)+"_awaygk.csv")
        
    print(time.time() -step,"     ",time.time() - start, idx)

    if idx % 20 == 19:
        sleepneed = 90
        
        print("Now Sleeping for ",sleepneed," seconds zZZ...")
        time.sleep(sleepneed)
        temptime = time.time()