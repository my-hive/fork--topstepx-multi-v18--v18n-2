"""v18n-2 experiment 161.
FAMILY: treasury_equity_duration_risk_transfer
Mechanism: a sustained Treasury duration move reflects macro discount-rate repricing that transfers
to equity futures during next US risk session.
Hypothesis: follow completed 5-session ZN direction in ES from 17:00 to 15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="treasury_equity_duration_risk_transfer";PARAMS={"lookback_sessions":5,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'ZN','ES'}<=set(panel):return ans
 z=panel['ZN']; hist={};moves=[]
 for day,g in z.groupby('session',sort=False):
  hist[str(pd.Timestamp(day).date())]=np.sign(sum(moves[-5:])) if len(moves)>=5 else 0
  moves.append(g.close.iloc[-1]-g.close.iloc[0])
 d=panel['ES'];out=ans['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();day=pd.to_datetime(d.session).dt.strftime('%Y-%m-%d').to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  side=hist.get(day[ix[0]],0);bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
