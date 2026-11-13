"""v18n-2 experiment 197.
FAMILY: gold_tuesday_latecomex_liquidity_reversal
Mechanism: Tuesday late COMEX gold execution overshoots before settlement and reverses as dealer
liquidity returns.
Hypothesis: fade GC 13:00-14:00 direction 14:00-16:00 Tuesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_tuesday_latecomex_liquidity_reversal";PARAMS={"weekday":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 46800<=t[i]<50400];bars=[i for i in ix if 50400<=t[i]<57600]
  if dow[ix[0]]!=1 or len(x)<2 or not bars:continue
  side=-np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-2.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
