"""v18n-2 experiment 127.
FAMILY: crude_midmorning_hedging_continuation
Mechanism: exceptional 09:30-10:30 crude repricing reveals inventory/refinery hedging demand;
flow persists into settlement as producers and refiners complete execution.
Hypothesis: follow CL causal trailing-60-session top-quintile midmorning move, 10:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_midmorning_hedging_continuation";PARAMS={"lookback_sessions":60,"quantile":.80,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 34200<=t[i]<37800];bars=[i for i in ix if 37860<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.80) if len(hist)>=60 else np.inf
   if abs(move)>=th and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-.25:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
