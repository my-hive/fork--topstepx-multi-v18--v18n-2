"""v18n-2 experiment 137.
FAMILY: longbond_midmorning_duration_execution_continuation
Mechanism: broad US macro-execution duration demand persists through the bond session as dealer
risk transfer and institutional hedging unwind gradually.
Hypothesis: follow ZB after causal top-40% 09:30-10:30 move, 10:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="longbond_midmorning_duration_execution_continuation";PARAMS={"lookback_sessions":60,"quantile":.60,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel:return ans
 d=panel['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[];out=ans['ZB']
 for day,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 34200<=t[i]<37800];bars=[i for i in ix if 37860<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.60) if len(hist)>=60 else np.inf;hist.append(move)
   if abs(move)<th or not bars:continue
   side=np.sign(move);ref=c[bars[0]];stopped=False
   for i in bars:
    if stopped:continue
    if side*(c[i]-ref)<=-.25:stopped=True
    else:out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZB' else 0.) for s,d in panel.items()}
