"""v18n-2 experiment 83.
FAMILY: euro_friday_weekend_carry_demand
Mechanism: Friday European portfolio rebalancing before weekend closure creates euro futures
demand during US hours.
Hypothesis: long 6E Friday 10:00-15:00 CT, $250 stop. Falsification: stressed PnL, era, or
yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="euro_friday_weekend_carry_demand";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6E' not in panel:return ans
 d=panel['6E'];o=ans['6E'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=4:continue
  bars=[i for i in ix if 36000<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-.0005:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='6E' else 0.) for s,d in panel.items()}
