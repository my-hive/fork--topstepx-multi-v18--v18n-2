"""v18n-2 experiment 199.
FAMILY: copper_monday_prior_us_inventory_reversal
Mechanism: Friday US copper inventory-risk hedges unwind during Monday Asia when weekend physical
inventory uncertainty is resolved.
Hypothesis: fade prior completed US-session HG direction Monday 00:00-08:30; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="copper_monday_prior_us_inventory_reversal";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];out=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();prev=0.
 for ix in d.groupby('session',sort=False).indices.values():
  us=[i for i in ix if 30600<=t[i]<54000];bars=[i for i in ix if t[i]<30600];side=-np.sign(prev)
  if dow[ix[0]]==0 and side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.01:break
    out[i]=side
  if len(us)>1:prev=c[us[-1]]-c[us[0]]
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HG' else 0.) for s,d in panel.items()}
