"""v18n-2 experiment 201.
FAMILY: ultrabond_thirdweek_monday_duration_reversal
Mechanism: third-week Monday Treasury duration allocations reverse after coupon-cycle dealer hedging.
Hypothesis: short UB Monday calendar week three, 08:30-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_thirdweek_monday_duration_reversal";PARAMS={"calendar_week":3,"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy();week=((dt.dt.day.to_numpy()-1)//7)+1
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if dow[ix[0]]!=0 or week[ix[0]]!=3 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-.5:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
