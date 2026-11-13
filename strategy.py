"""v18n-2 experiment 226.
FAMILY: crude_monday_midmorning_refinery_continuation
Mechanism: Monday midmorning refinery hedge flow continues into afternoon physical energy
liquidity after US desks absorb weekend inventory information.
Hypothesis: follow 10:00-11:00 CL direction 11:00-15:00 Monday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_monday_midmorning_refinery_continuation";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 36000<=t[i]<39600];bars=[i for i in ix if 39600<=t[i]<54000]
  if dow[ix[0]]!=0 or len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
