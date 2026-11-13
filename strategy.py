"""v18n-2 experiment 259.
FAMILY: crude_january_refinery_restocking_demand
Mechanism: January refinery restocking supports crude through US cash-session liquidity.
Hypothesis: long CL 08:30-15:00 in January; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_january_refinery_restocking_demand";PARAMS={"month":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mon[ix[0]]!=1 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-.25:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
