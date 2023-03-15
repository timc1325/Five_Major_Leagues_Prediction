
import pandas as pd

matches = pd.read_csv("data/url.csv")
matches.columns=pd.Index(["id", 'Home', 'Score', 'Away', 'url'])

temp = matches.url.str.split("/",expand=True)[6].str.split("-",expand=True)
mask = temp.iloc[:,-5:].isna().sum(axis=1)

for i in range(temp.shape[0]):
  temp.iloc[i,0:] = temp.iloc[i,0:].shift(mask[i],axis=0)
temp[temp[11]=="Bundesliga"] = temp[temp[11]=="Bundesliga"].shift(-1,axis=1)
league_name =temp.iloc[:,10]+" "+temp.iloc[:,11].fillna("")
date = pd.to_datetime(temp.iloc[:,7]+"-"+temp.iloc[:,8]+"-"+temp.iloc[:,9])
matches["League"]= league_name.str.strip()
matches["Date"] = date
matches = matches.drop("id",axis=1)
matches = matches[matches.columns[::-1]]
cols = matches.columns.tolist()
cols = ['Date', 'League', 'Home', 'Score', 'Away', 'url']
matches=matches[cols]
matches.to_csv("data/match.csv")