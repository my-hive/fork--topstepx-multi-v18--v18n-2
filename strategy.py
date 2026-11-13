"""v18n-2 experiment 223.
FAMILY: gold_wednesday_opening_to_close_physical_continuation
Mechanism: Wednesday COMEX physical-demand hedge orders revealed at open continue into closing
liquidity.
Hypothesis: follow completed 08:30-09:30 GC direction during 14:00-15:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_wednesday_opening_to_close_physical_continuation";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 30600<=t[i]<34200];bars=[i for i in ix if 50400<=t[i]<54000]
  if dow[ix[0]]!=2 or len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-2.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
