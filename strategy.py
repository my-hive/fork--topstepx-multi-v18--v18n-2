"""v18n-2 experiment 251.
FAMILY: gold_january_physical_restocking_demand
Mechanism: January physical restocking supports gold through US cash-session liquidity.
Hypothesis: long GC 08:30-15:00 in January; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_january_physical_restocking_demand";PARAMS={"month":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mon[ix[0]]!=1 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-2.5:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
