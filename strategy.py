"""v18n-2 experiment 230.
FAMILY: treasury_wednesday_midday_auction_duration_continuation
Mechanism: Wednesday Treasury auction concession and dealer duration transfer revealed before
midday persist through cash-session hedge execution.
Hypothesis: follow 10:00-11:00 ZB direction 11:00-15:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="treasury_wednesday_midday_auction_duration_continuation";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel:return ans
 d=panel['ZB'];out=ans['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 36000<=t[i]<39600];bars=[i for i in ix if 39600<=t[i]<54000]
  if dow[ix[0]]!=2 or len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZB' else 0.) for s,d in panel.items()}
