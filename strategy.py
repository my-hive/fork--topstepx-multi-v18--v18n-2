"""v18n-2 experiment 255.
FAMILY: cattle_june_grilling_demand_continuation
Mechanism: June grilling-season processor demand supports live cattle through US cash liquidity.
Hypothesis: long LE 10:00-15:00 in June; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="cattle_june_grilling_demand_continuation";PARAMS={"month":6,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'LE' not in panel:return ans
 d=panel['LE'];out=ans['LE'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 36000<=t[i]<54000]
  if mon[ix[0]]!=6 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-.5:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='LE' else 0.) for s,d in panel.items()}
