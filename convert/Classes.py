import pandas as pd
from collections import OrderedDict

namelist = OrderedDict()

class Player():
  def __init__(self, name: str, stat = None):
    self.name = name
    self.stat = stat #stat include date
    namelist [name] = self

  def add_stat(self, newstat:pd.DataFrame):
    self.stat = pd.concat([self.stat, newstat],axis=0)

if __name__ == "__main__":
  import time
  start = time.time()
  """
  iter over all downloaded csvs
    idx_match [0,9129]
    idx_tb [0,3]

    4*9129 number of tables to go through
    2 of 4 table has 13-14 lines, the other 2 mainly 1 lines, so 30 lines per match
  """
  temp=time.time()
  for idx_match in range(0,9027):
    for idx_tb in ["homestat","homegk","awaystat","awaygk"]: #we have multiple tables to extract from
      #Get Game csv
      stat = pd.read_csv("data/stat/" + str(idx_match) + "_" + str(idx_tb) + ".csv")

      #Get Date
      match =pd.read_csv("data/match.csv")
      date = match.iloc[idx_match,1]
      home, away = match.Home[idx_match], match.Away[idx_match]
      team = home if idx_tb in ["homestat","homegk"] else away
      #Go through each player in game csv
      for i,j in stat.iterrows():
        #get name and stats
        name, stat_serie = team+"_"+j["Player"], j.to_frame().transpose().loc[:,"Player":]
        #add date information(CRUCIAL!!!)
        stat_serie["Date"] = date
        stat_serie["Team"] = team
        if name not in namelist:
          a = Player(name,stat_serie)
        else:
          namelist[name].add_stat(stat_serie)

    if idx_match % 100==99:
      print(time.time()-temp, idx_match)
      temp=time.time()

  print(time.time()-start)
  len(namelist)

  #save dictionary to pkl file
  import pickle
  with open("data/namelist.pkl", "wb") as outp:
    pickle.dump(namelist, outp, pickle.HIGHEST_PROTOCOL)

  list(namelist.items())[1]