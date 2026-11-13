"""v18n-2 experiment 119.
FAMILY: silver_morning_extreme_execution_continuation
Mechanism: exceptional COMEX opening silver repricing reflects macro/physical hedging flow that
persists while US liquidity broadens.
Hypothesis: follow causal trailing-120-session top-5% 09:30-10:00 SI move, 10:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_morning_extreme_execution_continuation";PARAMS={"lookback_sessions":120,"quantile":.95,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 34200<=t[i]<36000];bars=[i for i in ix if 36060<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];threshold=np.quantile(np.abs(hist[-120:]),.95) if len(hist)>=120 else np.inf
   if abs(move)>=threshold and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-.5:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
