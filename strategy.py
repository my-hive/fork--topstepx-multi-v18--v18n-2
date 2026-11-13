"""v18n-2 experiment 151.
FAMILY: spx_friday_gamma_pin_reversal
Mechanism: dealer hedging around weekly option expiry dampens an exceptional morning index move as
liquidity concentrates near the close.
Hypothesis: fade ES top-decile 09:30-12:00 Friday move from 12:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="spx_friday_gamma_pin_reversal";PARAMS={"lookback_sessions":60,"quantile":.9,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel:return ans
 d=panel['ES'];out=ans['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();hist=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 34200<=t[i]<43200]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.9) if len(hist)>=60 else np.inf;hist.append(move)
   if dow[ix[0]]!=4 or abs(move)<th:continue
   side=-np.sign(move);bars=[i for i in ix if 43260<=t[i]<54000]
   if not bars:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-5.:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
