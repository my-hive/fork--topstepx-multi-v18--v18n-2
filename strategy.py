"""v18n-2 experiment 166.
FAMILY: spx_asia_to_us_risk_transfer_momentum
Mechanism: a sustained Asia-to-Europe equity-risk move transfers into US institutional futures
liquidity and continues through cash-session positioning.
Hypothesis: follow completed 10-session ES Asia direction 08:30-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="spx_asia_to_us_risk_transfer_momentum";PARAMS={"lookback_sessions":10,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel:return ans
 d=panel['ES'];out=ans['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();moves=[]
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if t[i]>=61200 or t[i]<21600];bars=[i for i in ix if 30600<=t[i]<54000]
  side=np.sign(sum(moves[-10:])) if len(moves)>=10 else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-5:break
    out[i]=side
  if len(x)>1:moves.append(c[x[-1]]-c[x[0]])
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
