"""v18n-2 experiment 229.
FAMILY: nasdaq_october_opening_earnings_positioning_continuation
Mechanism: October earnings-season index hedging at US open continues as dealer inventory is
unwound across liquid cash hours.
Hypothesis: follow 08:30-10:00 NQ direction 10:00-15:00 in October; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_october_opening_earnings_positioning_continuation";PARAMS={"month":10,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];out=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);mon=dt.dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 30600<=t[i]<36000];bars=[i for i in ix if 36000<=t[i]<54000]
  if mon[ix[0]]!=10 or len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-12.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
