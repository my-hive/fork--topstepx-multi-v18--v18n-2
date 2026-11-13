"""v18n-2 experiment 149.
FAMILY: naturalgas_monthstart_utility_supply
Mechanism: utilities renew prompt-month physical hedges after the calendar reset, adding early-month
natural-gas supply pressure before US close.
Hypothesis: short NG first three calendar sessions, 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="naturalgas_monthstart_utility_supply";PARAMS={"calendar_days":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NG' not in panel:return ans
 d=panel['NG'];out=ans['NG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dates=pd.to_datetime(d.session);day=dates.dt.day.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if day[ix[0]]>3:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if ref-c[i]<=-.025:stopped=True
   else:out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NG' else 0.) for s,d in panel.items()}
