"""v18n-2 experiment 163.
FAMILY: gold_january_february_physical_restocking_momentum
Mechanism: early-year Asian jewelry and reserve restocking sustains gold trend following through
January-February sessions.
Hypothesis: follow completed 5-session GC direction in Jan-Feb, 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_january_february_physical_restocking_momentum";PARAMS={"lookback_sessions":5,"months":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mo=pd.to_datetime(d.session).dt.month.to_numpy();moves=[]
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  side=np.sign(sum(moves[-5:])) if len(moves)>=5 and mo[ix[0]]<=2 else 0
  if bars and side:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-2.5:break
    out[i]=side
  if len(bars)>1:moves.append(c[bars[-1]]-c[bars[0]])
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
