"""v18n-2 experiment 129.
FAMILY: gasoline_opening_inventory_reversal
Mechanism: extreme 09:00-09:30 RBOB repricing reflects transient pre-release liquidity imbalance;
refinery/inventory hedgers fade it into US afternoon settlement.
Hypothesis: fade causal trailing-60-session top-30% 09:00-09:30 RB move, 09:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_opening_inventory_reversal";PARAMS={"lookback_sessions":60,"quantile":.70,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 32400<=t[i]<34200];bars=[i for i in ix if 34260<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.70) if len(hist)>=60 else np.inf
   if abs(move)>=th and bars:
    side=-np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-.006:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
