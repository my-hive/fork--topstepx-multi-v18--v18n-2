"""v18n-2 experiment 225.
FAMILY: gasoline_wednesday_midmorning_inventory_continuation
Mechanism: Wednesday midmorning gasoline inventory hedges continue as physical market liquidity
absorbs the same directional order flow into settlement.
Hypothesis: follow 09:00-10:00 RB direction 10:00-15:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_wednesday_midmorning_inventory_continuation";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 32400<=t[i]<36000];bars=[i for i in ix if 36000<=t[i]<54000]
  if dow[ix[0]]!=2 or len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.006:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
