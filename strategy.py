"""v18n-2 experiment 179.
FAMILY: copper_tuesday_late_settlement_asia_continuation
Mechanism: Tuesday COMEX late settlement direction reflects industrial hedge flow that persists
through Asian base-metal liquidity.
Hypothesis: follow completed 15:00-17:00 HG move 00:00-04:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="copper_tuesday_late_settlement_asia_continuation";PARAMS={"weekday":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];out=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 54000<=t[i]<61200];bars=[i for i in ix if t[i]<14400]
  if dow[ix[0]]!=1 or len(x)<2 or not bars:continue
  side=np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.01:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HG' else 0.) for s,d in panel.items()}
