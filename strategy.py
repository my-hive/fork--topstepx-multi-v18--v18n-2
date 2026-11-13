"""v18n-2 experiment 214.
FAMILY: gold_november_wednesday_physical_liquidity_reversal
Mechanism: November midweek physical-demand hedges fade through COMEX as post-allocation
liquidity normalizes.
Hypothesis: short GC 08:30-15:00 every November Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_november_wednesday_physical_liquidity_reversal";PARAMS={"month":11,"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);mo=dt.dt.month.to_numpy();wd=dt.dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mo[ix[0]]!=11 or wd[ix[0]]!=2 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-2.5:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
