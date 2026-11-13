"""v18n-2 experiment 213.
FAMILY: longbond_thirdcycle_friday_duration_demand
Mechanism: third four-week-cycle Friday duration allocation demand supports long bonds into the
weekend after dealer hedge-book reconciliation.
Hypothesis: long ZB 08:30-15:00 Friday where ISO week modulo four equals two; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="longbond_thirdcycle_friday_duration_demand";PARAMS={"week_cycle":4,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel:return ans
 d=panel['ZB'];out=ans['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy();week=dt.dt.isocalendar().week.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if dow[ix[0]]!=4 or week[ix[0]]%4!=2 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-.25:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZB' else 0.) for s,d in panel.items()}
