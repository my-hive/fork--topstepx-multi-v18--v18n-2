"""v18n-2 experiment 131.
FAMILY: naturalgas_gasoline_opening_energy_flow
Mechanism: exceptional US-open natural-gas repricing signals broad energy-demand and refinery
input pressure, which continues RBOB hedging execution into settlement.
Hypothesis: follow RB after causal NG top-quintile 08:30-09:30 move, 09:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="naturalgas_gasoline_opening_energy_flow";PARAMS={"lookback_sessions":60,"quantile":.80,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'NG','RB'}<=set(panel):return ans
 d=panel['NG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[];events={}
 for day,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 30600<=t[i]<34200]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.80) if len(hist)>=60 else np.inf
   if abs(move)>=th:events[str(day)]=np.sign(move)
   hist.append(move)
 d=panel['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans['RB']
 for day,ix in d.groupby('session',sort=False).indices.items():
  side=events.get(str(day),0);bars=[i for i in ix if 34260<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.006:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
