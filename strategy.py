"""v18n-2 experiment 245.
FAMILY: nasdaq_november_earnings_rebalance_demand
Mechanism: November earnings completion and year-end benchmark rebalancing support NQ demand
through US cash-session liquidity.
Hypothesis: long NQ 08:30-15:00 in November; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_november_earnings_rebalance_demand";PARAMS={"month":11,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];out=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mon[ix[0]]!=11 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-12.5:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
