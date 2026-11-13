"""v18n-2 experiment 121.
FAMILY: equity_quarterend_lunch_execution
Mechanism: quarter-end allocator execution produces broad midday index repricing that continues
as closing benchmark demand arrives.
Hypothesis: trade ES quarter-end-session 11:00-15:00 in completed 10:00-11:00 direction; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="equity_quarterend_lunch_execution";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel:return ans
 d=panel['ES'];out=ans['ES'];c,t=d.close.to_numpy();dt=pd.to_datetime(d.session);qend=(dt.dt.month.isin([3,6,9,12]) & (dt.dt.day>=25)).to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if not qend[ix[0]]:continue
  pre=[i for i in ix if 36000<=t[i]<39600];bars=[i for i in ix if 39660<=t[i]<54000]
  if len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
