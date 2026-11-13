"""v18n-2 experiment 154.
FAMILY: ultrabond_shortterm_duration_reversal
Mechanism: a sustained 5-session duration move is crowded by mortgage and liability hedgers; next
session reverses as hedge demand normalizes.
Hypothesis: fade completed 5-session UB mean return at next reopen through US close; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_shortterm_duration_reversal";PARAMS={"lookback_sessions":5,"zscore":.5,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();moves=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if len(bars)>1:
   z=np.mean(moves[-5:])/(np.std(moves[-5:])+1e-12) if len(moves)>=5 else 0;side=-np.sign(z) if abs(z)>=.5 else 0;moves.append(c[bars[-1]]-c[bars[0]])
   if not side:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.5:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
