"""v18n-2 experiment 116.
FAMILY: equity_joint_lunch_execution_breadth
Mechanism: aligned exceptional ES and NQ lunch moves identify broad institutional execution,
more durable than an idiosyncratic index shock into closing liquidity.
Hypothesis: follow joint causal trailing-120-session top-5% 11:00-12:00 shocks, 12:01-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="equity_joint_lunch_execution_breadth";PARAMS={"lookback_sessions":120,"quantile":.95,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'ES','NQ'}<=set(panel):return ans
 moves={}; thresholds={}
 for s in ('ES','NQ'):
  d=panel[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
  for day,ix in d.groupby('session',sort=False).indices.items():
   pre=[i for i in ix if 39600<=t[i]<43200]
   if len(pre)>1:
    moves.setdefault(str(day),{})[s]=c[pre[-1]]-c[pre[0]]
    thresholds.setdefault(str(day),{})[s]=np.quantile(np.abs(hist[-120:]),.95) if len(hist)>=120 else np.inf
    hist.append(moves[str(day)][s])
 for s,stop in (('ES',5.),('NQ',12.5)):
  d=panel[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans[s]
  for day,ix in d.groupby('session',sort=False).indices.items():
   z=moves.get(str(day),{});q=thresholds.get(str(day),{})
   if not (set(z)=={'ES','NQ'} and all(abs(z[x])>=q[x] for x in z) and np.sign(z['ES'])==np.sign(z['NQ'])):continue
   bars=[i for i in ix if 43260<=t[i]<54000]
   if not bars:continue
   side=np.sign(z[s]);ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-stop:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s in ('ES','NQ') else 0.) for s,d in panel.items()}
