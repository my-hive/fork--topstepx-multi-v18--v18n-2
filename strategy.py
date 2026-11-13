"""v18n-2 experiment 158.
FAMILY: ultrabond_monday_weekend_duration_reversal
Mechanism: duration hedges accumulated before weekend overshoot into Monday; dealer balance-sheet
normalization reverses completed two-session move.
Hypothesis: fade completed 2-session UB direction Monday, 17:00-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_monday_weekend_duration_reversal";PARAMS={"lookback_sessions":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();moves=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if len(bars)>1:
   side=-np.sign(sum(moves[-2:])) if len(moves)>=2 and dow[ix[0]]==0 else 0;moves.append(c[bars[-1]]-c[bars[0]])
   if not side:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
