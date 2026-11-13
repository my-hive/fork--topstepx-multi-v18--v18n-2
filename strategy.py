"""v18n-2 experiment 189.
FAMILY: silver_wednesday_late_comex_settlement_momentum
Mechanism: Wednesday late COMEX silver execution momentum persists into settlement as industrial
and dealer hedges finish.
Hypothesis: follow 13:00-14:00 SI direction 14:00-15:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_wednesday_late_comex_settlement_momentum";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 46800<=t[i]<50400];bars=[i for i in ix if 50400<=t[i]<54000]
  if dow[ix[0]]!=2 or len(x)<2 or not bars:continue
  side=np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
