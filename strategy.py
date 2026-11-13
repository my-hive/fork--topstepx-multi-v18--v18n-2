"""v18n-2 experiment 156.
FAMILY: gold_september_post_monsoon_physical_demand
Mechanism: post-monsoon Indian wedding-season physical demand supports gold after September reopen.
Hypothesis: long GC September sessions from 17:00 through 15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_september_post_monsoon_physical_demand";PARAMS={"month":9,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();month=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if month[ix[0]]!=9:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-2.5:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
