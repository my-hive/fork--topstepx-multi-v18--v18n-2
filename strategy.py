"""v18n-2 experiment 191.
FAMILY: gasoline_april_drivingseason_inventory_demand
Mechanism: April driving-season inventory demand supports RBOB across US sessions.
Hypothesis: long RB April 17:00-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_april_drivingseason_inventory_demand";PARAMS={"month":4,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mo=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if mo[ix[0]]!=4:continue
  bars=[i for i in ix if t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-.006:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
