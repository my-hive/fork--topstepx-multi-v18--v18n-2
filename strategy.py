"""v18n-2 experiment 128.
FAMILY: silver_lateafternoon_settlement_continuation
Mechanism: exceptional 12:00-13:00 silver repricing represents hedging flow that continues into
COMEX settlement as participants complete execution.
Hypothesis: follow causal trailing-60-session top-decile move, 13:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_lateafternoon_settlement_continuation";PARAMS={"lookback_sessions":60,"quantile":.90,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 43200<=t[i]<46800];bars=[i for i in ix if 46860<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.90) if len(hist)>=60 else np.inf
   if abs(move)>=th and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-.5:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
