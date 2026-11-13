"""v18n-2 experiment 140.
FAMILY: crude_turnmonth_refinery_roll_demand
Mechanism: refinery hedge rolling and index rebalancing around calendar month boundary create
persistent crude demand across adjacent business sessions.
Hypothesis: long CL in last two/first two calendar days, 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_turnmonth_refinery_roll_demand";PARAMS={"boundary_calendar_days":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dates=pd.to_datetime(d.session)
 active=((dates.dt.day<=2)|(dates.dt.day>=dates.dt.days_in_month-1)).to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if not active[ix[0]]:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if c[i]-ref<=-.25:stopped=True
   else:out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
