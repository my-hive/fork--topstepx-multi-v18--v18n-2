"""v18n-2 experiment 186.
FAMILY: gasoline_monday_cashopen_inventory_continuation
Mechanism: Monday 10:00-11:00 RBOB inventory/retail hedging is absorbed and continues through
US afternoon physical-market execution.
Hypothesis: follow RB 10:00-11:00 direction 11:00-15:00 Monday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_monday_cashopen_inventory_continuation";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 36000<=t[i]<39600];bars=[i for i in ix if 39600<=t[i]<54000]
  if dow[ix[0]]!=0 or len(x)<2 or not bars:continue
  side=np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.006:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
