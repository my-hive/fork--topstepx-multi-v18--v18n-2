"""v18n-2 experiment 74.
FAMILY: five_year_wednesday_policy_carry
Mechanism: Wednesday Treasury auction-cycle hedging creates persistent front-end rate demand
through the US session.
Hypothesis: long ZF Wednesday 17:00 CT through 15:00 CT, $250 stop. Falsification: stressed
PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="five_year_wednesday_policy_carry";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZF' not in panel:return ans
 d=panel['ZF'];o=ans['ZF'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=2:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-.25:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='ZF' else 0.) for s,d in panel.items()}
