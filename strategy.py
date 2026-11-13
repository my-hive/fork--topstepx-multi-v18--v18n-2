"""v18n-2 experiment 165.
FAMILY: silver_thursday_asia_industrial_reversal
Mechanism: early-week Asian silver industrial hedging leaves a stale 20-session directional
position that reverses during Thursday US physical-liquidity transfer.
Hypothesis: fade completed 20-session Asia direction in SI Thursday 08:30-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_thursday_asia_industrial_reversal";PARAMS={"lookback_sessions":20,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();moves=[]
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 21600<=t[i]<30600];bars=[i for i in ix if 30600<=t[i]<54000]
  side=-np.sign(sum(moves[-20:])) if len(moves)>=20 and dow[ix[0]]==3 else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
  if len(x)>1:moves.append(c[x[-1]]-c[x[0]])
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
