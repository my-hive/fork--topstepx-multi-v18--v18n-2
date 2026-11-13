"""v18n-2 experiment 210.
FAMILY: ultrabond_monday_prior_friday_duration_reversal
Mechanism: Friday duration-risk hedges are unwound over Monday's reopening as weekend macro
uncertainty resolves.
Hypothesis: fade completed prior Friday US UB direction Monday through 15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_monday_prior_friday_duration_reversal";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy();prev=0.
 for ix in d.groupby('session',sort=False).indices.values():
  us=[i for i in ix if 30600<=t[i]<54000];bars=[i for i in ix if t[i]<54000];side=-np.sign(prev)
  if dow[ix[0]]==0 and side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
  if len(us)>1:prev=c[us[-1]]-c[us[0]]
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
