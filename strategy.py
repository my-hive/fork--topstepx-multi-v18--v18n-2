"""v18n-2 experiment 97.
FAMILY: silver_thursday_opening_liquidity_reversal
Mechanism: Thursday COMEX opening silver flow reverses as commercial liquidity replenishes after
initial price discovery.
Hypothesis: short SI Thursday 09:30-10:30 CT, $250 stop. Falsification: stressed PnL, era, or
yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_thursday_opening_liquidity_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];o=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=3:continue
  bars=[i for i in ix if 34200<=t[i]<37800]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if ref-c[i]<=-.5:break
   o[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='SI' else 0.) for s,d in panel.items()}
