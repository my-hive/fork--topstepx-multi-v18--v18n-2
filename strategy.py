"""v18n-2 experiment 188.
FAMILY: silver_monday_prior_opening_global_momentum
Mechanism: previous US opening silver move transmits into Monday COMEX liquidity through global
precious-metal positioning.
Hypothesis: follow prior completed 08:30-09:30 SI direction from 09:30-15:00 Monday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_monday_prior_opening_global_momentum";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();prior=0.
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 34200<=t[i]<54000];side=np.sign(prior) if dow[ix[0]]==0 else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
  x=[i for i in ix if 30600<=t[i]<34200];prior=c[x[-1]]-c[x[0]] if len(x)>1 else 0.
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
