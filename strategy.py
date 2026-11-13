"""v18n-2 experiment 182.
FAMILY: silver_march_firstweek_industrial_momentum
Mechanism: March first-week industrial restocking creates persistent overnight silver direction
through US COMEX liquidity.
Hypothesis: follow 00:00-08:30 SI direction March days 1-7 through 15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_march_firstweek_industrial_momentum";PARAMS={"month":3,"days":7,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);mo=dt.dt.month.to_numpy();day=dt.dt.day.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if t[i]<30600];bars=[i for i in ix if 30600<=t[i]<54000]
  if mo[ix[0]]!=3 or day[ix[0]]>7 or len(x)<2 or not bars:continue
  side=np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
