"""v18n-2 experiment 157.
FAMILY: naturalgas_earlymonth_utility_balancing
Mechanism: early-month utility balancing after billing-cycle demand forecasts supplies natural-gas
futures, producing a short bias through the US session.
Hypothesis: short NG on calendar days 1-6, 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="naturalgas_earlymonth_utility_balancing";PARAMS={"calendar_days":6,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NG' not in panel:return ans
 d=panel['NG'];out=ans['NG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();day=pd.to_datetime(d.session).dt.day.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if day[ix[0]]>6:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-.025:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NG' else 0.) for s,d in panel.items()}
