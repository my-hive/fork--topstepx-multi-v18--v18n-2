"""v18n-2 experiment 173.
FAMILY: treasury_thursday_lateauction_duration_flow
Mechanism: Thursday cash-bond auction/secondary-market duration adjustment completes in late
morning; exceptional 08:30-09:30 ZB move persists into 13:00.
Hypothesis: follow top-40% Thursday ZB move 09:31-13:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="treasury_thursday_lateauction_duration_flow";PARAMS={"history_sessions":60,"quantile":.6,"weekday":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel:return ans
 d=panel['ZB'];out=ans['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();vals=[]
 for ix in d.groupby('session',sort=False).indices.values():
  x=np.array([i for i in ix if 30600<=t[i]<34200]);bars=[i for i in ix if 34200<=t[i]<46800]
  r=c[x[-1]]-c[x[0]] if len(x)>1 else 0.;q=np.quantile(np.abs(vals[-60:]),.6) if len(vals)>=60 else np.inf;side=np.sign(r) if dow[ix[0]]==3 and abs(r)>=q else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.25:break
    out[i]=side
  if len(x)>1:vals.append(r)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZB' else 0.) for s,d in panel.items()}
