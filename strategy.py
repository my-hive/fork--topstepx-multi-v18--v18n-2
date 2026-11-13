"""v18n-2 experiment 203.
FAMILY: heatingoil_october_prior_us_refinery_hedge_continuation
Mechanism: October heating-oil seasonal hedge demand carries prior US refinery positioning into
Asian electronic trade ahead of winter supply allocations.
Hypothesis: follow completed prior US direction during October Asia 00:00-08:30; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="heatingoil_october_prior_us_refinery_hedge_continuation";PARAMS={"month":10,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HO' not in panel:return ans
 d=panel['HO'];out=ans['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();month=pd.to_datetime(d.session).dt.month.to_numpy();prev=0.
 for ix in d.groupby('session',sort=False).indices.values():
  us=[i for i in ix if 30600<=t[i]<54000];bars=[i for i in ix if t[i]<30600];side=np.sign(prev)
  if month[ix[0]]==10 and side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.006:break
    out[i]=side
  if len(us)>1:prev=c[us[-1]]-c[us[0]]
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HO' else 0.) for s,d in panel.items()}
