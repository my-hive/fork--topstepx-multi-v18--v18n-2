"""v18n-2 experiment 169.
FAMILY: ultrabond_cash_open_duration_shock_continuation
Mechanism: exceptional post-cash-open long-duration move reflects macro surprise and convexity
hedging that persists as cash-bond liquidity updates.
Hypothesis: follow top-quintile UB 09:30-10:00 move through 15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_cash_open_duration_shock_continuation";PARAMS={"history_sessions":60,"quantile":.8,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();vals=[]
 for ix in d.groupby('session',sort=False).indices.values():
  x=np.array([i for i in ix if 34200<=t[i]<36000]);bars=[i for i in ix if 36000<=t[i]<54000]
  r=c[x[-1]]-c[x[0]] if len(x)>1 else 0.;q=np.quantile(np.abs(vals[-60:]),.8) if len(vals)>=60 else np.inf;side=np.sign(r) if abs(r)>=q else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
  if len(x)>1:vals.append(r)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
