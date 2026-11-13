"""v18n-2 experiment 252.
FAMILY: euro_june_corporate_repatriation_demand
Mechanism: June half-year corporate repatriation supports euro futures during US cash liquidity.
Hypothesis: long 6E 08:30-15:00 in June; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="euro_june_corporate_repatriation_demand";PARAMS={"month":6,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6E' not in panel:return ans
 d=panel['6E'];out=ans['6E'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mon[ix[0]]!=6 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-.002:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='6E' else 0.) for s,d in panel.items()}
