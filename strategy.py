"""v18n-2 experiment 145.
FAMILY: ultrabond_firstweek_duration_suppression
Mechanism: early-month duration supply and dealer balance-sheet normalization suppress ultra-bond
prices after monthly allocation reset.
Hypothesis: short UB calendar week 1, 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_firstweek_duration_suppression";PARAMS={"calendar_week":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dates=pd.to_datetime(d.session);week=((dates.dt.day-1)//7+1).to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if week[ix[0]]!=1:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if ref-c[i]<=-.5:stopped=True
   else:out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
