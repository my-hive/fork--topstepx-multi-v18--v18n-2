"""v18n-2 experiment 164.
FAMILY: naturalgas_monday_asia_shock_continuation
Mechanism: exceptional Asian natural-gas repricing reflects weather and LNG flow information;
Monday US liquidity continues this newly incorporated supply-demand shock.
Hypothesis: follow top-30% 06:00-08:30 NG move Monday through 15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="naturalgas_monday_asia_shock_continuation";PARAMS={"history_sessions":60,"quantile":.7,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NG' not in panel:return ans
 d=panel['NG'];out=ans['NG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();vals=[]
 for ix in d.groupby('session',sort=False).indices.values():
  x=np.array([i for i in ix if 21600<=t[i]<30600]);bars=[i for i in ix if 30600<=t[i]<54000]
  r=c[x[-1]]-c[x[0]] if len(x)>1 else 0.;q=np.quantile(np.abs(vals[-60:]),.7) if len(vals)>=60 else np.inf
  side=np.sign(r) if dow[ix[0]]==0 and abs(r)>=q else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.025:break
    out[i]=side
  if len(x)>1:vals.append(r)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NG' else 0.) for s,d in panel.items()}
