"""v18n-2 experiment 232.
FAMILY: crude_march_refinery_maintenance_liquidity_reversal
Mechanism: March refinery-maintenance hedging causes opening crude overshoots that reverse as
physical and calendar-spread liquidity deepens through the US afternoon.
Hypothesis: fade 08:30-10:00 CL direction 10:00-15:00 in March; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_march_refinery_maintenance_liquidity_reversal";PARAMS={"month":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 30600<=t[i]<36000];bars=[i for i in ix if 36000<=t[i]<54000]
  if mon[ix[0]]!=3 or len(pre)<2 or not bars:continue
  side=-np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
