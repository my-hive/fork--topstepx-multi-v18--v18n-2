"""v18n-2 experiment 204.
FAMILY: gold_friday_opening_liquidity_continuation
Mechanism: Friday COMEX opening information shock attracts same-day hedging continuation through
weekly settlement.
Hypothesis: follow top-quintile causal 08:30-09:30 GC move through 15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_friday_opening_liquidity_continuation";PARAMS={"lookback":60,"quantile":.8,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 30600<=t[i]<34200];bars=[i for i in ix if 34200<=t[i]<54000]
  if len(x)<2:continue
  move=c[x[-1]]-c[x[0]];th=np.quantile(np.abs(hist[-60:]),.8) if len(hist)>=60 else np.inf;side=np.sign(move)
  if dow[ix[0]]==4 and abs(move)>=th and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-2.5:break
    out[i]=side
  hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
