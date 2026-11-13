"""v18n-2 experiment 258.
FAMILY: nasdaq_january_opening_newyear_rebalance_continuation
Mechanism: January new-year institutional allocation reinforces opening NQ order flow.
Hypothesis: follow NQ 08:30-10:00 direction through 15:00 in January; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_january_opening_newyear_rebalance_continuation";PARAMS={"month":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];out=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  sig=[i for i in ix if 30600<=t[i]<36000];bars=[i for i in ix if 36000<=t[i]<54000]
  if mon[ix[0]]!=1 or not sig or not bars:continue
  side=1 if c[sig[-1]]>=c[sig[0]] else -1;ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-12.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
