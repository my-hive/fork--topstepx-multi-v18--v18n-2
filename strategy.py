"""v18n-2 experiment 124.
FAMILY: crude_opening_equity_risk_reversal
Mechanism: an exceptional crude opening repricing raises inflation/growth uncertainty; equity
index risk reprices opposite while cross-asset liquidity broadens through US session.
Hypothesis: fade NQ from completed CL 08:30-09:30 top-decile move, 09:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_opening_equity_risk_reversal";PARAMS={"lookback_sessions":120,"quantile":.90,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'CL','NQ'}<=set(panel):return ans
 d=panel['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();events={};hist=[]
 for day,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 30600<=t[i]<34200]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-120:]),.90) if len(hist)>=120 else np.inf
   if abs(move)>=th:events[str(day)]=-np.sign(move)
   hist.append(move)
 d=panel['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans['NQ']
 for day,ix in d.groupby('session',sort=False).indices.items():
  side=events.get(str(day),0);bars=[i for i in ix if 34260<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-12.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
