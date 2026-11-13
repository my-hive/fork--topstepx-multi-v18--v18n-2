"""v18n-2 experiment 112.
FAMILY: euro_extreme_us_opening_shock_continuation
Mechanism: exceptional early US euro-futures move reprices dollar liquidity and persists during
North American execution.
Hypothesis: follow causal trailing-120-session top-5% 08:30-09:30 6E move, 09:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="euro_extreme_us_opening_shock_continuation";PARAMS={"lookback_sessions":120,"quantile":.95,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6E' not in panel:return ans
 d=panel['6E'];out=ans['6E'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 30600<=t[i]<34200];bars=[i for i in ix if 34260<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];threshold=np.quantile(np.abs(hist[-120:]),.95) if len(hist)>=120 else np.inf
   if abs(move)>=threshold and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-.002:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='6E' else 0.) for s,d in panel.items()}
