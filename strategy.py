"""v18n-2 experiment 222.
FAMILY: silver_wednesday_latecomex_liquidity_reversal
Mechanism: Wednesday late-COMEX industrial silver hedge pressure reverses into settlement
liquidity as dealers flatten intraday inventory.
Hypothesis: fade 13:00-15:00 SI direction during 15:00-17:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_wednesday_latecomex_liquidity_reversal";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 46800<=t[i]<54000];bars=[i for i in ix if 54000<=t[i]<61200]
  if dow[ix[0]]!=2 or len(pre)<2 or not bars:continue
  side=-np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
