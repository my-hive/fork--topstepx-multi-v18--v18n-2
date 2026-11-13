"""v18n-2 experiment 126.
FAMILY: spx_friday_opening_imbalance_continuation
Mechanism: Friday weekly equity rebalancing produces a concentrated opening imbalance whose
same-direction institutional execution persists through the cash session.
Hypothesis: follow ES Friday top-quintile 08:30-09:00 move, 09:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="spx_friday_opening_imbalance_continuation";PARAMS={"lookback_sessions":60,"quantile":.80,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel:return ans
 d=panel['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans['ES'];hist=[];dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 30600<=t[i]<32400];bars=[i for i in ix if 32460<=t[i]<54000]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.80) if len(hist)>=60 else np.inf
   if dow[ix[0]]==4 and abs(move)>=th and bars:
    side=np.sign(move);ref=c[bars[0]]
    for i in bars:
     if side*(c[i]-ref)<=-5:break
     out[i]=side
   hist.append(move)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
