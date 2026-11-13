"""v18n-2 experiment 205.
FAMILY: silver_firstweek_tuesday_industrial_momentum
Mechanism: first-week Tuesday industrial metal allocation flows reinforce the COMEX opening
impulse through US settlement.
Hypothesis: follow SI 08:30-09:30 direction through 15:00, first five calendar days Tuesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_firstweek_tuesday_industrial_momentum";PARAMS={"calendar_days":5,"weekday":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy();dom=dt.dt.day.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 30600<=t[i]<34200];bars=[i for i in ix if 34200<=t[i]<54000]
  if dow[ix[0]]!=1 or dom[ix[0]]>5 or len(x)<2 or not bars:continue
  side=np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
