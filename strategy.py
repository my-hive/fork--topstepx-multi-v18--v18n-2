"""v18n-2 experiment 239.
FAMILY: crude_wednesday_europe_to_us_refinery_continuation
Mechanism: Wednesday European crude positioning continues into US refinery and inventory-hedge
liquidity during the overlapping trading session.
Hypothesis: follow 06:00-09:00 CL direction 09:00-12:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_wednesday_europe_to_us_refinery_continuation";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  pre=[i for i in ix if 21600<=t[i]<32400];bars=[i for i in ix if 32400<=t[i]<43200]
  if dow[ix[0]]!=2 or len(pre)<2 or not bars:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
