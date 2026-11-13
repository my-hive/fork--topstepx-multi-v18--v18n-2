"""v18n-2 experiment 133.
FAMILY: treasury_friday_duration_hedge_flow
Mechanism: Friday duration hedging and dealer balance-sheet adjustment create persistent long-bond
buying through the US session ahead of weekend liquidity withdrawal.
Hypothesis: long ZB Friday 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="treasury_friday_duration_hedge_flow";PARAMS={"weekday":4,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel:return ans
 d=panel['ZB'];out=ans['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if dow[ix[0]]!=4:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-.25:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZB' else 0.) for s,d in panel.items()}
