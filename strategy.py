"""v18n-2 experiment 215.
FAMILY: ultrabond_october_thursday_supply_pressure
Mechanism: October Thursday long-duration supply and hedge pressure weighs on ultra bonds through the US session.
Hypothesis: short UB 08:30-15:00 every October Thursday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_october_thursday_supply_pressure";PARAMS={"month":10,"weekday":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);mo=dt.dt.month.to_numpy();wd=dt.dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mo[ix[0]]!=10 or wd[ix[0]]!=3 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-.5:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
