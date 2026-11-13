"""v18n-2 experiment 117.
FAMILY: russell_extreme_lunch_shock_continuation
Mechanism: exceptional lunch-hour small-cap futures repricing signals institutional risk transfer
that continues into closing liquidity.
Hypothesis: follow causal trailing-120-session top-5% 11:00-12:00 RTY move, 12:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="russell_extreme_lunch_shock_continuation";PARAMS={"lookback_sessions":120,"quantile":.95,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RTY' not in panel:return ans
 d=panel['RTY'];out=ans['RTY'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 39600<=t[i]<43200];bars=[i for i in ix if 43260<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];threshold=np.quantile(np.abs(hist[-120:]),.95) if len(hist)>=120 else np.inf
   if abs(move)>=threshold and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-5:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RTY' else 0.) for s,d in panel.items()}
