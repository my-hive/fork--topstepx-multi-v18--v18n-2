"""v18n-2 experiment 122.
FAMILY: silver_afternoon_extreme_execution_continuation
Mechanism: exceptional early-afternoon COMEX silver repricing signals physical/financial hedging
flow that persists into settlement liquidity.
Hypothesis: follow causal trailing-120-session top-10% 13:00-14:00 SI move, 14:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_afternoon_extreme_execution_continuation";PARAMS={"lookback_sessions":120,"quantile":.90,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 46800<=t[i]<50400];bars=[i for i in ix if 50460<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];threshold=np.quantile(np.abs(hist[-120:]),.90) if len(hist)>=120 else np.inf
   if abs(move)>=threshold and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-.5:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
