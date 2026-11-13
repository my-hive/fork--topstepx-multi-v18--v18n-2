"""v18n-2 experiment 183.
FAMILY: silver_september_extreme_industrial_reversal
Mechanism: September industrial restocking can create an exceptional prior COMEX move that is
reversed by next-session dealer inventory balancing.
Hypothesis: fade causal top-quintile prior US-session SI move in next US session; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_september_extreme_industrial_reversal";PARAMS={"history_sessions":60,"quantile":.8,"month":9,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mo=pd.to_datetime(d.session).dt.month.to_numpy();rets=[]
 for ix in d.groupby('session',sort=False).indices.values():
  prev=rets[-1] if rets else 0.;q=np.quantile(np.abs(rets[-61:-1]),.8) if len(rets)>=61 else np.inf;bars=[i for i in ix if 30600<=t[i]<54000]
  side=-np.sign(prev) if mo[ix[0]]==9 and abs(prev)>=q else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
  x=[i for i in ix if 30600<=t[i]<54000];rets.append(c[x[-1]]-c[x[0]] if len(x)>1 else 0.)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
