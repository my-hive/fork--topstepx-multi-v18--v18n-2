"""v18n-2 experiment 139.
FAMILY: ultrabond_friday_settlement_duration_demand
Mechanism: Friday afternoon duration demand from hedging and balance-sheet adjustment persists
into Treasury settlement ahead of weekend liquidity withdrawal.
Hypothesis: long UB Friday 14:00-16:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="ultrabond_friday_settlement_duration_demand";PARAMS={"weekday":4,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel:return ans
 d=panel['UB'];out=ans['UB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if dow[ix[0]]!=4:continue
  bars=[i for i in ix if 50400<=t[i]<57600]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if c[i]-ref<=-.5:stopped=True
   else:out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='UB' else 0.) for s,d in panel.items()}
