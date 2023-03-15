# 6239
# 6792
# In these two games both teams have 0 shots on target,

special = [6239,6792]
import pandas as pd
import sys
if "convert" not in sys.path:
    #!!!path needs to change per user!!!
    sys.path.insert(0,"convert")
url = pd.read_csv("data/match.csv")["url"]

r5, r6 = ["Saves", "Saves"],["0 of 0 — %", "% — 0 of 0"]

for i in special:
    a = pd.read_html(url[i])
    a[2].loc[4.3] = r5  # adding a row
    a[2].loc[4.4] = r6
    convert_outcome(a[2].sort_index().reset_index(drop=True)).to_csv("data/outcome/"+ str(i)+".csv")